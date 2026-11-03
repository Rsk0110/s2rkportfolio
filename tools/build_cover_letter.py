"""Cover letters for Rushil, styled to match the Jake's-template resume.

Usage (PowerShell, from the Portfolio folder):
  python tools\\build_cover_letter.py                      -> generic template with [blanks]
  python tools\\build_cover_letter.py --company "Shopify" --role "Software Developer Intern" ^
         --term "Winter 2027" --why "your work on developer tooling for millions of merchants" ^
         [--manager "Jane Doe"] [--focus web|ai|games|general] [--extra "One more sentence."]

Writes <name>.html, <name>.pdf and <name>.tex to Documents\\Rsk\\Resumes\\Cover Letters\\.
The .html opens in a browser with the same Edit / Save as PDF toolbar as the resumes;
the .tex compiles in Overleaf (pdfLaTeX).
"""
import argparse
import datetime
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_jakes as jk  # noqa: E402  (contact details, fonts, LaTeX escaping)

OUT_DIR = os.path.join(os.path.expanduser('~'), 'Documents', 'Rsk', 'Resumes', 'Cover Letters')

# Middle paragraph, picked to match the job. Facts only; edit freely.
FOCUS = {
    'general': ('Most recently, my team of four won the Ampere "AI for Motor Safety" prize at FormulaTech Hacks 2026 '
                'with CircuitGuard, a real-time Formula 1 safety system that reads live driver telemetry to detect crashes '
                'and recommend the right race-control response, backed by a Python/FastAPI service and a React 3D track view. '
                'On my own, I built Whisper Chain, a puzzle game whose levels are checked by a graph solver and covered by '
                'about 1,500 test assertions with continuous integration, and the MUN Chair Toolkit, a TypeScript/React app '
                'built for Model UN chairs to run roll call and voting, deployed on GitHub Pages.'),
    'web': ('I enjoy building tools people actually use. The MUN Chair Toolkit is a local-first TypeScript/React app for '
            'Model UN chairs: it handles committee setup, roll call and automated quorum and voting thresholds, keeps its '
            'rules in framework-free, tested functions, works offline with IndexedDB, and is deployed on GitHub Pages. '
            'At FormulaTech Hacks 2026 my team of four won the Ampere "AI for Motor Safety" prize with CircuitGuard, '
            'a project spanning a Python/FastAPI backend and a React 3D front end.'),
    'ai': ('At FormulaTech Hacks 2026 my team of four won the Ampere "AI for Motor Safety" prize with CircuitGuard, a '
           'real-time Formula 1 safety system. It analyses live driver telemetry to detect crashes and stopped cars, '
           'recommends the race-control response under the FIA regulations using semantic search over the rulebook, '
           'and models per-sector spectator risk with a Bayesian Monte Carlo pricing model. I am also prototyping a door '
           'occupancy counter that uses in-browser person detection (TensorFlow.js) on a phone camera, with a live '
           'dashboard and automatic daily reports.'),
    'games': ('I build games to learn engineering properly. Whisper Chain is a Godot puzzle game built on function '
              'composition: a graph solver finds every correct route, sets par and powers live hints, and about 1,500 test '
              'assertions with continuous integration keep all ten levels solvable. For the UW Game Jam I made '
              'Continental Smash, a two-player game with custom shaders and a narrated intro, and at FormulaTech Hacks '
              '2026 my team won the Ampere "AI for Motor Safety" prize with CircuitGuard.'),
}

LEADERSHIP = ('Outside of code, I have spent the last few years organizing and leading people. As Director of my '
              "school's Model UN program I ran conferences and trained delegates, I led operations for the 25th-anniversary "
              'DPSDQ MUN and marketing for a TEDxYouth event, and I have competed in eight hackathons, winning five. '
              'At Waterloo I am a member of the WARG autonomy and embedded flight software teams. I am comfortable '
              'picking up unfamiliar tools quickly, asking good questions, and owning a piece of work from start to finish.')


def letter(a):
    blank = lambda v, name: v if v else f'[{name}]'
    company, role, term = blank(a.company, 'Company'), blank(a.role, 'Role'), blank(a.term, 'Term, e.g. Winter 2027')
    why = a.why or '[one specific thing about the company, its product or team that genuinely interests you]'
    greeting = f'Dear {a.manager},' if a.manager else f'Dear {company} Hiring Team,'
    paras = [
        f'I am a first-year Computer Science (Co-op) and Computational Mathematics student at the University of Waterloo, '
        f'and I am excited to apply for the {role} position for the {term} co-op term. I am drawn to {company} because of {why}, '
        f'and I would love to contribute while learning from your team.',
        FOCUS[a.focus],
        LEADERSHIP,
        f'Thank you for considering my application. My resume is attached, and you can see my projects, screenshots and '
        f'live demos at rsk0110.github.io/s2rkportfolio. I would welcome the chance to talk about how I could contribute '
        f'to {company} this {a.term or "[Term]"}.',
    ]
    if a.extra:
        paras.insert(3, a.extra)
    return greeting, paras


def date_str():
    d = datetime.date.today()
    return f'{d.strftime("%B")} {d.day}, {d.year}'


