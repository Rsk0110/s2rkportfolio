"""Builds Rushil's resumes in Jake's Resume format (https://github.com/jakegut/resume).

Two outputs per version, from the same data:
  * <name>.tex   real Jake's-template LaTeX: paste into Overleaf (pdfLaTeX) to compile or edit.
  * <name>.html  a faithful HTML copy of the layout (Computer Modern, small-caps section rules)
                 that update_resumes.py prints to PDF for the website.

Projects, skills and awards come from build_resumes.py (shared with the designed CV), so
edit them there. Experience entries are below.
Outputs go to Portfolio/resumes/ and Documents/Rsk/Resumes/Jakes/ (+ Editable/ for the HTML).
"""
import html
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_resumes as data  # noqa: E402  (shared resume content)

ROOT = data.ROOT
OUT = os.path.join(ROOT, 'resumes')
HOME_RES = os.path.join(os.path.expanduser('~'), 'Documents', 'Rsk', 'Resumes')
JAKES_DIR = os.path.join(HOME_RES, 'Jakes')
EDITABLE = data.EDITABLE

NAME = 'Rushil Barve'
CONTACT = [
    ('+1 548 384 6520', 'tel:+15483846520'),
    ('s2rkv0110@gmail.com', 'mailto:s2rkv0110@gmail.com'),
    ('linkedin.com/in/rushil0110', 'https://www.linkedin.com/in/rushil0110/'),
    ('github.com/Rsk0110', 'https://github.com/Rsk0110'),
    ('rsk0110.github.io/s2rkportfolio', 'https://rsk0110.github.io/s2rkportfolio/'),
]

EDUCATION = [
    ('University of Waterloo', 'Waterloo, ON', 'Bachelor of Computer Science (Co-op), Computational Mathematics', 'Expected 2031'),
    ('Delhi Public School – Modern Indian School', 'Doha, Qatar', 'CBSE Senior Secondary, Computer Science', 'Graduated 2026'),
]

# (organisation, dates, role, location, bullets)
DESIGN_TEAMS = ('Waterloo Student Design Teams', 'Sep 2026 – Present', 'Member: WARG, UW Orbital, UW Game Dev', 'Waterloo, ON', [
    'Waterloo Aerial Robotics Group (WARG): member of the Autonomy and Embedded Flight Software sub-teams.',
    'UW Orbital (student satellite design team) and UW Game Dev; also Computer Science Club and UW Data Science Club.'])
LEADERSHIP = [
    ('DPS-Modern Indian School', 'May 2025 – Jun 2026', 'Director of MUN & Electoral and Democratic Club', 'Doha, Qatar', [
        "Led the school's Model UN program: organized conferences, trained delegates in research, procedure and resolution drafting.",
        'MUN trainer since May 2024; six Best Delegate awards across 8+ national and international conferences.']),
    ('TEDxYouth@DPSMIS', 'Sep – Dec 2025', 'Head of Marketing', 'Doha, Qatar', [
        'Led branding, social media and promotion for a TEDx-licensed youth event (11th edition, "Flip the Narrative").',
        'Worked across curation, design, operations and technical teams on the event campaign.']),
    ('DPSDQ MUN (25th-anniversary edition)', 'Jun – Oct 2025', 'Head of Operations', 'Doha, Qatar', [
        'Ran logistics and delegate services for the conference, coordinating with the Secretariat and support teams.']),
    ('Qatar Children’s Science Congress', 'Dec 2024 – Mar 2025', 'Team Leader', 'Doha, Qatar', [
        'Led an original student research project from experimental design to data analysis and expert-panel presentation.']),
    ('Catalyst MUN · Global MUN Network', 'Jun 2025 – May 2026', 'Head Chair & Delegate Mentor', 'Doha, Qatar / Online', [
        'Head Chair of the Historical Security Council (Catalyst MUN) and the WHO (Global MUN Network); mentored first-time delegates.']),
    ('HuAr (Humanities.Arts)', 'Feb 2024 – Mar 2025', 'Co-Founder', 'Doha, Qatar', [
        'Co-founded a student organization guiding students on humanities and arts paths; organized conferences and speaker sessions.']),
    ('Q-SOMA (Qatar Society of Medical Aspirants)', 'Jun 2025 – Jun 2026', 'Head of Outreach & Logistics', 'Doha, Qatar', [
        'Led outreach and logistics and supported event management for the society.']),
]
LEADERSHIP_EXTRA = [
    ('New Gen Network', 'Aug – Nov 2025', 'Event Manager', 'Doha, Qatar', []),
    ('SFI Football Cup (StraightForwardInsight)', 'May 2025', 'Event Coordinator', 'Doha, Qatar', ['Coordinated logistics and operations for a charity football cup.']),
    ('AetherMUN · Luminos Foundation', 'May – Aug 2025', 'Content Contributor · Brand Ambassador', 'Online', []),
    ('DPS-Modern Indian School', 'May 2024 – Jan 2025', 'Education Mentor', 'Doha, Qatar', ['Mentored a junior student while in Grade 11.']),
    ('CMU-Qatar MindCraft Workshop · Embassy of India', 'Jun – Nov 2024', 'Student Volunteer', 'Doha, Qatar', ['Assisted students with robotics activities; volunteered at the International Day of Yoga.']),
]

