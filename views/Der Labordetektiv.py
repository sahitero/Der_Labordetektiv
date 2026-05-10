import streamlit as st
import pandas as pd
import base64 # Für die Einbindung von Bildern in den App-Header
import time # Für kleinde Ladeanimationen und Verzögerungen (Analyzer)


# base64 Funktion für die Einbindung von Bildern in den App-Header
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode() # Umwandeln der Binärdaten in einen Base64-String
# Bild wird in Text umgewandelt, damit er im App-Header eingebunden werden kann. CSS kann diesen Text direkt als Hintergrund verwenden

# =========================================================
# 1) CSS STYLES
# =========================================================

# Anker für "Nach oben"-Funktion
st.markdown('<div id="top"></div>', unsafe_allow_html=True)

st.markdown("""
<style>

/* App-Hintergrund */
.stApp {
    background-color: #FFB3D1;
}

/* Globale Textfarbe */
h1, p, span, div {
    color: #4B0082 !important;
}

/* Standard-Cards, z.B. Patientenakte */
.cute-card {
    background-color: #FFF0F7;
    padding: 25px;
    border-radius: 25px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.12);
    margin-bottom: 15px;
    width: 100%;
    box-sizing: border-box;
}

/* Ergebnis-Cards, z.B. Mikroskop, Agarplatten, Blutwerte */
.result-card {
    background-color: #E6F7FF;
    padding: 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
}

/* Hinweis-Cards */
.hint-card {
    background-color: #F3E8FF;
    padding: 12px 14px;
    border-radius: 18px;
    margin-bottom: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.06);
}

/* Standard-Buttons */
div.stButton > button {
    background-color: #FFD6E8;
    color: #4B0082 !important;
    border-radius: 22px;
    border: none;
    padding: 0.6em 1.1em;
    font-weight: 700;
}

/* Button Hover-Effekt */
div.stButton > button:hover {
    background-color: #4B0082 !important;
    color: white !important;
}
/* Verhindert, dass globale Textfarben den Hover überschreiben */
div.stButton > button:hover p,
div.stButton > button:hover span,
div.stButton > button:hover div {
    color: white !important;
}

/* =========================================================
   Sticky App Header
========================================================= */

.app-header {
    position: sticky;
    top: 0;
    z-index: 999;

    background: rgba(255, 179, 209, 0.95);
    backdrop-filter: blur(8px);

    padding: 10px 6px 12px 6px;
    margin-bottom: 10px;

    border-bottom: 1px solid rgba(0,0,0,0.05);
}

/* Header Layout */
.header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}

/* Fallname */
.header-pill {
    background-color: #F3E8FF;
    border-radius: 999px;
    padding: 6px 12px;

    display: inline-block;

    font-weight: 800;
    color: #4B0082 !important;

    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);

    margin-bottom: 5px;
}

/* Score-Anzeige */
.header-score {
    background-color: #E6F7FF;
    border-radius: 999px;
    padding: 6px 12px;

    display: inline-block;

    font-weight: 800;
    color: #4B0082 !important;

    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
}

/* Header-Buttons */
.app-header div.stButton > button {
    background-color: #FFE4F1 !important;
    color: #4B0082 !important;

    border-radius: 999px !important;
    border: none !important;

    padding: 0.45em 1em !important;

    font-weight: 800 !important;

    box-shadow: 0px 6px 16px rgba(0,0,0,0.08) !important;
}

/* Hover-Effekt */
.app-header div.stButton > button:hover {
    background-color: #4B0082 !important;
    color: white !important;
}
            
/* =========================================================
   Laborstationen im Lab-Screen
========================================================= */

/* Karten der Laborstationen */
.station-card {
    background: #FFE4F1;
    border-radius: 26px;
    padding: 20px 18px;

    min-height: 260px;

    display: flex;
    flex-direction: column;
    justify-content: space-between;

    text-align: left;

    border: 1px solid rgba(75, 0, 130, 0.08);
    box-shadow: 0px 8px 18px rgba(0,0,0,0.08);
}

/* Icons der Stationen */
.station-icon {
    font-size: 34px;
    margin-bottom: 8px;
}

/* Titel der Stationen */
.station-title {
    font-size: 20px;
    font-weight: 900;
    line-height: 1.2;

    margin-bottom: 10px;

    color: #4B0082 !important;
}

/* Beschreibung der Stationen */
.station-sub {
    font-size: 15px;
    line-height: 1.65;

    margin-bottom: 14px;

    color: #6A3FA0 !important;
}

/* Status-Badges */
.station-badge {
    display: inline-block;

    width: fit-content;

    background: #E6F7FF;
    border-radius: 999px;

    padding: 7px 12px;

    font-size: 13px;
    font-weight: 800;

    color: #4B0082 !important;

    margin-top: auto;
}

/* Abstand zwischen den Karten */
.station-wrap {
    margin-bottom: 14px;
}

/* =========================================================
   Mikroskop & Labor-Elemente
========================================================= */

/* Allgemeine Screen-Box */
.screen-box {
    background-color: #FFF0F7;
    border-radius: 28px;
    padding: 20px;

    margin-bottom: 18px;

    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

/* Agarplatten */
.plate-card {
    background: #FFE4F1;

    width: 180px;
    height: 180px;

    margin: 0 auto 12px auto;

    display: flex;
    align-items: center;
    justify-content: center;

    border-radius: 999px;

    font-size: 56px;

    box-shadow:
        inset 0 0 0 8px rgba(255,255,255,0.4),
        0px 8px 18px rgba(0,0,0,0.08);
}

.plate-label {
    text-align: center;

    font-size: 18px;
    font-weight: 800;

    margin-bottom: 8px;

    color: #4B0082 !important;
}

/* Mikroskopie */
.microscope-box {
    background: #E6F7FF;

    border-radius: 28px;
    padding: 24px;

    text-align: center;

    margin-bottom: 16px;

    box-shadow: 0px 8px 18px rgba(0,0,0,0.08);
}

/* Gram-Färbung */
.gram-step-card {
    background: #F3E8FF;

    border-radius: 20px;
    padding: 16px;

    min-height: 120px;

    text-align: center;

    margin-bottom: 10px;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

.gram-step-title {
    font-weight: 800;

    margin-bottom: 8px;

    color: #4B0082 !important;
}

/* Grosse Emojis */
.big-emoji {
    font-size: 44px;

    display: block;

    margin-bottom: 10px;
}

/* Diagnose-/Hinweiskarten */
.path-card {
    background: #FFF7D6;

    border-radius: 18px;
    padding: 12px 14px;

    margin-top: 10px;
    margin-bottom: 14px;

    color: #4B0082 !important;

    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

/* =========================================================
   Dropdown / Expander
========================================================= */

/* Gesamter Dropdown */
div[data-testid="stExpander"] {
    background-color: #EFDCE6 !important;

    border-radius: 20px !important;
    border: 2px solid #E7A7C4 !important;

    overflow: hidden !important;
}

/* Dropdown-Kopf */
div[data-testid="stExpander"] summary {
    background-color: #EFDCE6 !important;

    border-radius: 20px !important;
}

/* Dropdown-Inhalt */
div[data-testid="stExpander"] div[role="region"] {
    background-color: #EFDCE6 !important;

    padding: 15px !important;
}
            
/* =========================================================
   Laborjournal
========================================================= */

.journal-card {
    background: #FFF8DC;

    border-radius: 22px;
    border: 2px dashed #E6CFA7;

    padding: 18px;
    margin-bottom: 14px;

    box-shadow: 0px 6px 15px rgba(0,0,0,0.08);
}

.journal-title {
    font-size: 20px;
    font-weight: 900;

    margin-bottom: 12px;

    color: #4B0082 !important;
}

.journal-section {
    font-weight: 800;

    margin-top: 10px;
    margin-bottom: 6px;

    color: #4B0082 !important;
}

.journal-entry {
    font-size: 14px;

    margin-left: 10px;
    margin-bottom: 4px;

    color: #5A2D82 !important;
}

/* =========================================================
   Blutanalyse
========================================================= */

.analyzer-card {
    background: #eef5fb;

    border-radius: 24px;
    border: 2px solid #d6e8f7;

    padding: 20px;
    min-height: 180px;

    margin-bottom: 12px;

    box-shadow: 0 6px 18px rgba(0,0,0,0.08);
}

.analyzer-title {
    font-size: 24px;
    font-weight: 800;

    margin-bottom: 8px;

    color: #4b0082;
}

.analyzer-sub {
    font-size: 16px;
    line-height: 1.5;

    margin-bottom: 14px;

    color: #5e2a84;
}

.analyzer-status {
    display: inline-block;

    background: #f8e7f0;
    color: #4b0082;

    border-radius: 999px;
    padding: 8px 14px;

    font-size: 14px;
    font-weight: 700;

    margin-top: 8px;
}

.machine-box {
    background: #fff8fc;

    border: 2px dashed #e5bfd1;
    border-radius: 22px;

    padding: 18px;
    margin: 12px 0 18px 0;

    color: #5e2a84;
    font-size: 17px;
    line-height: 1.6;
}

.analysis-step {
    background: #f3d6e5;

    border-radius: 18px;
    padding: 14px 18px;

    margin: 10px 0;

    color: #4b0082;
    font-weight: 600;
}

.soft-divider {
    height: 14px;
}
            
/* =========================================================
   Floating Lab Elements
========================================================= */

.floating-item {
    position: fixed;

    z-index: 0;
    pointer-events: none;

    font-size: 52px;
    opacity: 0.22;

    animation: floaty 8s ease-in-out infinite;
}

/* Positionen */

.item1 {
    top: 8%;
    left: 5%;
    animation-delay: 0s;
}

.item2 {
    top: 22%;
    right: 10%;
    animation-delay: 2s;
}

.item3 {
    bottom: 14%;
    left: 18%;
    animation-delay: 1s;
}

.item4 {
    bottom: 28%;
    right: 8%;
    animation-delay: 3s;
}

.item5 {
    top: 55%;
    left: 42%;
    animation-delay: 4s;
}

.item6 {
    top: 72%;
    right: 30%;
    animation-delay: 5s;
}

/* Floating Animation */

@keyframes floaty {

    0% {
        transform: translateY(0px) rotate(0deg) scale(1);
    }

    50% {
        transform: translateY(-20px) rotate(8deg) scale(1.08);
    }

    100% {
        transform: translateY(0px) rotate(0deg) scale(1);
    }
}

</style>
""", unsafe_allow_html=True)

