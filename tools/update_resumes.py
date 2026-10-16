"""Rebuilds the resume PDFs and website previews from the editable resume files.

Source:  Documents\\Rsk\\Resumes\\Canva-style\\Editable\\*.html   (edit these)
Outputs: Portfolio\\resume\\<name>.pdf + <slug>-<page>.jpg      (published on the site)
         Documents\\Rsk\\Resumes\\Canva-style\\<name>.pdf        (your local copies)

Run through update-resumes.bat, which also publishes the result.
"""
import os
import shutil
import subprocess
import sys
import tempfile

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is missing. Install it with:  python -m pip install pillow")

HOME = os.path.expanduser("~")
EDITABLE = os.path.join(HOME, "Documents", "Rsk", "Resumes", "Canva-style", "Editable")
LOCAL_PDFS = os.path.join(HOME, "Documents", "Rsk", "Resumes", "Canva-style")
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resume")

# file name -> (preview slug, page count)
RESUMES = {
    "Rushil_Barve_Resume": ("general", 1),
    "Rushil_Barve_Coop_Resume": ("coop", 1),
    "Rushil_Barve_Hackathon_Resume": ("hackathon", 1),
    "Rushil_Barve_Full_CV": ("full-cv", 2),
}
BROWSERS = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
]
# Hides the editing toolbar when taking the preview screenshot (print already hides it).
HIDE_TOOLBAR = "<style>.toolbar{display:none!important}.page{margin:0!important;box-shadow:none!important}html,body{background:#fff!important}</style>"


def browser():
    for b in BROWSERS:
        if os.path.exists(b):
            return b
    sys.exit("Couldn't find Microsoft Edge or Google Chrome.")


def file_url(path):
    return "file:///" + os.path.abspath(path).replace("\\", "/")


def run(exe, *args, out=None):
    # A throwaway profile keeps headless runs independent of any open browser window.
    profile = tempfile.mkdtemp(prefix="resume-browser-")
    try:
        for _ in range(3):
            subprocess.run([exe, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--no-first-run",
                            f"--user-data-dir={profile}", "--virtual-time-budget=20000", *args],
                           capture_output=True, timeout=180)
            if out is None or os.path.exists(out):
                return
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def main():
    exe = browser()
    os.makedirs(SITE, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="resumes-")
    try:
        for name, (slug, pages) in RESUMES.items():
            src = os.path.join(EDITABLE, name + ".html")
            if not os.path.exists(src):
                print(f"  skipped {name}: {src} not found")
                continue

            # 1. PDF
            pdf = os.path.join(tmp, name + ".pdf")
            run(exe, f"--print-to-pdf={pdf}", file_url(src), out=pdf)
            if not os.path.exists(pdf):
                sys.exit(f"Failed to create the PDF for {name}.")
            shutil.copy(pdf, os.path.join(SITE, name + ".pdf"))
            shutil.copy(pdf, os.path.join(LOCAL_PDFS, name + ".pdf"))

            # 2. Preview images for the website
            page_html = os.path.join(tmp, name + ".html")
            with open(src, encoding="utf-8") as f:
                html = f.read().replace("</head>", HIDE_TOOLBAR + "</head>", 1)
            with open(page_html, "w", encoding="utf-8") as f:
                f.write(html)
            png = os.path.join(tmp, name + ".png")
            run(exe, "--hide-scrollbars", "--force-device-scale-factor=2",
                f"--window-size=794,{1123 * pages}", f"--screenshot={png}", file_url(page_html), out=png)
            im = Image.open(png).convert("RGB")
            w, h = im.size
            for i in range(pages):
                crop = im.crop((0, i * h // pages, w, (i + 1) * h // pages))
                crop.thumbnail((1200, 1700), Image.LANCZOS)
                crop.save(os.path.join(SITE, f"{slug}-{i + 1}.jpg"), "JPEG", quality=86, optimize=True, progressive=True)
            print(f"  updated {name} ({pages} page{'s' if pages > 1 else ''})")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
