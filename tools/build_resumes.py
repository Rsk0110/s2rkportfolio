"""Generates the Canva-style resumes (HTML) for Rushil Barve.

This file is the source of truth for resume CONTENT: edit the data below
(PROJECTS, RESUME_PROJECTS, HACKS, leadership(), CERT_GROUPS ...) and run
update-resumes.bat. It writes the HTML to Portfolio/resumes/ and to
Documents/Rsk/Resumes/Canva-style/Editable/; update_resumes.py then renders
the PDFs and website previews from the Editable copies.
"""
import os, html, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
OUT = os.path.join(ROOT, 'resumes')
EDITABLE = os.path.join(os.path.expanduser('~'), 'Documents', 'Rsk', 'Resumes', 'Canva-style', 'Editable')
os.makedirs(OUT, exist_ok=True)
e = html.escape

CSS = '''
@import url('https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@300;400;600;700&family=Lato:wght@400;700&display=swap');
@page { size: 210mm 297mm; margin: 0; }
:root { --navy:#263654; --line:#c3cedb; --ink:#1b2433; --muted:#4b5668; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: #888; }
body { font-family: 'Lato', Arial, sans-serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.page { width: 794px; height: 1123px; position: relative; overflow: hidden; background: #fff; margin: 0 auto; page-break-after: always; }
.page:last-child { page-break-after: auto; }
@media screen { .page { margin: 16px auto; box-shadow: 0 4px 24px rgba(0,0,0,.4); } }

/* header decoration */
.blob { position: absolute; right: 0; top: 0; width: 396px; height: 236px; background: var(--navy); border-bottom-left-radius: 130px; }
.photo { position: absolute; right: 44px; top: 30px; width: 266px; height: 266px; border-radius: 70px; object-fit: cover; object-position: 50% 6%; border: 4px solid #fff; background: #fff; box-shadow: 0 6px 18px rgba(20,30,50,.25); }
.name { position: absolute; left: 42px; top: 30px; font-family: 'Josefin Sans', sans-serif; color: var(--navy); line-height: .98; }
.name .first { font-size: 54px; font-weight: 300; letter-spacing: 1px; }
.name .last { font-size: 64px; font-weight: 700; letter-spacing: 1px; }
.tag { position: absolute; left: 42px; top: 156px; width: 330px; font-family: 'Josefin Sans', sans-serif; font-weight: 700; font-size: 13.5px; letter-spacing: 1.3px; line-height: 1.35; color: #0d1320; }

/* left navy panel */
.side { position: absolute; left: 0; width: 262px; background: var(--navy); color: #fff; padding: 26px 22px 20px 30px; border-top-right-radius: 105px; }
.side.p1 { top: 246px; bottom: 0; }
.side.p2 { top: 0; bottom: 0; border-top-right-radius: 0; border-bottom-right-radius: 105px; padding-top: 40px; }
.side h2 { font-family: 'Josefin Sans', sans-serif; font-weight: 700; font-size: 21px; letter-spacing: 1px; margin: 14px 0 6px; }
.side h2:first-child { margin-top: 18px; }
.side p, .side li, .side div.row { font-size: 10.1px; line-height: 1.42; }
.side ul { list-style: disc; padding-left: 13px; }
.side li { margin-bottom: 3.4px; }
.side .row { margin-bottom: 4px; }
.side .row b { display: block; font-weight: 700; font-size: 8.4px; letter-spacing: .6px; opacity: .78; text-transform: uppercase; }
.side a { color: #fff; text-decoration: underline; text-decoration-color: rgba(255,255,255,.45); text-underline-offset: 2px; }

/* right column */
.main { position: absolute; left: 288px; right: 0; padding-right: 32px; }
.main.p1 { top: 308px; }
.main.p2 { top: 40px; }
.sh { margin: 0 calc(-32px / var(--z, 1)) 8px 0; border: 2px solid var(--line); border-right: none; border-radius: 36px 0 0 36px; padding: 2px 18px; font-family: 'Josefin Sans', sans-serif; font-weight: 700; font-size: 20px; letter-spacing: 1.6px; color: var(--navy); text-transform: uppercase; line-height: 1.35; }
.sec { margin-bottom: 13px; }
.item { margin-bottom: 7.5px; }
.item .t { display: flex; justify-content: space-between; gap: 10px; font-weight: 700; font-size: 11.6px; line-height: 1.3; }
.item .t span.d { font-weight: 400; color: var(--muted); font-size: 10px; white-space: nowrap; }
.item .s { font-size: 10.3px; color: var(--muted); line-height: 1.3; }
.item ul { list-style: disc; padding-left: 14px; margin-top: 1.5px; }
.item li { font-size: 10.5px; line-height: 1.36; margin-bottom: 1.4px; }
.chips { font-size: 9.3px; color: var(--muted); }
.hack { display: grid; grid-template-columns: 1fr 1fr; gap: 1px 14px; font-size: 10.6px; line-height: 1.5; }
.hack div { display: flex; justify-content: space-between; border-bottom: 1px dotted var(--line); }
.hack span { color: var(--muted); }
.cg { font-family: 'Josefin Sans', sans-serif; font-weight: 700; font-size: 11.5px; letter-spacing: 1.2px; text-transform: uppercase; color: var(--navy); margin: 7px 0 3px; }
.crow { margin-bottom: 2.4px; }
.crow .t { font-weight: 400; font-size: 10.2px; line-height: 1.32; }
.crow .t em { font-style: normal; color: var(--muted); }
.note { font-size: 10px; color: var(--muted); margin-top: 3px; }
'''