# Floating Lab-Elemente anzeigen
st.markdown("""
<div class="floating-item item1">🦠</div>
<div class="floating-item item2">🧬</div>
<div class="floating-item item3">🧫</div>
<div class="floating-item item4">🔬</div>
<div class="floating-item item5">💉</div>
<div class="floating-item item6">🧪</div>
""", unsafe_allow_html=True)

# =========================================================
# 2) SESSION STATE
# =========================================================

# Aktueller Screen
if "screen" not in st.session_state:
    st.session_state.screen = "home"

# Punktestand
if "score" not in st.session_state:
    st.session_state.score = 0

# Feedback nach Diagnose
if "feedback" not in st.session_state:
    st.session_state.feedback = None

# Freigeschaltete Laborstationen
default_unlocked = {
    "Mikroskop": False,
    "Kultur & Tests": False,
    "Blutanalyse": False,
}

# Freigeschaltete Stationen
if (
    "unlocked" not in st.session_state
    or set(st.session_state.unlocked.keys()) != set(default_unlocked.keys())
):
    st.session_state.unlocked = default_unlocked.copy()

# Aktueller Fall
if "case" not in st.session_state:
    st.session_state.case = "Fall 1"

# Ausgewählte Agarplatte
if "selected_plate" not in st.session_state:
    st.session_state.selected_plate = None

# Gram-Färbung
if "gram_steps" not in st.session_state:
    st.session_state.gram_steps = []

if "gram_result" not in st.session_state:
    st.session_state.gram_result = None

# Blutanalyse
if "selected_blood_param" not in st.session_state:
    st.session_state.selected_blood_param = None

# Laborjournal
default_lab_journal = {
    "Mikroskop": [],
    "Kultur & Tests": [],
    "Blutanalyse": []
}

if (
    "lab_journal" not in st.session_state
    or set(st.session_state.lab_journal.keys()) != set(default_lab_journal.keys())
):
    st.session_state.lab_journal = {
        key: value.copy() for key, value in default_lab_journal.items()
    }

# Hilfe-Menü
if "show_help" not in st.session_state:
    st.session_state.show_help = False

# Gram-Färbung
if "gram_done" not in st.session_state:
    st.session_state.gram_done = False

# Blutanalyse
if "blood_started" not in st.session_state:
    st.session_state.blood_started = False

if "blood_done" not in st.session_state:
    st.session_state.blood_done = False

if "blood_loaded" not in st.session_state:
    st.session_state.blood_loaded = False

# Analyse-Status
if "chem_done" not in st.session_state:
    st.session_state.chem_done = False

if "hema_done" not in st.session_state:
    st.session_state.hema_done = False

# Bereits bewertete Fälle
if "scored_cases" not in st.session_state:
    st.session_state.scored_cases = {}

# =========================================================
# 3) FALLDATEN
# =========================================================
# Patientenakten und klinische Informationen der Fälle
cases = {
    "Fall 1": {
        "story": "Eine 26-jährige Patientin wird notfallmässig ins Spital eingeliefert. "
                 "Sie wirkt verwirrt und desorientiert. Die Pflege berichtet von hohem Fieber und starkem Schüttelfrost. "
                 "Bei der Untersuchung zeigt sich eine schmerzhafte Schwellung am Oberschenkel, aus dem eitriges Sekret austritt. "
                 "Eine Probe wird ins Labor geschickt.",
        "name": "Britney McAdams",
        "age": 26,
        "sex": "weiblich",
        "symptoms": "Fieber, Schüttelfrost, Verwirrtheit"
    },

    "Fall 2": {
        "story": "Eine Patientin stellt sich mit starken Halsschmerzen und Fieber vor. "
                 "Sie berichtet über Schluckbeschwerden seit mehreren Tagen. "
                 "Bei der Untersuchung zeigen sich gerötete Tonsillen und geschwollene Lymphknoten.",
        "name": "Rebekka Schmidt",
        "age": 17,
        "sex": "weiblich",
        "symptoms": "Halsschmerzen, Fieber"
    },

    "Fall 3": {
        "story": "Eine junge Patientin klagt über Schmerzen beim Wasserlassen und häufigen Harndrang. "
                 "Zusätzlich bestehen leichte Unterbauchschmerzen.",
        "name": "Sara Keller",
        "age": 24,
        "sex": "weiblich",
        "symptoms": "Dysurie, Bauchschmerzen, Häufiger Harndrang"
    },

    "Fall 4": {
        "story": "Ein Patient stellt sich mit anhaltenden Bauchschmerzen und Durchfall vor. "
                 "Er berichtet über eine kürzliche Reise ins Ausland.",
        "name": "Tim Weber",
        "age": 33,
        "sex": "männlich",
        "symptoms": "Bauchschmerzen, Durchfall, Gewichtsverlust"
    },

    "Fall 5": {
        "story": "Bei einem älteren Patienten zeigt sich eine Rötung im Bereich einer Katheterstelle. "
                 "Die Beschwerden bestehen seit mehreren Tagen.",
        "name": "Samuel D McDonald",
        "age": 72,
        "sex": "männlich",
        "symptoms": "Rötung an Katheterstelle, leichtes Fieber, Unwohlsein"
    },

    "Fall 6": {
        "story": "Eine Patientin berichtet über Juckreiz und einen weisslichen Belag im Mund- und Intimbereich. "
                 "Die Beschwerden bestehen seit einigen Tagen.",
        "name": "Kelly Keller",
        "age": 29,
        "sex": "weiblich",
        "symptoms": "Juckreiz, weisser Belag"
    }
}