HACK_LINE = ('8 hackathons, 5 won, 1 organised: FormulaTech Hacks 2026 (Waterloo; Winner, Ampere: AI for Motor Safety), '
             'RevenueCat Shipaton, OpenCV AI Competition (AWS), Nebius x NVIDIA Global AI Hackathon, IBM BOB 2.0 (all 2026), '
             'DPS MIS Doha (2025), Birla School (2024), CMU Qatar (2023).')

# Which sections each version gets. Projects use data.RESUME_PROJECTS (key -> bullet count).
VERSIONS = {
    # projects: key -> bullets shown; exp: number of leadership roles; exp_bullets: bullets per role
    'Rushil_Barve_Resume': dict(title='Resume', exp=3, exp_bullets=1, awards='short', certs=False, extra=False,
        projects={'circuitguard': 3, 'whisper': 3, 'mun': 2, 'occupancy': 2}),
    'Rushil_Barve_Coop_Resume': dict(title='Co-op Resume', exp=4, exp_bullets=1, awards='short', certs=True, extra=False,
        projects={'circuitguard': 3, 'whisper': 2, 'mun': 2, 'occupancy': 1}),
    'Rushil_Barve_Hackathon_Resume': dict(title='Hackathon Resume', exp=2, exp_bullets=1, awards='hack', certs=False, extra=False,
        projects={'circuitguard': 3, 'whisper': 2, 'smash': 2, 'mun': 1, 'occupancy': 1}),
    'Rushil_Barve_Full_CV': dict(title='Full CV', exp=None, exp_bullets=None, awards='full', certs=True, extra=True, pages=2,
        projects={'circuitguard': 3, 'whisper': 3, 'daydream': 2, 'lanternlight': 2, 'mun': 3, 'paypilot': 2, 'occupancy': 3, 'smash': 2, 'tracknector': 2, 'corso': 2}),
}


def awards(kind):
    if kind == 'hack':
        return [HACK_LINE] + data.ACH_SHORT_LIST[:3]
    if kind == 'full':
        return [HACK_LINE] + data.ACH_FULL_LIST
    return [HACK_LINE] + data.ACH_SHORT_LIST


def projects(which):
    by = {p['key']: p for p in data.PROJECTS}
    return [(by[k], n) for k, n in which.items() if k in by]


def experience(cfg):
    lead = LEADERSHIP if cfg['exp'] is None else LEADERSHIP[:cfg['exp']]
    rows = [DESIGN_TEAMS] + lead + (LEADERSHIP_EXTRA if cfg['extra'] else [])
    n = cfg.get('exp_bullets')
    return [(o, d, r, l, b[:n] if n else b) for o, d, r, l, b in rows]


def skills(cfg):
    rows = list(data.SKILL_ROWS)
    if cfg['certs']:
        certs = data.CERT_LIST if cfg['extra'] else [c for c in data.CERT_LIST if 'Bloomberg' not in c]  # technical ones only on one-pagers
        rows.append(('Certifications', '; '.join(certs)))
    return rows