import base64
_b64 = base64.b64encode(open(os.path.join(ROOT, 'profile.jpg'), 'rb').read()).decode()
PHOTO = f'<img class="photo" src="data:image/jpeg;base64,{_b64}" alt="Rushil Barve">'
EMAIL = 's2rkv0110@gmail.com'

def header(tagline):
    return f'''<div class="blob"></div>{PHOTO}
<div class="name"><div class="first">RUSHIL</div><div class="last">BARVE</div></div>
<div class="tag">{e(tagline)}</div>'''

def side(sections, cls='p1'):
    return f'<div class="side {cls}">' + ''.join(sections) + '</div>'

def h2(t): return f'<h2>{e(t)}</h2>'
def para(t): return f'<p>{e(t)}</p>'
def ul(items): return '<ul>' + ''.join(f'<li>{e(i)}</li>' for i in items) + '</ul>'
def rows(pairs): return ''.join(f'<div class="row"><b>{e(k)}</b>{v}</div>' for k, v in pairs)

def link(href, text): return f'<a href="{href}">{e(text)}</a>'
CONTACT = h2('Contact') + rows([
    ('Email', link('mailto:' + EMAIL, EMAIL)),
    ('Portfolio', link('https://rsk0110.github.io/s2rkportfolio/', 'rsk0110.github.io/s2rkportfolio')),
    ('Phone', link('tel:+15483846520', '+1 548 384 6520')),
    ('LinkedIn', link('https://www.linkedin.com/in/rushil0110/', 'linkedin.com/in/rushil0110')),
    ('GitHub', link('https://github.com/Rsk0110', 'github.com/Rsk0110')),
    ('Devpost', link('https://devpost.com/Rsk0110', 'devpost.com/Rsk0110')),
    ('Location', 'Waterloo, Ontario')])
SKILLS = h2('Skills') + rows([
    ('Languages', 'Python, JavaScript, TypeScript, GDScript, C, SQL, HTML, CSS'),
    ('Frameworks', 'React, Vite, Tailwind CSS, FastAPI, Godot 4, Zustand'),
    ('Tools', 'Git, GitHub Actions, SQLite, IndexedDB, Render')])