# Alte Fallnamen bereinigen
if "case" in st.session_state and isinstance(st.session_state.case, str):
    if " - " in st.session_state.case:
        st.session_state.case = st.session_state.case.split(" - ")[0]

# Falls kein gültiger Fall gesetzt ist
if "case" not in st.session_state or st.session_state.case not in cases:
    st.session_state.screen = "level"
else:
    case = st.session_state.case
    data = cases[case]

# Mikroskopischer Test bei jedem Patient und die erwarteten Ergebnisse, die den Spielern angezeigt werden, wenn sie die Mikroskop-Station betreten. Diese Informationen helfen den Spielern, die mikroskopischen Eindrücke zu interpretieren und die richtigen Schlüsse zu ziehen. Es ist wichtig, dass diese Informationen klar und verständlich formuliert sind, damit die Spieler sie leicht verstehen und in ihre Diagnosen einbeziehen können.
lab_info = {
    "Fall 1": {"Mikroskop": "Diff-BB: Neutrophilie, Linksverschiebung möglich.",
               "Agarplatte": "Wachstum auf Kulturmedien erwartet.",
               "Blutprobe": "Entzündungszeichen passend zu bakterieller Infektion."},
    "Fall 2": {"Mikroskop": "Kettenbild passend zu grampositiven Kokken möglich.",
               "Agarplatte": "β-Hämolyse wäre ein wichtiger Hinweis.",
               "Blutprobe": "Entzündungszeichen passend zu Infektion."},
    "Fall 3": {"Mikroskop": "Stäbchen wären passend.",
               "Agarplatte": "MAC wäre besonders spannend.",
               "Blutprobe": "Leichte Entzündungszeichen möglich."},
    "Fall 4": {"Mikroskop": "Keine Bakterien zu sehen.",
               "Agarplatte": "Wachstum möglich, aber weniger aggressiv.",
               "Blutprobe": "Eosinophilie wäre ein zentraler Hinweis."},
    "Fall 5": {"Mikroskop": "Kokken sind sichtbar.",
               "Agarplatte": "Wachstum grampositiver Hautflora möglich.",
               "Blutprobe": "Erhöhte Entzündungszeichen."},
    "Fall 6": {"Mikroskop": "Sprosszellen oder Hyphen möglich.",
               "Agarplatte": "Pilzwachstum könnte sichtbar sein.",
               "Blutprobe": "Unspezifische Entzündungszeichen."},
}
# Agar-Ergebnisse pro Fall (COS / MAC / CNA) und die Interpretation dieser Ergebnisse. Diese Informationen helfen den Spielern, die Ergebnisse der Agarplatten zu verstehen und die richtigen Schlüsse zu ziehen. Es ist wichtig, dass diese Informationen klar und verständlich formuliert sind, damit die Spieler sie leicht verstehen und in ihre Diagnosen einbeziehen können.
micro_tests = {
    "Fall 1": {"Katalase": "positiv", "Koagulase": "positiv"},
    "Fall 2": {"Katalase": "negativ", "Koagulase": "nicht sinnvoll"},
    "Fall 3": {"Katalase": "nicht zentral", "Koagulase": "nicht sinnvoll"},
    "Fall 4": {"Katalase": "nicht sinnvoll", "Koagulase": "nicht sinnvoll"},
    "Fall 5": {"Katalase": "positiv", "Koagulase": "negativ"},
    "Fall 6": {"Katalase": "nicht primär", "Koagulase": "nicht primär"},
}
# beschreibt die Mikroskopischen Eindrücke pro Fall, die angezeigt werden, wenn die Spieler die Mikroskop-Station öffnen. Es enthält auch den Pfad zu einem Bild, das den mikroskopischen Eindruck visualisiert. Diese Bilder sollten in einem Ordner "images" im selben Verzeichnis wie die App liegen.
#Aufzeigen der Mikroskopischen Bildern
microscope_info = {
    "Fall 1": {
        "view": "Grampositive Kokken in Haufen, typisch für Staphylokokken",
        "gram_type": "Gram-positiv",
        "image": "images/fall1_mikro.png",
        "sample": "Probe: Eiter aus einer Hautabszess-Läsion"
    },
    "Fall 2": {
        "view": "Grampositive Kokken in Ketten, typisch für Streptokokken",
        "gram_type": "Gram-positiv",
        "image": "images/fall2_mikro.png",
        "sample": "Probe: Rachenabstrich"
    },
    "Fall 3": {
        "view": "Gramnegative Stäbchen sichtbar",
        "gram_type": "Gram-negativ",
        "image": "images/fall3_mikro.png",
        "sample": "Probe: Mittelstrahlurin"
    },
    "Fall 4": {
        "view": "Auffälliges, strukturiertes Ei, passend zu einem Helminthen",
        "gram_type": "Nicht sinnvoll",
        "image": "images/fall4_mikro.png",
        "sample": "Probe: Stuhlprobe"
    },
    "Fall 5": {
        "view": "Grampositive Kokken erkennbar",
        "gram_type": "Gram-positiv, aber unspezifisch",
        "image": "images/fall5_mikro.png",
        "sample": "Probe: Abstrich von der Katheterstelle"
    },
    "Fall 6": {
        "view": "Sprosszellen und Hyphen, vereinbar mit einem Hefepilz",
        "gram_type": "Nicht typisch / Pilzverdacht",
        "image": "images/fall6_mikro.png",
        "sample": "Probe: Vaginalabstrich"
    }
}

#Eine Zusammenfassung der Platteninformationen und der erwarteten Ergebnisse, die den Spielern angezeigt werden, wenn sie die Agarplatten-Station betreten. Diese Informationen helfen den Spielern, die Ergebnisse der Agarplatten zu verstehen und die richtigen Schlüsse zu ziehen. Es ist wichtig, dass diese Informationen klar und verständlich formuliert sind, damit die Spieler sie leicht verstehen und in ihre Diagnosen einbeziehen können.
growth_results = {
    "Fall 1": {"COS": "Wachstum", "MAC": "kein Wachstum", "CNA": "Wachstum"},
    "Fall 2": {"COS": "Wachstum", "MAC": "kein Wachstum", "CNA": "Wachstum"},
    "Fall 3": {"COS": "Wachstum", "MAC": "Wachstum", "CNA": "kein Wachstum"},
    "Fall 4": {"COS": "kein Wachstum", "MAC": "kein Wachstum", "CNA": "kein Wachstum"},
    "Fall 5": {"COS": "Wachstum", "MAC": "kein Wachstum", "CNA": "Wachstum"},
    "Fall 6": {"COS": "Wachstum", "MAC": "kein Wachstum", "CNA": "kein Wachstum"},
}