def build_html(a, greeting, paras):
    e = html.escape
    to = []
    if a.manager:
        to.append(a.manager)
    to.append(a.company or '[Company]')
    if a.address:
        to.append(a.address)
    contact = '<span class="sep">|</span>'.join(f'<a href="{u}">{e(t)}</a>' for t, u in jk.CONTACT)
    body = (f'<header><h1>{e(jk.NAME)}</h1><div class="contact">{contact}</div></header>'
            f'<div class="letter"><p class="date">{e(date_str())}</p>'
            f'<p class="to">{"<br>".join(e(x) for x in to)}</p>'
            f'<p class="re"><b>Re: {e(a.role or "[Role]")}, {e(a.term or "[Term]")} co-op</b></p>'
            f'<p>{e(greeting)}</p>' + ''.join(f'<p>{e(p)}</p>' for p in paras) +
            f'<p class="close">Sincerely,<br><br>{e(jk.NAME)}</p></div>')
    css = jk.CSS + '''
.letter { font-size: 1em; line-height: 1.38; margin-top: .6em; }
.letter p { margin: 0 0 .85em; text-align: left; }
.letter .date, .letter .to { text-align: left; }
.letter .re { margin-top: .2em; }
.letter .close { margin-top: 1.2em; text-align: left; }
header { border-bottom: 0.6px solid #000; padding-bottom: .35em; }
header .contact { font-size: .82em; white-space: nowrap; }
'''
    script = jk.SCRIPT.replace("page.querySelectorAll('li, .t, .row span, .plain div, h1, h2, .contact')",
                               "page.querySelectorAll('.letter p, h1, .contact')")
    toolbar = jk.TOOLBAR.replace("Jake's template. Click text to edit; Enter in a bullet adds a new one.",
                                 'Cover letter. Click text to edit, then Save as PDF.')
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(jk.NAME)} - Cover Letter</title>'
            f'<style>{css}</style></head><body>{toolbar}<div class="page" data-pages="1"><div class="content">{body}</div></div>{script}</body></html>')


def build_tex(a, greeting, paras):
    t = jk.tex
    to = ([a.manager] if a.manager else []) + [a.company or '[Company]'] + ([a.address] if a.address else [])
    contact = ' $|$ '.join(fr'\href{{{u}}}{{\underline{{{t(x)}}}}}' for x, u in jk.CONTACT)
    lines = [r'\documentclass[letterpaper,11pt]{article}', r'\usepackage[empty]{fullpage}',
             r'\usepackage[hidelinks]{hyperref}', r'\usepackage{titlesec}', r'\input{glyphtounicode}', r'\pdfgentounicode=1',
             r'\addtolength{\oddsidemargin}{-0.5in}', r'\addtolength{\evensidemargin}{-0.5in}', r'\addtolength{\textwidth}{1in}',
             r'\addtolength{\topmargin}{-.5in}', r'\addtolength{\textheight}{1.0in}', r'\setlength{\parindent}{0pt}',
             r'\setlength{\parskip}{0.8em}', r'\urlstyle{same}', '', r'\begin{document}', r'\begin{center}',
             fr'    \textbf{{\Huge \scshape {t(jk.NAME)}}} \\ \vspace{{1pt}}', fr'    \small {contact}', r'\end{center}',
             r'\vspace{-6pt}\hrule\vspace{6pt}', '', t(date_str()), '', r' \\ '.join(t(x) for x in to), '',
             fr'\textbf{{Re: {t(a.role or "[Role]")}, {t(a.term or "[Term]")} co-op}}', '', t(greeting), '']
    lines += [t(p) + '\n' for p in paras]
    lines += ['Sincerely,', '', r'\vspace{1em}', t(jk.NAME), '', r'\end{document}', '']
    return '\n'.join(lines)


def to_pdf(html_path, pdf_path):
    exe = next((b for b in [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                            r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
                            r'C:\Program Files\Google\Chrome\Application\chrome.exe'] if os.path.exists(b)), None)
    if not exe:
        return False
    profile = tempfile.mkdtemp(prefix='cl-browser-')
    try:
        subprocess.run([exe, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--no-first-run',
                        f'--user-data-dir={profile}', '--virtual-time-budget=20000', f'--print-to-pdf={pdf_path}',
                        'file:///' + os.path.abspath(html_path).replace('\\', '/')], capture_output=True, timeout=180)
    finally:
        shutil.rmtree(profile, ignore_errors=True)
    return os.path.exists(pdf_path)


def main():
    ap = argparse.ArgumentParser(description='Make a cover letter matching the Jake\'s-template resume.')
    ap.add_argument('--company'); ap.add_argument('--role'); ap.add_argument('--term')
    ap.add_argument('--why', help='what specifically draws you to the company (finishes "I am drawn to X because of ...")')
    ap.add_argument('--manager', help='hiring manager name, if known'); ap.add_argument('--address')
    ap.add_argument('--focus', choices=sorted(FOCUS), default='general', help='which projects to lead with')
    ap.add_argument('--extra', help='an extra paragraph, e.g. answering a question from the posting')
    a = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)
    name = 'Rushil_Barve_Cover_Letter' + (('_' + re.sub(r'[^A-Za-z0-9]+', '_', a.company).strip('_')) if a.company else '_Template')
    greeting, paras = letter(a)
    html_path, tex_path, pdf_path = (os.path.join(OUT_DIR, name + ext) for ext in ('.html', '.tex', '.pdf'))
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(build_html(a, greeting, paras))
    with open(tex_path, 'w', encoding='utf-8') as f:
        f.write(build_tex(a, greeting, paras))
    ok = to_pdf(html_path, pdf_path)
    print(('PDF, HTML and .tex' if ok else 'HTML and .tex (PDF failed: run from PowerShell)'), '->', OUT_DIR, '\\', name)


if __name__ == '__main__':
    main()