CERTS = h2('Certifications') + ul([
    'Python Essentials 2 · HTML Essentials · Computer Hardware Basics',
    'Accenture Nordics – Software Engineering Job Simulation', 'Bloomberg – Client Service Job Simulation'])
ACH_SHORT = h2('Achievements') + ul([
    'Gold Medal of Distinction, International Informatics Olympiad (2023-24); Bronze (2024-25)',
    'Gold Medal of Distinction, National Science Olympiad',
    'Six Best Delegate awards across 8+ national and international MUN conferences',
    'Basketball, CBSE Qatar Clusters: Gold (2025-26), Bronze (2023-24, 2024-25)'])
ACH_FULL = h2('Honors & Awards') + ul([
    'Gold Medal of Distinction, International Informatics Olympiad (2023-24); Bronze Medal of Distinction (2024-25)',
    'Gold Medal of Distinction, National Science Olympiad',
    'Special Achievement Certificate, International Olympiad of English Language (2024-25)',
    'Best Delegate, UN Commission on Crime Prevention and Criminal Justice, Monarch MUN (2024-25)',
    'Honorary Mention, SDG 13, DPS-Modern Indian School MUN (2024-25)',
    'Six Best Delegate awards and one Honorable Mention across 8+ conferences',
    'Basketball, CBSE Qatar Clusters: Gold (2025-26); Bronze (2023-24, 2024-25); national-level athlete'])

def sh(t): return f'<div class="sh">{e(t)}</div>'
def sec(title, body): return f'<div class="sec">{sh(title)}{body}</div>'
def item(title, date='', sub='', bullets=()):
    d = f'<span class="d">{e(date)}</span>' if date else ''
    s = f'<div class="s">{e(sub)}</div>' if sub else ''
    b = '<ul>' + ''.join(f'<li>{e(x)}</li>' for x in bullets) + '</ul>' if bullets else ''
    return f'<div class="item"><div class="t"><span>{e(title)}</span>{d}</div>{s}{b}</div>'

EDU = sec('Education',
    item('University of Waterloo', 'Expected 2031', 'Computer Science (Co-op) · Computational Mathematics') +
    item('Delhi Public School – Modern Indian School, Doha', 'Graduated 2026', 'CBSE Senior Secondary, Computer Science'))