# Referenzwerte f¨r Blutprobe zur Interpretation
REF = {
    "CRP (mg/L)": (0, 5),
    "PCT (ng/mL)": (0, 0.05),
    "Leukos (G/L)": (4, 10),
    "Troponin (ng/L)": (0, 14),
    "Glukose (mmol/L)": (3.9, 5.6),
    "pH (BGA)": (7.35, 7.45),
    "Laktat (mmol/L)": (0.5, 2.0),
}
# Referenzwerte Differentialblutbild
REF_BLOOD_DIFF = {
    "Leukozyten (G/L)": (4, 10),
    "Neutrophile (%)": (40, 75),
    "Lymphozyten (%)": (20, 45),
    "Eosinophile (%)": (0, 6)
}
# Werte für das Blutprobenscreening
blood_values = {
    "Fall 1": {"CRP (mg/L)": 180, "PCT (ng/mL)": 8.5, "Leukos (G/L)": 18, "Laktat (mmol/L)": 4.2, "pH (BGA)": 7.28},
    "Fall 2": {"CRP (mg/L)": 95, "Leukos (G/L)": 14},
    "Fall 3": {"CRP (mg/L)": 35, "Leukos (G/L)": 12},
    "Fall 4": {"CRP (mg/L)": 8, "Leukos (G/L)": 8},
    "Fall 5": {"CRP (mg/L)": 4, "Leukos (G/L)": 9},
    "Fall 6": {"CRP (mg/L)": 20, "Leukos (G/L)": 10},
}
# Werte für das Differentialblutbild
blood_diff = {
    "Fall 1": {"Leukozyten (G/L)": 18, "Neutrophile (%)": 82, "Lymphozyten (%)": 12, "Eosinophile (%)": 1},
    "Fall 2": {"Leukozyten (G/L)": 13, "Neutrophile (%)": 78, "Lymphozyten (%)": 15, "Eosinophile (%)": 1},
    "Fall 3": {"Leukozyten (G/L)": 12, "Neutrophile (%)": 74, "Lymphozyten (%)": 18, "Eosinophile (%)": 1},
    "Fall 4": {"Leukozyten (G/L)": 8, "Neutrophile (%)": 45, "Lymphozyten (%)": 25, "Eosinophile (%)": 18},
    "Fall 5": {"Leukozyten (G/L)": 9, "Neutrophile (%)": 55, "Lymphozyten (%)": 30, "Eosinophile (%)": 2},
    "Fall 6": {"Leukozyten (G/L)": 10, "Neutrophile (%)": 55, "Lymphozyten (%)": 30, "Eosinophile (%)": 6},
}

# Erklärungstexte für Blutbild-Werte als Hilfestellung
blood_explanations = {
    "Leukozyten (G/L)": "Leukozyten sind weisse Blutkörperchen. Erhöhte Werte sprechen oft für eine Entzündung oder Infektion.",
    "Neutrophile (%)": "Neutrophile sind oft bei bakteriellen Infektionen erhöht.",
    "Lymphozyten (%)": "Lymphozyten sind häufig bei viralen Infektionen erhöht.",
    "Eosinophile (%)": "Eosinophile können bei Parasiten oder allergischen Reaktionen erhöht sein."
}

# Agar-Ergebnisse pro Fall (COS / MAC / CNA)
agar_results = {
    "Fall 1": {
        "COS": "Wachstum vorhanden, helle Kolonien, Hämolyse sichtbar.",
        "MAC": "Kein Wachstum.",
        "CNA": "Deutliches Wachstum mit Hämolyse."
    },
    "Fall 2": {
        "COS": "Deutliches Wachstum mit β-Hämolyse.",
        "MAC": "Kein Wachstum.",
        "CNA": "Wachstum vorhanden."
    },
    "Fall 3": {
        "COS": "Wachstum vorhanden.",
        "MAC": "Starkes Wachstum vorhanden.",
        "CNA": "Kein Wachstum."
    },
    "Fall 4": {
        "COS": "Kein Wachstum.",
        "MAC": "Kein Wachstum.",
        "CNA": "Kein Wachstum."
    },
    "Fall 5": {
        "COS": "leichtes Wachstum.",
        "MAC": "Kein Wachstum.",
        "CNA": "leichtes Wachstum."
    },
    "Fall 6": {
        "COS": "Mögliches atypisches Wachstum.",
        "MAC": "Kein Wachstum.",
        "CNA": "Kein Wachstum."
    }
}

# Mikroskopischer Eindruck + Gram-Ziel pro Fall
gram_data = {
    "Fall 1": "Gram-positiv, Kokken in Haufen",
    "Fall 2": "Gram-positiv, Kokken in Ketten",
    "Fall 3": "Gram-negativ, Stäbchen",
    "Fall 4": "Keine Bakterien, aber auffällige Strukturen",
    "Fall 5": "Gram-positiv, Kokken",
    "Fall 6": "Pilzstrukturen sichtbar"
}
# Die Lösungen aller Fälle
solutions = {
    "Fall 1": "Staphylococcus aureus",
    "Fall 2": "Streptococcus pyogenes",
    "Fall 3": "Escherichia coli",
    "Fall 4": "Helmintheninfektion",
    "Fall 5": "Staphylococcus epidermidis",
    "Fall 6": "Candida spp.",
}
# Mögliche Diagnosen
DIAG_CHOICES = [
    # Grampositive Bakterien
    "Staphylococcus aureus",
    "Staphylococcus epidermidis",
    "Streptococcus pyogenes",

    # Gramnegative Bakterien
    "Escherichia coli",
    "Klebsiella pneumoniae",
    "Pseudomonas aeruginosa",

    # Pilze / Parasiten
    "Candida spp.",
    "Helmintheninfektion",
    "Giardiasis (Protozoen)",

    # Virale Ursachen
    "Virale Infektion (z.B. Influenza)",
    "EBV / Mononukleose",

    # Andere Differenzialdiagnosen
    "Allergische Reaktion / Hypersensitivität",
    "Gastroenteritis (bakteriell)",
    "Gastroenteritis (viral)",
    "Pneumonie (bakteriell)",
    "Pneumonie (viral)",
    "Akutes Koronarsyndrom",
    "Diabetische Ketoazidose",

    # Unsicher
    "Unklar",
]

# ========================================================
# 4) HELPER FUNCTIONS
# ========================================================
def flag(value, low, high):
    if value < low:
        return "↓"
    if value > high:
        return "↑"
    return "✓"

def interpret_blood(diff: dict) -> list[str]:
    hints = []
    neut = float(diff.get("Neutrophile (%)", 0))
    lymph = float(diff.get("Lymphozyten (%)", 0))
    eos = float(diff.get("Eosinophile (%)", 0))

    if neut >= 70:
        hints.append("Neutrophile ↑ spricht eher für bakterielle Ursache (akut)")
    if lymph >= 45:
        hints.append("Lymphozyten ↑ spricht eher für virale Ursache")
    if eos >= 6:
        hints.append("Eosinophile ↑ spricht für Parasiten oder Allergie / Überempfindlichkeit")
    if not hints:
        hints.append("Differentialblutbild: kein klarer Hinweis → weitere Tests wichtig")
    return hints