# --------------------------------------------------------------------------- LaTeX
TEX_PREAMBLE = r'''%-------------------------
% Resume in Latex
% Author : Jake Gutierrez
% Based off of: https://github.com/sb2nov/resume
% License : MIT
%------------------------

\documentclass[letterpaper,11pt]{article}

\usepackage{latexsym}
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage[usenames,dvipsnames]{color}
\usepackage{verbatim}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{} % clear all header and footer fields
\fancyfoot{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Adjust margins
\addtolength{\oddsidemargin}{-0.5in}
\addtolength{\evensidemargin}{-0.5in}
\addtolength{\textwidth}{1in}
\addtolength{\topmargin}{-.5in}
\addtolength{\textheight}{1.0in}

\urlstyle{same}

\raggedbottom
\raggedright
\setlength{\tabcolsep}{0in}

% Sections formatting
\titleformat{\section}{
  \vspace{-4pt}\scshape\raggedright\large
}{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]

% Ensure that generate pdf is machine readable/ATS parsable
\pdfgentounicode=1

%-------------------------
% Custom commands
\newcommand{\resumeItem}[1]{
  \item\small{
    {#1 \vspace{-2pt}}
  }
}

\newcommand{\resumeSubheading}[4]{
  \vspace{-2pt}\item
    \begin{tabular*}{0.97\textwidth}[t]{l@{\extracolsep{\fill}}r}
      \textbf{#1} & #2 \\
      \textit{\small#3} & \textit{\small #4} \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeProjectHeading}[2]{
    \item
    \begin{tabular*}{0.97\textwidth}{l@{\extracolsep{\fill}}r}
      \small#1 & #2 \\
    \end{tabular*}\vspace{-7pt}
}

\newcommand{\resumeSubItem}[1]{\resumeItem{#1}\vspace{-4pt}}

\renewcommand\labelitemii{$\vcenter{\hbox{\tiny$\bullet$}}$}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0.15in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}}
\newcommand{\resumeItemListEnd}{\end{itemize}\vspace{-5pt}}

%-------------------------------------------
%%%%%%  RESUME STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\begin{document}
'''


def tex(s):
    """Escapes plain text for LaTeX (UTF-8 input; Overleaf pdfLaTeX handles – — ’ ·)."""
    rep = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_',
           '{': r'\{', '}': r'\}', '^': r'\^{}', '~': r'$\sim$', '·': r'$\cdot$', '"': "''"}
    out = ''.join(rep.get(c, c) for c in s)
    # opening quotes for "quoted" phrases
    import re
    return re.sub(r"''(\w)", r"``\1", out)


def build_tex(cfg):
    L = [TEX_PREAMBLE, '%----------HEADING----------',
         r'\begin{center}', fr'    \textbf{{\Huge \scshape {tex(NAME)}}} \\ \vspace{{1pt}}',
         '    \\small ' + ' $|$ '.join(fr'\href{{{u}}}{{\underline{{{tex(t)}}}}}' for t, u in CONTACT),
         r'\end{center}', '', '%-----------EDUCATION-----------', r'\section{Education}', r'  \resumeSubHeadingListStart']
    for school, loc, degree, date in EDUCATION:
        L.append(f'    \\resumeSubheading\n      {{{tex(school)}}}{{{tex(loc)}}}\n      {{{tex(degree)}}}{{{tex(date)}}}')
    L += [r'  \resumeSubHeadingListEnd', '', '%-----------PROJECTS-----------', r'\section{Projects}', r'    \resumeSubHeadingListStart']
    for p, n in projects(cfg['projects']):
        title = tex(p['title']) + ' $|$ \\emph{' + tex(p['stack'].replace(' · ', ', ')) + '}'
        L.append(f'      \\resumeProjectHeading\n          {{\\textbf{{{title}}}}}{{{tex(p["date"])}}}')
        L.append('          \\resumeItemListStart')
        L += [f'            \\resumeItem{{{tex(b)}}}' for b in p['bullets'][:n]]
        L.append('          \\resumeItemListEnd')
    L += [r'    \resumeSubHeadingListEnd', '', '%-----------EXPERIENCE-----------', r'\section{Experience \& Leadership}', r'  \resumeSubHeadingListStart']
    for org, date, role, loc, bullets in experience(cfg):
        L.append(f'    \\resumeSubheading\n      {{{tex(org)}}}{{{tex(date)}}}\n      {{{tex(role)}}}{{{tex(loc)}}}')
        if bullets:
            L.append('      \\resumeItemListStart')
            L += [f'        \\resumeItem{{{tex(b)}}}' for b in bullets]
            L.append('      \\resumeItemListEnd')
    L += [r'  \resumeSubHeadingListEnd', '', '%-----------AWARDS-----------', r'\section{Hackathons \& Awards}', r' \begin{itemize}[leftmargin=0.15in, label={}]', r'    \small{\item{']
    L.append(' \\\\\n'.join(f'     $\\bullet$ {tex(a)}' for a in awards(cfg['awards'])))
    L += [r'    }}', r' \end{itemize}', '', '%-----------TECHNICAL SKILLS-----------', r'\section{Technical Skills}',
          r' \begin{itemize}[leftmargin=0.15in, label={}]', r'    \small{\item{']
    L.append(' \\\\\n'.join(f'     \\textbf{{{tex(k)}}}{{: {tex(v)}}}' for k, v in skills(cfg)))
    L += [r'    }}', r' \end{itemize}', '', '%-------------------------------------------', r'\end{document}', '']
    return '\n'.join(L)