# ---------------------------------------------------------------------------
# PROJECTS: one entry per project (most important bullets first).
# RESUME_PROJECTS picks which projects each resume shows and how many bullets.
# The page layout shrinks text automatically so one-page resumes stay one page.
# ---------------------------------------------------------------------------
PROJECTS = [
    dict(key='circuitguard', title='CircuitGuard', stack='Python · FastAPI · React · Three.js',
         sub='Winner, Ampere – AI for Motor Safety · FormulaTech Hacks 2026', bullets=[
            'Real-time Formula 1 safety system: analyses live driver telemetry to detect crashes and stopped cars on the racing line and recommends the FIA response (safety car, VSC, red flag) under the 2026 sporting regulations.',
            'Models per-sector spectator risk with a Bayesian Monte Carlo insurance-pricing model, so premiums can reflect each track section instead of a blanket rate.',
            'Python/FastAPI backend on the OpenF1 API, FAISS semantic search over FIA regulations, faster-whisper radio transcription, Next.js/React 3D track view.',
            'Built with a team of four at FormulaTech Hacks 2026 (University of Waterloo).']),
    dict(key='whisper', title='Whisper Chain', stack='Godot 4 · GDScript',
         sub='Puzzle game built on function composition', bullets=[
            'Puzzle game where each villager garbles a message (reverse, swap, double, drop a word); players route the message so the distortions cancel, discovering inverses and non-commutativity.',
            'Graph solver (DFS over simple paths) finds every correct route, sets par and powers live hints; used to design and validate all 10 levels.',
            '~3,000 lines of GDScript with UI-free game logic, ~1,500 test assertions including randomized property tests, and GitHub Actions CI building web and Windows exports.',
            'All art and audio generated in code: vector portraits and per-character synthesized voices.']),
    dict(key='mun', title='MUN Chair Toolkit', stack='TypeScript · React · Vite · Tailwind · Zustand · Dexie',
         sub='Local-first web app for Model UN chairs · live on GitHub Pages', bullets=[
            'Committee-management app for Model UN chairs: committee and agenda setup, bulk delegation entry, and roll call with Present, Present and Voting, and Absent states.',
            'Automated quorum, simple-majority and two-thirds calculations, so chairs no longer count votes by hand.',
            'Kept rules in framework-free functions (src/lib/rules.ts) with automated tests; deployed to GitHub Pages.',
            'Stores everything in the browser with IndexedDB, so it works offline with no account or backend.']),
    dict(key='occupancy', title='Door Occupancy Counter (in progress)', stack='Python · SQLite · JavaScript',
         sub='Prototype: live building occupancy from door sensors', bullets=[
            'Counts people entering and leaving each door from two-beam sensor events (direction from beam order), keeping a live headcount with no manual logging.',
            'Live web dashboard, SQLite event log and automatic daily Excel reports (summary, hourly and event sheets) written with no external libraries.',
            'Sensor simulator covering edge cases (turning back, tailgating, held doors) and unit tests, so the system is testable before any hardware.']),
    dict(key='smash', title='Continental Smash', stack='Godot 4 · GDScript · GLSL shaders',
         sub='UW Game Jam Fall 2026 entry (theme: Drift)', bullets=[
            'Local two-player game where drifting continents ram each other to raise mountains and shove the rival into an ocean trench.',
            'Custom shaders for the planet, ocean, terrain and clouds, a narrated cinematic intro, particle impact effects and an Inspector-tunable ruleset.']),
    dict(key='tracknector', title='Track Nector', stack='Python · HTML · JSON · Render',
         sub='Self-hosted personal finance tracker', bullets=[
            'Lightweight tracker for card balances and daily spending built around manual entry, with no bank account linking.',
            'Chose self-hosting and manual input deliberately to keep financial data private.',
            'Wrote the account logic in Python (bank_account.py) and added Render deployment config.']),
    dict(key='corso', title='Corso Website', stack='HTML · Bootstrap · Sass · JavaScript',
         sub='First web project, from a web design course', bullets=[
            'Responsive site for courses and workshops: sticky navbar that changes on scroll, image carousel, registration and email-subscribe forms.',
            'Compiled styles from Sass with npm scripts for build and watch.']),
]

RESUME_PROJECTS = {
    'general':   (['circuitguard', 'whisper', 'mun'], 2),
    'coop':      (['circuitguard', 'whisper', 'mun'], 2),
    'hackathon': (['circuitguard', 'whisper', 'smash', 'mun'], 2),
    'full':      (['circuitguard', 'whisper', 'mun', 'occupancy', 'smash', 'tracknector', 'corso'], 2),
}

def projects(which):
    keys, n = RESUME_PROJECTS[which]
    by = {p['key']: p for p in PROJECTS}
    body = ''.join(item(by[k]['title'], by[k]['stack'], by[k]['sub'], by[k]['bullets'][:n]) for k in keys)
    return sec('Projects', body +
        '<div class="note">Source code available <a href="mailto:' + EMAIL + '?subject=Source%20code%20request" style="color:#263654;font-weight:700">on request</a> · more projects at rsk0110.github.io/s2rkportfolio</div>')

HACKS = [('FormulaTech Hacks — Winner (Ampere)', '2026'), ('RevenueCat Shipaton', '2026'), ('OpenCV AI Competition (AWS)', '2026'),
         ('Nebius x NVIDIA Global AI Hackathon', '2026'), ('IBM BOB 2.0 Hackathon', '2026'), ('DPS MIS Doha Hackathon', '2025'),
         ('Birla School Hackathon — Qatar', '2024'), ('CMU Qatar Hackathon', '2023')]