def interpret_micro(mt: dict) -> list[str]:
    hints = []
    gram = mt.get("Gram", "").lower()
    kat = mt.get("Katalase", "").lower()
    koa = mt.get("Koagulase", "").lower()

    if "gram-positiv" in gram and "kokken" in gram and "haufen" in gram and "positiv" in kat:
        hints.append("Grampositive Kokken in Haufen + Katalase positiv = Staphylokokken")
        if "positiv" in koa:
            hints.append("Koagulase positiv = Hinweis auf Staphylococcus aureus")
        elif "negativ" in koa:
            hints.append("Koagulase negativ = eher Staphylococcus epidermidis")

    if "gram-positiv" in gram and "ketten" in gram and "negativ" in kat:
        hints.append("Grampositive Kokken in Ketten + Katalase negativ = Hinweis auf Streptokokken")

    if not hints:
        hints.append("Mikrotests: kein eindeutiger Shortcut = Kultur/ weitere Schritte beachten")
    return hints

def reset_gram_game():
    st.session_state.gram_steps = []
    st.session_state.gram_result = None

# =========================================================
# 5) SCREENS
# =========================================================

# -------------------------
# HOME SCREEN
# -------------------------
if st.session_state.screen == "home":

    # Startscreen-Hintergrund laden
    bg_image = get_base64("images/startscreen.png")

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """, unsafe_allow_html=True)

    # Abstand nach oben
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Titelbereich
    st.markdown(
    """
    <div style="text-align: center;">
    <h1 style="display: inline-block; background-color: rgba(255,255,255,0.8); padding: 10px 30px; border-radius: 15px; font-size: 65px; color: #4B0082; font-weight: 900; margin-bottom: 20px;">
    Lab Diagnose Game
    </h1>
    <p style="font-size: 28px; color: #5A2D82; font-weight: 500;">
    Willkommen im biomedizinischen Labor!
    </p>
    </div>
        """,
        unsafe_allow_html=True
    )

    # Score-Anzeige
    st.markdown(f"""
    <div style="
        text-align: center;
        font-size: 28px;
        font-weight: 700;
        color: #4B0082;
        margin-top: 20px;
    ">
        Score: {st.session_state.score}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Start-Button
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("✨ Start", key="start_home", use_container_width=True):
            st.session_state.screen = "level"
            st.session_state.selected_plate = None
            st.rerun()

# -------------------------
# LEVEL SCREEN
# -------------------------
elif st.session_state.screen == "level":
    st.title("Fall auswählen")

    st.markdown(f"""
    <div class="hint-card">
        🎯 <b>Score:</b> {st.session_state.score}
    </div>
    """, unsafe_allow_html=True)

    case_preview = {
        "Fall 1": "Schwerer Infekt mit Fieber",
        "Fall 2": "Akute Halsentzündung",
        "Fall 3": "Verdacht auf Harnwegsinfekt",
        "Fall 4": "Gastrointestinale Beschwerden",
        "Fall 5": "Infektion an Katheterstelle",
        "Fall 6": "Verdacht auf Infektion",
    }

    order = ["Fall 1", "Fall 2", "Fall 3", "Fall 4", "Fall 5", "Fall 6"]

    cols = st.columns(3)

    for i, case_key in enumerate(order):
        with cols[i % 3]:
            label = f"{case_key} - {case_preview[case_key]}"

            if st.button(label, key=f"btn_{case_key}"):

                st.session_state.case = case_key

                st.session_state.lab_journal = {
                    "Mikroskop": [],
                    "Blutanalyse": [],
                    "Kultur & Tests": []
                }

                st.session_state.unlocked = {
                    "Mikroskop": False,
                    "Blutanalyse": False,
                    "Kultur & Tests": False
                }

                st.session_state.screen = "lab"
                st.session_state.feedback = None
                st.session_state.selected_plate = None

                reset_gram_game()
                st.rerun()

    if st.button("🔙 Zurück zum Home", key="back_level"):
        st.session_state.screen = "home"
        st.rerun()