# --------------------------------------------------------------------------- HTML
CSS = '''
@font-face { font-family: "CMU Serif"; font-weight: 400; font-style: normal; src: url("https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/fonts/cmu-serif-500-roman.woff2") format("woff2"); }
@font-face { font-family: "CMU Serif"; font-weight: 400; font-style: italic; src: url("https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/fonts/cmu-serif-500-italic.woff2") format("woff2"); }
@font-face { font-family: "CMU Serif"; font-weight: 700; font-style: normal; src: url("https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/fonts/cmu-serif-700-roman.woff2") format("woff2"); }
@font-face { font-family: "CMU Serif"; font-weight: 700; font-style: italic; src: url("https://cdn.jsdelivr.net/npm/computer-modern@0.1.2/fonts/cmu-serif-700-italic.woff2") format("woff2"); }
@page { size: 8.5in 11in; margin: 0.5in 0.5in 0.45in; }
* { box-sizing: border-box; }
html { background: #888; }
body { margin: 0; font-family: "CMU Serif", "Latin Modern Roman", "Computer Modern", Georgia, serif; color: #000; font-size: var(--fs, 11pt); line-height: 1.18; }
.page { width: 8.5in; min-height: 11in; margin: 16px auto; padding: 0.5in; background: #fff; box-shadow: 0 4px 24px rgba(0,0,0,.4); }
@media print { html { background: #fff; } .page { margin: 0; padding: 0; width: auto; min-height: 0; box-shadow: none; } .toolbar { display: none !important; } }
a { color: inherit; }
header { text-align: center; margin-bottom: 0.35em; }
header h1 { font-size: 2.26em; font-weight: 700; font-variant: small-caps; letter-spacing: .01em; margin: 0 0 .12em; line-height: 1; }
header .contact { font-size: .91em; }
header .contact a { text-decoration: underline; }
header .contact .sep { margin: 0 .35em; }
section { break-inside: auto; }
h2 { font-size: 1.2em; font-weight: 400; font-variant: small-caps; margin: .55em 0 .3em; padding-bottom: .05em; border-bottom: 0.6px solid #000; line-height: 1.15; break-after: avoid; }
.entry { margin: 0 0 .32em .15in; break-inside: avoid; }
.row { display: flex; justify-content: space-between; gap: 1em; }
.row1 b { font-weight: 700; }
.row2 { font-style: italic; font-size: .91em; }
.proj { font-size: .91em; }
.proj .t b { font-weight: 700; } .proj .t em { font-style: italic; }
ul.items { margin: .12em 0 .1em; padding-left: .32in; font-size: .91em; }
ul.items li { margin: 0 0 .1em; }
.plain { margin: 0 0 0 .15in; font-size: .91em; }
.plain div { margin-bottom: .14em; }
.toolbar { position: sticky; top: 0; z-index: 10; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: center; padding: 10px; background: #1b2433; color: #fff; font: 13px Arial, sans-serif; }
.toolbar button { font: inherit; font-weight: 700; padding: 7px 14px; border-radius: 8px; border: 0; cursor: pointer; background: #fff; color: #1b2433; }
.toolbar button.on { background: #3b82f6; color: #fff; }
.toolbar span { opacity: .75; }
body.editing .page [contenteditable="true"] { outline: 1px dashed rgba(59,130,246,.6); }
'''

TOOLBAR = ('<div class="toolbar"><button id="editBtn">Edit mode: off</button><button id="pdfBtn">Save as PDF</button>'
           '<button id="saveBtn">Save edited file</button><span>Jake\'s template. Click text to edit; Enter in a bullet adds a new one. '
           'Print dialog: Save as PDF, paper Letter, Margins Default. For LaTeX, use the matching .tex file in Overleaf.</span></div>')