def hackathons(title='Hackathons'):
    return sec(title, '<div class="hack">' + ''.join(f'<div>{e(a)}<span>{b}</span></div>' for a, b in HACKS) + '</div><div class="note"><b>8 hackathons · 5 won · 1 organised</b></div>')

WATERLOO = sec('Waterloo Teams', item('WARG — Waterloo Aerial Robotics Group', '2026', 'Autonomy team · Embedded Flight Software team') +
    item('UW Orbital · UW Game Dev', '2026', 'Student satellite design team · built beginner-level games') +
    '<div class="note">Member: Computer Science Club, UW Data Science Club</div>')

def leadership(full=False):
    base = [
        ('Director of MUN & Electoral and Democratic Club', 'May 2025 – Jun 2026', 'DPS-Modern Indian School, Doha',
         ["Led and managed the school's MUN program: organized conferences, trained delegates, promoted diplomacy and public speaking."]),
        ('Head of Marketing, TEDxYouth@DPSMIS', 'Sep – Dec 2025', '',
         ['Led branding, social media and promotion for a TEDx-licensed youth event, working across curation, design, operations and technical teams.']),
        ('Head of Operations, DPSDQ MUN', 'Jun – Oct 2025', '',
         ['Ran logistics and delegate services for the 25th-anniversary edition, coordinating with the Secretariat.']),
        ('Team Leader, Qatar Children\u2019s Science Congress', 'Dec 2024 – Mar 2025', '',
         ['Led an original student research project from experimental design to data analysis and expert-panel presentation.']),
        ('Co-Founder, HuAr (Humanities.Arts)', 'Feb 2024 – Mar 2025', '',
         ['Co-founded a student organization guiding students on humanities and arts paths; organized conferences and speaker sessions.']),
        ('Head of Outreach & Logistics, Q-SOMA', 'Jun 2025 – Jun 2026', 'Qatar Society of Medical Aspirants',
         ['Led outreach and logistics and supported event management for the society.']),
        ('MUN Trainer & Head Chair', 'May 2024 – May 2026', 'DPS-MIS · Catalyst MUN · Global MUN Network',
         ['Trained delegates in research, procedure and resolution drafting; Head Chair of Historical Security Council (Catalyst MUN) and WHO (Global MUN Network).']),
    ]
    extra = [
        ('Event Manager, New Gen Network', 'Aug – Nov 2025', '', []),
        ('Event Coordinator, SFI Football Cup', 'May 2025', '', ['Coordinated logistics and operations for a charity football cup.']),
        ('Content Contributor, AetherMUN · Brand Ambassador, Luminos Foundation', 'May – Aug 2025', '', []),
        ('Education Mentor, DPS-Modern Indian School', 'May 2024 – Jan 2025', '', ['Mentored a junior student while in Grade 11.']),
    ]
    items = base + (extra if full else [])
    return sec('Leadership & Experience', ''.join(item(t, d, s, b) for t, d, s, b in items))

def compact_leadership():
    rows_ = [('Director of MUN, DPS-Modern Indian School', 'May 2025 – Jun 2026'), ('Head of Marketing, TEDxYouth@DPSMIS', 'Sep – Dec 2025'),
             ('Head of Operations, DPSDQ MUN', 'Jun – Oct 2025'), ('Team Leader, Qatar Children\u2019s Science Congress', 'Dec 2024 – Mar 2025')]
    return sec('Leadership', ''.join(item(t, d) for t, d in rows_))

def main(inner, cls='p1', z=1.0):
    return f'<div class="main {cls}"><div class="z" style="zoom:{z}; --z:{z}">{inner}</div></div>'