# -------------------------
# LAB SCREEN
# -------------------------
elif st.session_state.screen == "lab":
    case = st.session_state.case
    data = cases[case]

    # --- 1. HEADER ---
    if st.button("← Fallauswahl", key="back_to_lvl"):
        st.session_state.screen = "level"
        st.rerun()

    st.markdown(f"""
    <div class="header-row">
        <div class="header-pill">🧪 {case}</div>
        <div class="header-score">🎯 Score: {st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- 2. PATIENTENAKTE ---
    st.markdown(f"""
    <div class="cute-card">
    <h2>🩺 Patientenfall</h2>
    <p style="font-style: italic; font-size: 20px; line-height: 1.6;">
    "{data['story']}"
    </p>
    <hr>
    <p style="font-size: 17px;">
    <b>Patient:</b> {data['name']} ({data['age']} Jahre, {data['sex']})
    </p>
    <p style="font-size: 17px;">
    <b>Symptome:</b> {data['symptoms']}
    </p>
    </div>
    """, unsafe_allow_html=True)

    # --- 3. LABORSTATIONEN ---
    st.write("### 🔬 Laborstationen")

    col1, col2, col3 = st.columns(3, gap="medium")

    with col1:
        st.markdown(f'<div class="station-card"><div class="station-icon">🔬</div><div class="station-title">Mikroskop</div><div class="station-sub">Gram-Färbung</div><div class="station-badge">{"✅ Offen" if st.session_state.unlocked["Mikroskop"] else "🔒 Zu"}</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        if st.button("Mikroskop öffnen", key="btn_mic", use_container_width=True):
            st.session_state.unlocked["Mikroskop"] = True
            st.session_state.screen = "mikroskop"
            st.rerun()

    with col2:
        st.markdown(f'<div class="station-card"><div class="station-icon">🧫</div><div class="station-title">Kultur & Tests</div><div class="station-sub">Agarplatten</div><div class="station-badge">{"✅ Offen" if st.session_state.unlocked["Kultur & Tests"] else "🔒 Zu"}</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        if st.button("Kultur öffnen", key="btn_cul", use_container_width=True):
            st.session_state.unlocked["Kultur & Tests"] = True
            st.session_state.screen = "agar"
            st.rerun()

    with col3:
        st.markdown(f'<div class="station-card"><div class="station-icon">🩸</div><div class="station-title">Blutanalyse</div><div class="station-sub">Laborwerte</div><div class="station-badge">{"✅ Offen" if st.session_state.unlocked["Blutanalyse"] else "🔒 Zu"}</div></div>', unsafe_allow_html=True)
        st.markdown("<div style='margin-top: 18px;'></div>", unsafe_allow_html=True)
        if st.button("Blut öffnen", key="btn_bld", use_container_width=True):
            st.session_state.unlocked["Blutanalyse"] = True
            st.session_state.screen = "blutbild"
            st.rerun()

    st.markdown("---")

    # --- 4. REIHE: JOURNAL (Links) UND DIAGNOSE (Rechts) ---
    left_col, right_col = st.columns([1.5, 1], gap="large")

    with left_col:
        journal = st.session_state.lab_journal
        journal_html = '<div class="journal-card"><div class="journal-title">📓 Mein Laborjournal</div>'
        if any(journal.values()):
            for sec, entries in journal.items():
                if entries:
                    journal_html += f'<div class="journal-section">{sec}</div>'
                    for e in entries: journal_html += f'<div class="journal-entry">• {e}</div>'
        else:
            journal_html += '<div class="journal-entry">Noch keine Einträge.</div>'
        journal_html += '</div>'
        st.markdown(journal_html, unsafe_allow_html=True)

    with right_col:
        st.write("### 🧠 Finale Diagnose")
        # Das helle Design für die Selectbox wird durch CSS automatisch angewendet
        with st.form(key="final_diag"):
            diag = st.selectbox("Was ist deine Diagnose?", ["— bitte wählen —"] + DIAG_CHOICES)
            submit = st.form_submit_button("✅ Diagnose abgeben")
            
            # Die Logik für das Feedback (Punktevergabe) bleibt hier erhalten
            if submit and diag != "— bitte wählen —":
                feedback_key = f"feedback_{case}"
                if case not in st.session_state.scored_cases:
                    if diag == solutions[case]:
                        st.session_state.score += 10
                        st.session_state[feedback_key] = {"type": "success", "msg": "✅ Richtig! +10 Punkte"}
                    else:
                        st.session_state.score -= 5
                        st.session_state[feedback_key] = {"type": "error", "msg": f"❌ Falsch! Lösung: {solutions[case]}"}
                    st.session_state.scored_cases[case] = True
                    st.rerun()
        # Feedback Anzeigen
        feedback_key = f"feedback_{case}"

        if feedback_key in st.session_state:
            fb = st.session_state[feedback_key]

            if fb["type"] == "success":
                st.success(fb["msg"])
            elif fb["type"] == "error":
                st.error(fb["msg"])


# -------------------------
# AGAR SCREEN
# -------------------------
elif st.session_state.screen == "agar":
    case = st.session_state.case

    # Zurück-Button zum Labor
    if st.button("← Zurück zum Labor", key=f"back_from_agar_{case}"):
        st.session_state.screen = "lab"
        st.rerun()

  # Einführungstext
    st.markdown("""
    <div class="screen-box">
        <h1 style="text-align:center;">🧫 Kultur & Tests</h1>
        <p style="text-align:center;">Wähle eine Agarplatte aus und kombiniere das Wachstum mit den mikrobiologischen Schnelltests.</p>
    </div>
    """, unsafe_allow_html=True)

    # Glühbirne, mit Nebeninfos
    with st.expander("💡 Wissen: Was verraten uns diese Agarplatten?", expanded=False):
        st.markdown("""
        ### 🧫 Die Welt der Nährmedien
        Um Bakterien zu identifizieren, lassen wir sie auf verschiedenen "Tellern" (Agarplatten) wachsen:
        
        *   **COS (Kochblutagar mit Schafsblut):** Ein Universalmedium. Fast alles wächst hier. Besonders wichtig: Hier sieht man die **Hämolyse** (wie die Bakterien rote Blutkörperchen zerstören).
        *   **MAC (MacConkey-Agar):** Ein Selektivmedium für **gramnegative Bakterien** (z.B. Darmbakterien). Es zeigt auch, ob die Bakterien Zucker (Laktose) vergären können (gibt verschiedene Verfärbungen auf Agar!).
        *   **CNA (Colistin-Nalidixinsäure-Agar):** Ein Selektivmedium, auf dem fast nur **grampositive Bakterien** (wie Staphylokokken oder Streptokokken) wachsen.
        
        **Warum nutzen wir mehrere?** Wenn etwas auf CNA wächst, aber nicht auf MAC, wissen wir sofort: Es ist grampositiv!
        """)

    # Plattenübersicht mit Erklärungen
    st.markdown("""
    <div class="path-card">
    🧪 <b>Plattenübersicht:</b> COS = Kochblut, MAC = MacConkey, CNA = grampositive Selektion
    </div>
    """, unsafe_allow_html=True)

    # Agarplatten-Auswahl
    st.subheader("Agarplatte auswählen")

    # Drei Spalten für die Plattenauswahl mit Symbolen und Beschriftungen
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="plate-card">🧫</div>
        <div class="plate-label">COS</div>
        """, unsafe_allow_html=True)
        if st.button("COS öffnen", key=f"plate_cos_{case}"):
            st.session_state.selected_plate = "COS"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="plate-card">🧫</div>
        <div class="plate-label">MAC</div>
        """, unsafe_allow_html=True)
        if st.button("MAC öffnen", key=f"plate_mac_{case}"):
            st.session_state.selected_plate = "MAC"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="plate-card">🧫</div>
        <div class="plate-label">CNA</div>
        """, unsafe_allow_html=True)
        if st.button("CNA öffnen", key=f"plate_cna_{case}"):
            st.session_state.selected_plate = "CNA"
            st.rerun()

    st.write("")

    # Bilder für die Fälle
    plate_images = {
        "Fall 1": {
            "COS": "images/fall1_cos.png",
            "MAC": "images/fallleer_mac.png",
            "CNA": "images/fall1_cna.png"
        },
        "Fall 2": {
            "COS": "images/fall2_cos.png",
            "MAC": "images/fallleer_mac.png",
            "CNA": "images/fall2_cna.png"
        },
        "Fall 3": {
            "COS": "images/fall3_cos.png",
            "MAC": "images/fall3_mac.png",
            "CNA": "images/fallleer_mac.png"
        },
        "Fall 4": {
            "COS": "images/fallleer_cos.png",
            "MAC": "images/fallleer_mac.png",
            "CNA": "images/fallleer_mac.png"
        },
        "Fall 5": {
            "COS": "images/fall5_cos.png",
            "MAC": "images/fallleer_mac.png",
            "CNA": "images/fall5_cna.png"
        },
        "Fall 6": {
            "COS": "images/fall6_cos.png",
            "MAC": "images/fallleer_mac.png",
            "CNA": "images/fallleer_mac.png"
        }
    }

    # Agar-Befunde, schriftliche Interpretation und Schnelltest-Ergebnisse für die Fälle
    plate_text = {
        "Fall 1": {
            "COS": "Goldene Kolonien mit β-Hämolyse",
            "MAC": "Kein Wachstum",
            "CNA": "Wachstum mit β-Hämolyse"
        },
        "Fall 2": {
            "COS": "Kleine Kolonien mit starker β-Hämolyse",
            "MAC": "Kein Wachstum",
            "CNA": "Wachstum mit β-Hämolyse"
        },
        "Fall 3": {
            "COS": "Graue Kolonien",
            "MAC": "Rosa Kolonien (Laktose+)",
            "CNA": "Kein Wachstum"
        },
        "Fall 4": {
            "COS": "Kein Wachstum",
            "MAC": "Kein Wachstum",
            "CNA": "Kein Wachstum"
        },
        "Fall 5": {
            "COS": "Weisse Kolonien ohne Hämolyse",
            "MAC": "Kein Wachstum",
            "CNA": "Wachstum ohne Hämolyse"
        },
        "Fall 6": {
            "COS": "Cremige, weissliche Kolonien",
            "MAC": "Kein Wachstum",
            "CNA": "Kaum oder kein Wachstum"
        }
    }
    
    plate = st.session_state.get("selected_plate")

    if plate is not None:
        image_path = plate_images[case][plate]
        text = plate_text[case][plate]
        mt = micro_tests[case]

        st.markdown("## 🧫 Wachstum auf der ausgewählten Platte")

        st.markdown(f"""
        <div class="result-card">
            <h3>🔎 Ausgewählte Platte: {plate}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.image(image_path, use_container_width=True)
        st.info(text)

        st.subheader("Mikrobiologische Schnelltests")

        st.markdown(f"""
        <div class="result-card">
            <b>Katalase:</b> {mt.get("Katalase", "nicht durchgeführt/keine Angabe")}<br>
            <b>Koagulase:</b> {mt.get("Koagulase", "nicht durchgeführt/keine Angabe")}<br>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")

        st.subheader("🧠 Interpretation der Agarplatten")
        for hint in interpret_micro(mt):
            st.markdown(f'<div class="hint-card">{hint}</div>', unsafe_allow_html=True)

        st.write("---")

        # Laborjournal der Agarplattenbefunde
        if st.button("📓 Befunde ins Laborjournal übernehmen", key=f"journal_agar_{case}"):

            if "Kultur & Tests" not in st.session_state.lab_journal:
                st.session_state.lab_journal["Kultur & Tests"] = []

            neue_infos = []

            for aktuelle_platte in ["COS", "MAC", "CNA"]:
                platten_text = plate_text[case][aktuelle_platte]
                neue_infos.append(f"Platte {aktuelle_platte}: {platten_text}")

            neue_infos.append(
                f"Schnelltests: Kat({mt.get('Katalase', 'nicht durchgeführt/keine Angabe')}), "
                f"Koag({mt.get('Koagulase', 'nicht durchgeführt/keine Angabe')})"
            )

            for info in neue_infos:
                if info not in st.session_state.lab_journal["Kultur & Tests"]:
                    st.session_state.lab_journal["Kultur & Tests"].append(info)

            st.success("✅ Alle Agar-Befunde wurden ins Journal eingetragen!")

    else:
        st.markdown("""
        <div class="hint-card">
            Wähle zuerst eine Platte aus, damit Wachstum, Schnelltests und Interpretation angezeigt werden.
        </div>
        """, unsafe_allow_html=True)
# -------------------------
# MIKROSKOP SCREEN
# -------------------------
elif st.session_state.screen == "mikroskop":
    case = st.session_state.case

    if st.button("← Zurück zum Labor", key=f"back_from_mic_{case}"):
        st.session_state.screen = "lab"
        st.rerun()

    st.markdown("""
    <div class="screen-box">
        <h1 style="text-align:center;">🔬 Mikroskop</h1>
        <p style="text-align:center;">Beobachte die Probe und führe danach die Gram-Färbung durch.</p>
    </div>
    """, unsafe_allow_html=True)


    # GLÜHBIRNE / HILFE SEKTION
    with st.expander("💡 Wissen: Warum färben wir Bakterien?", expanded=False):
        st.markdown("""
        ### 🔬 Die Gram-Färbung
        Bakterien sind unter dem Mikroskop fast farblos. Die Gram-Färbung ist der wichtigste erste Schritt der Diagnose:
        
        1.  **Gram-positiv (Blau/Violett):** Diese Bakterien haben eine dicke Zellwand, die den Farbstoff festhält.
        2.  **Gram-negativ (Rot/Pink):** Diese haben eine dünne Wand und eine zusätzliche Fettschicht. Der blaue Farbstoff wird ausgewaschen und sie werden mit Safranin gegengefärbt.
        
        **Formen:** Wir achten auch auf die Form (**Kokken** = Kügelchen, **Stäbchen**) und die Anordnung (**Haufen** wie Weintrauben oder **Ketten**).
        """)

    st.subheader("🎮 Gram-Färbung Mini-Spiel")
    st.write("Wähle die Schritte in der richtigen Reihenfolge:")

    # Vier Spalten für die Gram-Färbungsschritte
    c1, c2, c3, c4 = st.columns(4)

    # Gram-Färbungsschritte mit Emojis und Beschriftungen
    with c3:
        st.markdown("""
        <div class="gram-step-card">
            <span class="big-emoji">🟣</span>
            <div class="gram-step-title">Kristallviolett</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Wählen", key=f"cv_{case}"):
            st.session_state.gram_steps.append("Kristallviolett")
            st.rerun()

    with c1:
        st.markdown("""
        <div class="gram-step-card">
            <span class="big-emoji">🧴</span>
            <div class="gram-step-title">Lugol</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Wählen", key=f"lugol_{case}"):
            st.session_state.gram_steps.append("Lugol")
            st.rerun()

    with c4:
        st.markdown("""
        <div class="gram-step-card">
            <span class="big-emoji">💧</span>
            <div class="gram-step-title">Alkohol</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Wählen", key=f"alk_{case}"):
            st.session_state.gram_steps.append("Alkohol")
            st.rerun()

    with c2:
        st.markdown("""
        <div class="gram-step-card">
            <span class="big-emoji">🩷</span>
            <div class="gram-step-title">Safranin</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Wählen", key=f"saf_{case}"):
            st.session_state.gram_steps.append("Safranin")
            st.rerun()

    # Anzeige der aktuellen Reihenfolge und Reset-Button
    col_a, col_b = st.columns([3, 1])

    with col_a:
        st.markdown(f"""
        <div class="hint-card">
        <b>Deine Reihenfolge:</b> {" → ".join(st.session_state.gram_steps) if st.session_state.gram_steps else "Noch keine Schritte gewählt."}
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        if st.button("🔄 Reset", key=f"reset_gram_{case}"):
            reset_gram_game()
            st.session_state.gram_done = False
            st.rerun()

    # Sobald 4 Schritte gewählt wurden, wird die Reihenfolge überprüft und das Ergebnis angezeigt
    if len(st.session_state.gram_steps) == 4 and st.session_state.gram_result is None:
        correct_order = ["Kristallviolett", "Lugol", "Alkohol", "Safranin"]

        if st.session_state.gram_steps == correct_order:
            st.session_state.gram_result = microscope_info[case]["gram_type"]
            st.session_state.gram_done = True
        else:
            st.session_state.gram_result = "Reihenfolge nicht korrekt"
            st.session_state.gram_done = False

    if st.session_state.gram_result:
        if st.session_state.gram_result == "Reihenfolge nicht korrekt":
            st.error("❌ Die Reihenfolge war nicht korrekt. Versuch es nochmals.")
        else:
            st.success(f"✅ Ergebnis der Gram-Färbung: {st.session_state.gram_result}")

    if st.session_state.gram_done:
        st.image(
            microscope_info[case]["image"],
            caption="Mikroskopischer Befund",
            use_container_width=True
        )
        # Interpretationstexte basierend auf dem Fall
        st.markdown(f"""
        <div class="hint-card">
        <b>🧪 {microscope_info[case]["sample"]}</b>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="hint-card">
        🔬 Führe zuerst die Gram-Färbung korrekt durch, damit das Präparat sichtbar wird.
        </div>
        """, unsafe_allow_html=True)

    st.write("---")

    st.subheader("🧠 Interpretation des Mikroskops")
    
    st.markdown(f"""
    <div class="result-card">
        {microscope_info[case]["view"]}
    </div>
    """, unsafe_allow_html=True)

    st.write("---")

    # Laborjournal der Mikroskopbefunde
    if st.button("📓 Mikroskop-Befund ins Laborjournal übernehmen", key=f"journal_micro_{case}"):
        
        if "Mikroskop" not in st.session_state.lab_journal:
            st.session_state.lab_journal["Mikroskop"] = []

        if st.session_state.gram_result and st.session_state.gram_result != "Reihenfolge nicht korrekt":
            st.session_state.lab_journal["Mikroskop"].append(
                f"{microscope_info[case]['view']}"
            )
            st.session_state.lab_journal["Mikroskop"].append(
                f"Gram-Ergebnis: {st.session_state.gram_result}"
            )
            st.success("✅ Mikroskop-Befund wurde ins Journal übernommen!")
        else:
            st.warning("Bitte führe zuerst die Gram-Färbung korrekt durch.")

# -------------------------
# BLUTANALYSE SCREEN
# -------------------------
elif st.session_state.screen == "blutbild":
    case = st.session_state.case

    if st.button("← Zurück zum Labor", key=f"back_from_blood_{case}"):
        st.session_state.screen = "lab"
        st.rerun()

    st.markdown("""
    <div class="screen-box">
        <h1 style="text-align:center;">🩸 Blutanalyse</h1>
        <p style="text-align:center;">Beurteile die Blutwerte und das Differentialblutbild.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="path-card">
    🧪 <b>Hinweis:</b> Achte auf erhöhte Entzündungswerte und Veränderungen im Differentialblutbild.
    </div>
    """, unsafe_allow_html=True)

    # Glühbrine, mit Nebeninfos
    with st.expander("💡 Wissen: Was bedeuten diese Blutwerte?", expanded=False):
        st.markdown("""
        ### 🩸 Entzündungsmarker im Check
        *   **CRP (C-reaktives Protein):** Ein allgemeiner Alarmwert. Er steigt bei fast jeder Entzündung an. Werte über 100 mg/L deuten oft auf eine schwere bakterielle Infektion hin.
        *   **PCT (Procalcitonin):** Der "Spezialist" für Bakterien. Ist PCT hoch, ist eine bakterielle Infektion (oder sogar eine Sepsis) sehr wahrscheinlich. Bei Viren bleibt PCT meist niedrig.
        *   **Leukozyten:** Die "Polizei" des Körpers. Viel Arbeit (Infektion) = Viele Polizisten (hohe Werte).
        *   **Differentialblutbild:** Hier schauen wir, *welche* Polizisten da sind. **Neutrophile** kämpfen gegen Bakterien, **Lymphozyten** eher gegen Viren, **Eosinophile** gegen Parasiten.
        """)

    st.markdown("---")

    st.subheader("⚙️ Analyseablauf")

# Simulation der Blutanalyse mit Fortschrittsbalken und Statusanzeigen
    if not st.session_state.blood_loaded:
        st.markdown("""
        <div class="machine-box">
            🧪 <b>Probenannahme:</b><br>
            Die EDTA-Blutprobe ist eingetroffen und wartet auf die Bearbeitung im Labor.
        </div>
        """, unsafe_allow_html=True)

        if st.button("🧪 Probe ins Analysegerät laden", key=f"load_blood_{case}"):
            st.session_state.blood_loaded = True
            st.rerun()

    if st.session_state.blood_loaded:
        st.markdown("""
        <div class="machine-box">
            ✅ <b>Probe geladen:</b><br>
            Wähle jetzt, welche Analysegeräte verwendet werden sollen.
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class="analyzer-card">
                <div class="analyzer-title">🧪 Chemie-Analyzer</div>
                <div class="analyzer-sub">
                    Misst Entzündungsparameter und Basiswerte wie CRP, PCT und Leukozyten.
                </div>
                <div class="analyzer-status">
                    {"✅ abgeschlossen" if st.session_state.chem_done else "⏳ bereit"}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.chem_done:
                if st.button("▶️ Chemie-Analyse starten", key=f"start_chem_{case}", use_container_width=True):
                    with st.spinner("🧪 Chemie-Analyzer läuft..."):
                        progress = st.progress(0)
                        for i in range(100):
                            time.sleep(0.015)
                            progress.progress(i + 1)

                    st.session_state.chem_done = True
                    st.rerun()

        with col2:
            st.markdown(f"""
            <div class="analyzer-card">
                <div class="analyzer-title">🩸 Hämatologie-Analyzer</div>
                <div class="analyzer-sub">
                    Erstellt das Differentialblutbild und zeigt Veränderungen der Zellpopulationen.
                </div>
                <div class="analyzer-status">
                    {"✅ abgeschlossen" if st.session_state.hema_done else "⏳ bereit"}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if not st.session_state.hema_done:
                if st.button("▶️ Hämatologie-Analyse starten", key=f"start_hema_{case}", use_container_width=True):
                    with st.spinner("🩸 Hämatologie-Analyzer läuft..."):
                        progress = st.progress(0)
                        for i in range(100):
                            time.sleep(0.015)
                            progress.progress(i + 1)

                    st.session_state.hema_done = True
                    st.rerun()

        values = blood_values.get(case, {})
        diff = blood_diff.get(case, {})
        
    st.markdown("---")
    # Anzeige der Ergebnisse mit Ampelfarben und Interpretation
    if st.session_state.chem_done:
        st.subheader("🧪 Chemie-Resultate")

        for param, val in values.items():
            if param in REF:
                low, high = REF[param]
                flag_symbol = flag(val, low, high)
                st.markdown(f"""
                <div class="result-card">
                {param}: <b>{val}</b> (Ref: {low}–{high}) <b>{flag_symbol}</b>
                </div>
                """, unsafe_allow_html=True)

    if st.session_state.hema_done:
        st.subheader("🩸 Hämatologie-Resultate")

        for param, val in diff.items():
            if param in REF_BLOOD_DIFF:
                low, high = REF_BLOOD_DIFF[param]
                flag_symbol = flag(val, low, high)
                st.markdown(f"""
                <div class="result-card">
                {param}: <b>{val}</b> (Ref: {low}–{high}) <b>{flag_symbol}</b>
                </div>
                """, unsafe_allow_html=True)
    # Interpretation der Ergebnisse basierend auf den Werten und dem Fall
    if st.session_state.chem_done or st.session_state.hema_done:
        st.write("---")
        st.subheader("🧠 Interpretation der Blutanalyse")

        if st.session_state.hema_done:
            for h in interpret_blood(diff):
                st.markdown(f"""<div class="hint-card">{h}</div>""", unsafe_allow_html=True)

        if st.session_state.chem_done:
            if "CRP" in values and values["CRP"] > 100:
                st.markdown("""<div class="hint-card">🧠 CRP stark erhöht → deutlicher Entzündungsprozess.</div>""", unsafe_allow_html=True)
            if "PCT" in values and values["PCT"] > 0.5:
                st.markdown("""<div class="hint-card">🧠 PCT erhöht → Hinweis auf bakterielle Infektion möglich.</div>""", unsafe_allow_html=True)
            if "Leukos" in values and values["Leukos"] > 10:
                st.markdown("""<div class="hint-card">🧠 Leukozyten erhöht → passt zu einer Entzündungsreaktion.</div>""", unsafe_allow_html=True)
        st.write("---")
        # Zusammenfassung und Möglichkeit, die Befunde ins Laborjournal zu übernehmen
        if st.session_state.chem_done and st.session_state.hema_done:
            st.markdown("""
            <div class="analysis-step">
            🌟 Beide Geräte haben die Probe erfolgreich ausgewertet. Jetzt kannst du die Befunde ins Laborjournal übernehmen.
            </div>
            """, unsafe_allow_html=True)

            st.markdown("---")
            # Laborjournal der Blutanalysebefunde
            if st.button("📓 Ins Laborjournal übernehmen", key=f"journal_blood_{case}"):
                neue_eintraege = []

                if st.session_state.chem_done:
                    werte_liste = [f"{p}: {v}" for p, v in values.items()]
                    neue_eintraege.append("🧪 Chemie: " + " | ".join(werte_liste))

                if st.session_state.hema_done:
                    diff_liste = [f"{p}: {v}" for p, v in diff.items()]
                    neue_eintraege.append("🩸 Hämatologie: " + " | ".join(diff_liste))

                    for hinweis in interpret_blood(diff):
                        neue_eintraege.append(hinweis)

                if "Blutanalyse" not in st.session_state.lab_journal:
                    st.session_state.lab_journal["Blutanalyse"] = []

                for eintrag in neue_eintraege:
                    if eintrag not in st.session_state.lab_journal["Blutanalyse"]:
                        st.session_state.lab_journal["Blutanalyse"].append(eintrag)

                st.success("✅ Komplette Blutanalyse wurde ins Journal übernommen!")