SCRIPT = '''<script>
(function(){
  var page=document.querySelector('.page'), editing=false, btn=document.getElementById('editBtn');
  // Keep the resume on its page budget: shrink the font a little if content overflows.
  var np=(+page.dataset.pages||1), budget=np*(11-0.95)*96 - 6 - (np-1)*72;  // leave room for the gap at each page break
  function fit(){
    var fs=11; document.body.style.setProperty('--fs', fs+'pt');
    var box=page.querySelector('.content'); var content=function(){ return box.getBoundingClientRect().height; };
    while(content()>budget && fs>9.45){ fs-=0.1; document.body.style.setProperty('--fs', fs.toFixed(1)+'pt'); }
  }
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(fit);
  function set(on){ editing=on; document.body.classList.toggle('editing',on);
    page.querySelectorAll('li, .t, .row span, .plain div, h1, h2, .contact').forEach(function(el){ if(on) el.setAttribute('contenteditable','true'); else el.removeAttribute('contenteditable'); });
    btn.textContent='Edit mode: '+(on?'on':'off'); btn.classList.toggle('on',on); }
  btn.onclick=function(){ set(!editing); };
  document.addEventListener('click',function(e){ if(editing && e.target.closest('a')) e.preventDefault(); });
  document.addEventListener('keydown',function(e){ if(!editing||e.key!=='Enter') return; var li=e.target.closest&&e.target.closest('li'); if(!li) return;
    e.preventDefault(); var n=document.createElement('li'); n.setAttribute('contenteditable','true'); n.textContent='New point'; li.after(n); n.focus(); });
  document.getElementById('pdfBtn').onclick=function(){ var was=editing; set(false); fit(); window.print(); if(was) set(true); };
  document.getElementById('saveBtn').onclick=function(){ var was=editing; set(false);
    var a=document.createElement('a'); a.href=URL.createObjectURL(new Blob(['<!DOCTYPE html>\\n'+document.documentElement.outerHTML],{type:'text/html'}));
    a.download=location.pathname.split('/').pop()||'resume.html'; a.click(); if(was) set(true); };
})();
</script>'''

e = html.escape


def build_html(cfg):
    H = [f'<header><h1>{e(NAME)}</h1><div class="contact">' +
         '<span class="sep">|</span>'.join(f'<a href="{u}">{e(t)}</a>' for t, u in CONTACT) + '</div></header>']
    H.append('<section><h2>Education</h2>')
    for school, loc, degree, date in EDUCATION:
        H.append(f'<div class="entry"><div class="row row1"><span><b>{e(school)}</b></span><span>{e(loc)}</span></div>'
                 f'<div class="row row2"><span>{e(degree)}</span><span>{e(date)}</span></div></div>')
    H.append('</section><section><h2>Projects</h2>')
    for p, n in projects(cfg['projects']):
        H.append(f'<div class="entry proj"><div class="row"><span class="t"><b>{e(p["title"])}</b> | <em>{e(p["stack"].replace(" · ", ", "))}</em></span>'
                 f'<span>{e(p["date"])}</span></div><ul class="items">' + ''.join(f'<li>{e(b)}</li>' for b in p['bullets'][:n]) + '</ul></div>')
    H.append('</section><section><h2>Experience &amp; Leadership</h2>')
    for org, date, role, loc, bullets in experience(cfg):
        ul = ('<ul class="items">' + ''.join(f'<li>{e(b)}</li>' for b in bullets) + '</ul>') if bullets else ''
        H.append(f'<div class="entry"><div class="row row1"><span><b>{e(org)}</b></span><span>{e(date)}</span></div>'
                 f'<div class="row row2"><span>{e(role)}</span><span>{e(loc)}</span></div>{ul}</div>')
    H.append('</section><section><h2>Hackathons &amp; Awards</h2><div class="plain">' +
             ''.join(f'<div>• {e(a)}</div>' for a in awards(cfg['awards'])) + '</div></section>')
    H.append('<section><h2>Technical Skills</h2><div class="plain">' +
             ''.join(f'<div><b>{e(k)}</b>: {e(v)}</div>' for k, v in skills(cfg)) + '</div></section>')
    body = ''.join(H)
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(NAME)} — {e(cfg["title"])}</title>'
            f'<style>{CSS}</style></head><body>{TOOLBAR}<div class="page" data-pages="{cfg.get("pages", 1)}"><div class="content">{body}</div></div>{SCRIPT}</body></html>')


def main():
    for d in (OUT, JAKES_DIR):
        os.makedirs(d, exist_ok=True)
    for name, cfg in VERSIONS.items():
        with open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8') as f:
            f.write(build_html(cfg))
        with open(os.path.join(OUT, name + '.tex'), 'w', encoding='utf-8') as f:
            f.write(build_tex(cfg))
        shutil.copy(os.path.join(OUT, name + '.tex'), os.path.join(JAKES_DIR, name + '.tex'))
        if os.path.isdir(EDITABLE):
            shutil.copy(os.path.join(OUT, name + '.html'), os.path.join(EDITABLE, name + '.html'))
    print("built Jake's-format resumes ->", OUT)


if __name__ == '__main__':
    main()