TOOLBAR_CSS = '\n.toolbar { position: sticky; top: 0; z-index: 10; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: center; padding: 10px; background: #1b2433; color: #fff; font: 13px Lato, Arial, sans-serif; }\n.toolbar button { font: inherit; font-weight: 700; padding: 7px 14px; border-radius: 8px; border: 0; cursor: pointer; background: #fff; color: #263654; }\n.toolbar button.on { background: #3b82f6; color: #fff; }\n.toolbar span { opacity: .75; }\nbody.editing .page [contenteditable="true"]:hover { outline: 1px dashed rgba(59,130,246,.8); outline-offset: 1px; }\nbody.editing .page [contenteditable="true"]:focus { outline: 2px solid #3b82f6; outline-offset: 1px; }\n@media print { .toolbar { display: none !important; } html, body { background: #fff; } }\n'
TOOLBAR_HTML = '<div class="toolbar"><button id="editBtn">Edit mode: off</button><button id="pdfBtn">Save as PDF</button><button id="addBtn">+ Bullet</button><button id="dupBtn">Duplicate entry</button><button id="delBtn">Delete entry</button><button id="saveBtn">Save edited file</button><span>Click text to edit. Press Enter in a bullet for a new point (Backspace on an empty one removes it). In the print dialog choose Save as PDF, Margins: None, and turn on Background graphics.</span></div>'
TOOLBAR_JS = "<script>\n(function(){\n  var editing=false, btn=document.getElementById('editBtn');\n  var sel='.page .z li, .page .z .t span, .page .z .s, .page .z .note, .page .z .hack div, .page .z .hack div span, .page .side p, .page .side li, .page .side .row, .page .tag, .page .name div, .page .sh';\n  function set(on){ editing=on; document.body.classList.toggle('editing',on);\n    document.querySelectorAll(sel).forEach(function(el){ if(on) el.setAttribute('contenteditable','true'); else el.removeAttribute('contenteditable'); });\n    btn.textContent='Edit mode: '+(on?'on':'off'); btn.classList.toggle('on',on); }\n  btn.onclick=function(){ set(!editing); }; var lastItem=null;document.addEventListener(\"focusin\",function(ev){var it=ev.target.closest&&ev.target.closest(\".item\"); if(it) lastItem=it;});function selectAll(el){var r=document.createRange(); r.selectNodeContents(el); var sl=getSelection(); sl.removeAllRanges(); sl.addRange(r);}function caretEnd(el){var r=document.createRange(); r.selectNodeContents(el); r.collapse(false); var sl=getSelection(); sl.removeAllRanges(); sl.addRange(r);}function newLi(){var n=document.createElement(\"li\"); n.setAttribute(\"contenteditable\",\"true\"); n.textContent=\"New point\"; return n;}document.addEventListener(\"keydown\",function(ev){ if(!editing) return; var li=ev.target.closest&&ev.target.closest(\"li\"); if(!li||li.getAttribute(\"contenteditable\")!==\"true\") return; if(ev.key===\"Enter\"){ev.preventDefault(); var n=newLi(); li.after(n); n.focus(); selectAll(n);} else if((ev.key===\"Backspace\"||ev.key===\"Delete\")&&li.textContent.trim()===\"\"){ev.preventDefault(); var p=li.previousElementSibling; li.remove(); if(p){p.focus(); caretEnd(p);}}});function needItem(){ if(!editing){alert(\"Turn Edit mode on first.\"); return null;} if(!lastItem||!lastItem.isConnected){alert(\"Click inside an entry first.\"); return null;} return lastItem;}document.getElementById(\"addBtn\").onclick=function(){var it=needItem(); if(!it) return; var ul=it.querySelector(\"ul\"); if(!ul){ul=document.createElement(\"ul\"); it.appendChild(ul);} var n=newLi(); ul.appendChild(n); n.focus(); selectAll(n);};document.getElementById(\"dupBtn\").onclick=function(){var it=needItem(); if(!it) return; it.after(it.cloneNode(true));};document.getElementById(\"delBtn\").onclick=function(){var it=needItem(); if(!it) return; if(confirm(\"Delete this entry?\")) it.remove();}; document.addEventListener('click',function(ev){ if(editing && ev.target.closest('a')) ev.preventDefault(); });\n  document.getElementById('pdfBtn').onclick=function(){ var was=editing; set(false); window.print(); if(was) set(true); };\n  document.getElementById('saveBtn').onclick=function(){ var was=editing; set(false);\n    var html='<!DOCTYPE html>\\n'+document.documentElement.outerHTML; var a=document.createElement('a');\n    a.href=URL.createObjectURL(new Blob([html],{type:'text/html'})); a.download=location.pathname.split('/').pop()||'resume.html'; a.click(); if(was) set(true); };\n})();\n</script>"


def crow(title, issuer, year):
    return f'<div class="item crow"><div class="t"><span>{e(title)} <em>— {e(issuer)}</em></span><span class="d">{e(year)}</span></div></div>'

CERT_GROUPS = [
    ('Model United Nations', [
        ('UNHSC Head Chair', 'Catalyst MUN', '2025-26'),
        ('Certificate of Appreciation, Director of MUN Club and Electoral & Democratic Club', 'DPS-Modern Indian School', '2025-26'),
        ('Best Delegate', 'DPS-Monarch International School MUN', '2024-25'),
        ('Honorary Mention', 'DPS-MUN', '2024-25'),
        ('Participation as Delegate', 'DPS-MUN and DPS-Monarch MUN', '2024-25'),
    ]),
    ('Olympiads & Academics', [
        ('Gold Medal, International Informatics Olympiad', 'Silverzone Foundation', '2023-24'),
        ('Special Achievement, International Informatics Olympiad', 'Silverzone Foundation', '2023-24, 2024-25'),
        ('Special Achievement and Level 2, International Olympiad of English Language', 'Silverzone Foundation', '2024-25'),
        ('Abacus Levels 1 and 2 (Excellence) and Abacus Challenge participation', 'TCA Qatar', '2018-19'),
    ]),
    ('Sports & Cultural', [
        ('3rd Position, Basketball (Participation 2023-24)', 'CBSE Qatar Clusters', '2024-25'),
        ('2nd Position, Basketball (3rd in 2022-23)', 'Sports Rendezvous, DPS-MIS', '2023-25'),
        ('3rd Position, Group Dance', 'Sports Rendezvous, DPS-MIS', '2024-25'),
        ('1st Position, Skipping Rope Challenge', 'Sports Rendezvous, DPS-MIS', '2021-22'),
        ('Participation, Chess', 'Sports Rendezvous, DPS-MIS', '2022-23'),
        ('Level 5 Swimming completion', 'Sports Castle Academy', '2023-24'),
    ]),
    ('Other Events', [
        ('Participation, Science India Forum (QCSC)', 'SIF Indian Cultural Centre, Embassy of India Qatar', '2024-25'),
        ('Participation, Pariksha Pe Charcha', 'Ministry of Education, Government of India', '2024-25'),
    ]),
]

def certificates():
    body = ''.join(f'<div class="cg">{e(g)}</div>' + ''.join(crow(*r) for r in rows_) for g, rows_ in CERT_GROUPS)
    return sec('Certificates & Recognition', body)

FIT_JS = """<script>
// Shrinks each page's main column just enough to fit, so one-page resumes stay one page.
(function(){
  function fit(){
    document.querySelectorAll('.page').forEach(function(p){
      var z=p.querySelector('.z'); if(!z) return;
      var limit=p.getBoundingClientRect().bottom-22, zoom=parseFloat(z.style.zoom)||1;
      while(z.getBoundingClientRect().bottom>limit && zoom>0.62){ zoom-=0.01; z.style.zoom=zoom.toFixed(2); z.style.setProperty('--z',zoom.toFixed(2)); }
    });
  }
  (document.fonts&&document.fonts.ready?document.fonts.ready:Promise.resolve()).then(fit);
  window.addEventListener('beforeprint',fit);
})();
</script>"""

def page(inner, title='Rushil Barve'):
    return f'<section class="page">{inner}</section>'

def doc(title, pages):
    return f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{e(title)}</title><style>{CSS}{TOOLBAR_CSS}</style></head><body>{TOOLBAR_HTML}{"".join(pages)}{TOOLBAR_JS}{FIT_JS}</body></html>'

TAG_MAIN = 'Computer Science & Computational Mathematics · University of Waterloo'

# ---- 1. general resume ----
about_main = 'First-year Waterloo student who builds practical, privacy-minded software, competes in hackathons and olympiads, and leads teams. Looking for Winter/Spring co-op.'
resume = doc('Rushil Barve — Resume', [page(
    header(TAG_MAIN) + side([h2('About Me'), para(about_main), CONTACT, SKILLS, ACH_SHORT]) +
    main(f'{EDU}{projects("general")}{hackathons()}{WATERLOO}{compact_leadership()}', 'p1', 1.0))])

# ---- 2. co-op resume ----
about_coop = 'CS & Computational Mathematics student seeking a Winter/Spring co-op. I ship full-stack projects, lead teams and events, and communicate clearly under pressure.'
coop = doc('Rushil Barve — Co-op Resume', [page(
    header(TAG_MAIN) + side([h2('About Me'), para(about_coop), CONTACT, SKILLS, ACH_SHORT, CERTS]) +
    main(f'{EDU}{projects("coop")}{leadership()}{WATERLOO}', 'p1', 1.0))])

# ---- 3. hackathon resume ----
about_hack = 'Olympiad-level problem solver who builds fast, pitches clearly and leads teams under pressure. Eight hackathons from high school in Qatar to Waterloo.'
hack_side = h2('Strengths') + ul(['Rapid prototyping & shipping', 'Public speaking and pitching', 'Team management', 'Event logistics', 'Marketing and branding'])
hack = doc('Rushil Barve — Hackathon Resume', [page(
    header('Hackathon Builder · CS & Computational Mathematics @ UWaterloo') + side([h2('About Me'), para(about_hack), CONTACT, SKILLS, hack_side, ACH_SHORT]) +
    main(f'{projects("hackathon")}{hackathons()}{WATERLOO}{compact_leadership()}', 'p1', 1.0))])

# ---- 4. full CV (2 pages) ----
about_full = 'Computer science student at the University of Waterloo with a record in informatics olympiads, Model UN and student leadership. Experienced in leading teams, running events, training peers and public speaking, with a growing focus on building technology that has real impact.'
interests = h2('Interests') + ul(['Basketball: house captain, national-level CBSE Clusters player', 'Kickboxing (Feb 2026 – present)', 'Swimming, chess, dance, visual art'])
vol = sec('Volunteering', item('Student Volunteer, CMU-Qatar MindCraft Workshop', 'Nov 2024', '', ['Assisted students with robotics and technology activities.']) +
          item('Student Volunteer, Embassy of India International Day of Yoga', 'Jun 2024'))
p1 = page(header(TAG_MAIN) + side([h2('About Me'), para(about_full), CONTACT, SKILLS]) +
          main(f'{EDU}{projects("full")}{hackathons()}{WATERLOO}', 'p1', 1.0))
p2 = page(side([CERTS, ACH_FULL, interests], 'p2') + main(f'{leadership(True)}{vol}{certificates()}', 'p2', 1.0))
fullcv = doc('Rushil Barve — Full CV', [p1, p2])

for name, content in [('Rushil_Barve_Resume', resume), ('Rushil_Barve_Coop_Resume', coop), ('Rushil_Barve_Hackathon_Resume', hack), ('Rushil_Barve_Full_CV', fullcv)]:
    open(os.path.join(OUT, name + '.html'), 'w', encoding='utf-8').write(content)
    if os.path.isdir(EDITABLE):
        shutil.copy(os.path.join(OUT, name + '.html'), os.path.join(EDITABLE, name + '.html'))
print('built resumes ->', OUT)
