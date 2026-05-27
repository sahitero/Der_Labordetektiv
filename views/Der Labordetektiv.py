import streamlit as st
import pandas as pd
import time

# =====================================================================
# 🛠️ DATEN & FUNKTIONEN AUS DEM "FUNCTIONS"-ORDNER ZURÜCKRUFEN
# =====================================================================
from functions.cases_data import (
    cases, microscope_info, micro_tests, plate_text, 
    blood_values, blood_diff, REF, REF_BLOOD_DIFF, solutions, DIAG_CHOICES
)
from functions.helpers import (
    get_base64, flag, interpret_blood, interpret_micro, reset_gram_game
)

# =====================================================================
# 🎨 1) CSS STYLES & HINTERGRÜNDE
# =====================================================================

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
div.stButton > button:hover p,
div.stButton > button:hover span,
div.stButton > button:hover div {
    color: white !important;
}

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

.header-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
}

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

.header-score {
    background-color: #E6F7FF;
    border-radius: 999px;
    padding: 6px 12px;
    display: inline-block;
    font-weight: 800;
    color: #4B0082 !important;
    box-shadow: 0px 6px 16px rgba(0,0,0,0.08);
}

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

.station-icon {
    font-size: 34px;
    margin-bottom: 8px;
}

.station-title {
    font-size: 20px;
    font-weight: 900;
    line-height: 1.2;
    margin-bottom: 10px;
    color: #4B0082 !important;
}

.station-sub {
    font-size: 15px;
    line-height: 1.65;
    margin-bottom: 14px;
    color: #6A3FA0 !important;
}

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

.screen-box {
    background-color: #FFF0F7;
    border-radius: 28px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.08);
}

.plate-card {
    background: #FFE4F1;
    width: 180px;
    height: 180px;
    margin: 0 auto 12px auto;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 56px;
    border-radius: 999px;
    box-shadow: inset 0 0 0 8px rgba(255,255,255,0.4), 0px 8px 18px rgba(0,0,0,0.08);
}

.plate-label {
    text-align: center;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 8px;
    color: #4B0082 !important;
}

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

.big-emoji {
    font-size: 44px;
    display: block;
    margin-bottom: 10px;
}

.path-card {
    background: #FFF7D6;
    border-radius: 18px;
    padding: 12px 14px;
    margin-top: 10px;
    margin-bottom: 14px;
    color: #4B0082 !important;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
}

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

.floating-item {
    position: fixed;
    z-index: 0;
    pointer-events: none;
    font-size: 52px;
    opacity: 0.22;
    animation: floaty 8s ease-in-out infinite;
}

.item1 { top: 8%; left: 5%; animation-delay: 0s; }
.item2 { top: 22%; right: 10%; animation-delay: 2s; }
.item3 { bottom: 14%; left: 18%; animation-delay: 1s; }
.item4 { bottom: 28%; right: 8%; animation-delay: 3s; }
.item5 { top: 55%; left: 42%; animation-delay: 4s; }
.item6 { top: 72%; right: 30%; animation-delay: 5s; }

@keyframes floaty {
    0% { transform: translateY(0px) rotate(0deg) scale(1); }
    50% { transform: translateY(-20px) rotate(8deg) scale(1.08); }
    100% { transform: translateY(0px) rotate(0deg) scale(1); }
}

/* Expander / Dropdown Styling (Rosa mit Umrandung) */
div[data-testid="stExpander"] {
    background-color: #EFDCE6 !important;
    border-radius: 20px !important;
    border: 2px solid #E7A7C4 !important;
    overflow: hidden !important;
}

div[data-testid="stExpander"] summary {
    background-color: #EFDCE6 !important;
    border-radius: 20px !important;
}

div[data-testid="stExpander"] div[role="region"] {
    background-color: #EFDCE6 !important;
    padding: 15px !important;
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

# =====================================================================
# 💾 2) SESSION STATE INITIALISIERUNG
# =====================================================================
if "screen" not in st.session_state:
    st.session_state.screen = "home"

if "score" not in st.session_state:
    st.session_state.score = 0

if "feedback" not in st.session_state:
    st.session_state.feedback = None

default_unlocked = {
    "Mikroskop": False,
    "Kultur & Tests": False,
    "Blutanalyse": False,
}

if "unlocked" not in st.session_state or set(st.session_state.unlocked.keys()) != set(default_unlocked.keys()):
    st.session_state.unlocked = default_unlocked.copy()

if "case" not in st.session_state:
    st.session_state.case = "Fall 1"

if "selected_plate" not in st.session_state:
    st.session_state.selected_plate = None

if "gram_steps" not in st.session_state:
    st.session_state.gram_steps = []

if "gram_result" not in st.session_state:
    st.session_state.gram_result = None

if "selected_blood_param" not in st.session_state:
    st.session_state.selected_blood_param = None

default_lab_journal = {
    "Mikroskop": [],
    "Kultur & Tests": [],
    "Blutanalyse": []
}

if "lab_journal" not in st.session_state or set(st.session_state.lab_journal.keys()) != set(default_lab_journal.keys()):
    st.session_state.lab_journal = {key: value.copy() for key, value in default_lab_journal.items()}

if "show_help" not in st.session_state:
    st.session_state.show_help = False

if "gram_done" not in st.session_state:
    st.session_state.gram_done = False

if "blood_started" not in st.session_state:
    st.session_state.blood_started = False

if "blood_done" not in st.session_state:
    st.session_state.blood_done = False

if "blood_loaded" not in st.session_state:
    st.session_state.blood_loaded = False

if "chem_done" not in st.session_state:
    st.session_state.chem_done = False

if "hema_done" not in st.session_state:
    st.session_state.hema_done = False

if "scored_cases" not in st.session_state:
    st.session_state.scored_cases = {}

# =====================================================================
# ⚙️ 3) FALL-STEUERUNG
# =====================================================================
if "case" in st.session_state and isinstance(st.session_state.case, str):
    if " - " in st.session_state.case:
        st.session_state.case = st.session_state.case.split(" - ")[0]

if "case" not in st.session_state or st.session_state.case not in cases:
    st.session_state.screen = "level"
else:
    case = st.session_state.case
    data = cases[case]

# =====================================================================
# 🖥️ 4) DIE APPSCREENS
# =====================================================================

# -------------------------
# HOME SCREEN
# -------------------------
if st.session_state.screen == "home":
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

    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center;">
    <h1 style="display: inline-block; background-color: rgba(255,255,255,0.8); padding: 10px 30px; border-radius: 15px; font-size: 65px; color: #4B0082; font-weight: 900; margin-bottom: 20px;">
    Der Labordetektiv
    </h1>
    <p style="font-size: 28px; color: #5A2D82; font-weight: 500;">Willkommen im biomedizinischen Labor!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f'<div style="text-align: center; font-size: 28px; font-weight: 700; color: #4B0082; margin-top: 20px;">Score: {st.session_state.score}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

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
    st.markdown(f'<div class="hint-card">🎯 <b>Score:</b> {st.session_state.score}</div>', unsafe_allow_html=True)

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
                st.session_state.lab_journal = {"Mikroskop": [], "Blutanalyse": [], "Kultur & Tests": []}
                st.session_state.unlocked = {"Mikroskop": False, "Blutanalyse": False, "Kultur & Tests": False}
                st.session_state.screen = "lab"
                st.session_state.feedback = None
                st.session_state.selected_plate = None
                reset_gram_game()
                st.session_state.gram_done = False
                st.session_state.blood_started = False
                st.session_state.blood_done = False
                st.session_state.blood_loaded = False
                st.session_state.hema_done = False
                st.session_state.chem_done = False
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

    if st.button("← Fallauswahl", key="back_to_lvl"):
        st.session_state.screen = "level"
        st.rerun()

    st.markdown(f'<div class="header-row"><div class="header-pill">🧪 {case}</div><div class="header-score">🎯 Score: {st.session_state.score}</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="cute-card"><h2>🩺 Patientenfall</h2><p style="font-style: italic; font-size: 20px; line-height: 1.6;">"{data["story"]}"</p><hr><p style="font-size: 17px;"><b>Patient:</b> {data["name"]} ({data["age"]} Jahre, {data["sex"]})</p><p style="font-size: 17px;"><b>Symptome:</b> {data["symptoms"]}</p></div>', unsafe_allow_html=True)

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
        diag = st.selectbox("Was ist deine Diagnose?", ["— bitte wählen —"] + DIAG_CHOICES, key=f"select_diag_{case}")
        
        if st.button("✅ Diagnose abgeben", key=f"submit_btn_{case}", use_container_width=True):
            if diag != "— bitte wählen —":
                feedback_key = f"feedback_{case}"
                if case not in st.session_state.scored_cases:
                    if diag == solutions[case]:
                        st.session_state.score += 10
                        st.session_state[feedback_key] = {"type": "success", "msg": "✅ Richtig! +10 Punkte"}
                        st.balloons() 
                    else:
                        st.session_state.score -= 5
                        st.session_state[feedback_key] = {"type": "error", "msg": f"❌ Falsch! Lösung: {solutions[case]}"}
                    st.session_state.scored_cases[case] = True
            else:
                st.warning("Bitte wähle zuerst eine Diagnose aus!")

        feedback_key = f"feedback_{case}"
        if feedback_key in st.session_state:
            fb = st.session_state[feedback_key]
            if fb["type"] == "success": st.success(fb["msg"])
            elif fb["type"] == "error": st.error(fb["msg"])

# -------------------------
# AGAR SCREEN
# -------------------------
elif st.session_state.screen == "agar":
    case = st.session_state.case
    if st.button("← Zurück zum Labor", key=f"back_from_agar_{case}"):
        st.session_state.screen = "lab"
        st.rerun()

    st.markdown('<div class="screen-box"><h1 style="text-align:center;">🧫 Kultur & Tests</h1><p style="text-align:center;">Wähle eine Agarplatte aus und kombiniere das Wachstum mit Schnelltests.</p></div>', unsafe_allow_html=True)

    with st.expander("💡 Wissen: Was verraten uns diese Agarplatten?", expanded=False):
        st.markdown("""
        ### 🧫 Die Welt der Nährmedien
        Um Bakterien zu identifizieren, lassen wir sie auf verschiedenen "Tellern" (Agarplatten) wachsen:
        
        * **COS (Kochblutagar mit Schafsblut):** Ein Universalmedium. Fast alles wächst hier. Besonders wichtig: Hier sieht man die **Hämolyse** (wie die Bakterien rote Blutkörperchen zerstören).
        * **MAC (MacConkey-Agar):** Ein Selektivmedium für **gramnegative Bakterien** (z.B. Darmbakterien). Es zeigt auch, ob die Bakterien Zucker (Laktose) vergären können.
        * **CNA (Colistin-Nalidixinsäure-Agar):** Ein Selektivmedium, auf dem fast nur **grampositive Bakterien** wachsen.
        """)

    st.subheader("Agarplatte auswählen")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="plate-card">🧫</div><div class="plate-label">COS</div>', unsafe_allow_html=True)
        if st.button("COS öffnen", key=f"plate_cos_{case}"): st.session_state.selected_plate = "COS"; st.rerun()
    with col2:
        st.markdown('<div class="plate-card">🧫</div><div class="plate-label">MAC</div>', unsafe_allow_html=True)
        if st.button("MAC öffnen", key=f"plate_mac_{case}"): st.session_state.selected_plate = "MAC"; st.rerun()
    with col3:
        st.markdown('<div class="plate-card">🧫</div><div class="plate-label">CNA</div>', unsafe_allow_html=True)
        if st.button("CNA öffnen", key=f"plate_cna_{case}"): st.session_state.selected_plate = "CNA"; st.rerun()

    plate_images = {
        "Fall 1": {"COS": "images/fall1_cos.png", "MAC": "images/fallleer_mac.png", "CNA": "images/fall1_cna.png"},
        "Fall 2": {"COS": "images/fall2_cos.png", "MAC": "images/fallleer_mac.png", "CNA": "images/fall2_cna.png"},
        "Fall 3": {"COS": "images/fall3_cos.png", "MAC": "images/fall3_mac.png", "CNA": "images/fallleer_mac.png"},
        "Fall 4": {"COS": "images/fallleer_cos.png", "MAC": "images/fallleer_mac.png", "CNA": "images/fallleer_mac.png"},
        "Fall 5": {"COS": "images/fall5_cos.png", "MAC": "images/fallleer_mac.png", "CNA": "images/fall5_cna.png"},
        "Fall 6": {"COS": "images/fall6_cos.png", "MAC": "images/fallleer_mac.png", "CNA": "images/fallleer_mac.png"}
    }

    plate = st.session_state.get("selected_plate")
    if plate is not None:
        image_path = plate_images[case][plate]
        text = plate_text[case][plate]
        mt = micro_tests[case]

        st.markdown(f'<div class="result-card"><h3>🔎 Ausgewählte Platte: {plate}</h3></div>', unsafe_allow_html=True)
        st.image(image_path, use_container_width=True)
        st.info(text)

        st.subheader("Mikrobiologische Schnelltests")
        st.markdown(f'<div class="result-card"><b>Katalase:</b> {mt.get("Katalase")}<br><b>Koagulase:</b> {mt.get("Koagulase")}</div>', unsafe_allow_html=True)

        st.subheader("🧠 Interpretation")
        for hint in interpret_micro(mt):
            st.markdown(f'<div class="hint-card">{hint}</div>', unsafe_allow_html=True)

        if st.button("📓 Befunde ins Laborjournal übernehmen", key=f"journal_agar_{case}"):
            if "Kultur & Tests" not in st.session_state.lab_journal: st.session_state.lab_journal["Kultur & Tests"] = []
            neue_infos = [f"Platte {p}: {plate_text[case][p]}" for p in ["COS", "MAC", "CNA"]]
            neue_infos.append(f"Schnelltests: Kat({mt.get('Katalase')}), Koag({mt.get('Koagulase')})")
            for info in neue_infos:
                if info not in st.session_state.lab_journal["Kultur & Tests"]: st.session_state.lab_journal["Kultur & Tests"].append(info)
            st.success("✅ Alle Agar-Befunde wurden ins Journal eingetragen!")
    else:
        st.markdown('<div class="hint-card">Wähle zuerst eine Platte aus, damit Wachstum, Schnelltests und Interpretation angezeigt werden.</div>', unsafe_allow_html=True)

# -------------------------
# MIKROSKOP SCREEN
# -------------------------
elif st.session_state.screen == "mikroskop":
    case = st.session_state.case
    if st.button("← Zurück zum Labor", key=f"back_from_mic_{case}"):
        st.session_state.screen = "lab"
        st.rerun()

    st.markdown('<div class="screen-box"><h1 style="text-align:center;">🔬 Mikroskop</h1><p style="text-align:center;">Beobachte die Probe und führe danach die Gram-Färbung durch.</p></div>', unsafe_allow_html=True)

    with st.expander("💡 Wissen: Warum färben wir Bakterien?", expanded=False):
        st.markdown("""
        ### 🔬 Die Gram-Färbung
        Bakterien sind unter dem Mikroskop fast farblos. Die Gram-Färbung ist der wichtigste erste Schritt der Diagnose:
        
        1. **Gram-positiv (Blau/Violett):** Diese Bakterien haben eine dicke Zellwand, die den Farbstoff festhält.
        2. **Gram-negativ (Rot/Pink):** Diese haben eine dünne Wand. Der blaue Farbstoff wird ausgewaschen und sie werden gegengefärbt.
        """)

    st.subheader("🎮 Gram-Färbung Mini-Spiel")
    c1, c2, c3, c4 = st.columns(4)
    with c3:
        st.markdown('<div class="gram-step-card"><span class="big-emoji">🟣</span><div class="gram-step-title">Kristallviolett</div></div>', unsafe_allow_html=True)
        if st.button("Wählen", key=f"cv_{case}"): st.session_state.gram_steps.append("Kristallviolett"); st.rerun()
    with c1:
        st.markdown('<div class="gram-step-card"><span class="big-emoji">🧴</span><div class="gram-step-title">Lugol</div></div>', unsafe_allow_html=True)
        if st.button("Wählen", key=f"lugol_{case}"): st.session_state.gram_steps.append("Lugol"); st.rerun()
    with c4:
        st.markdown('<div class="gram-step-card"><span class="big-emoji">💧</span><div class="gram-step-title">Alkohol</div></div>', unsafe_allow_html=True)
        if st.button("Wählen", key=f"alk_{case}"): st.session_state.gram_steps.append("Alkohol"); st.rerun()
    with c2:
        st.markdown('<div class="gram-step-card"><span class="big-emoji">🩷</span><div class="gram-step-title">Safranin</div></div>', unsafe_allow_html=True)
        if st.button("Wählen", key=f"saf_{case}"): st.session_state.gram_steps.append("Safranin"); st.rerun()

    col_a, col_b = st.columns([3, 1])
    with col_a:
        st.markdown(f'<div class="hint-card"><b>Deine Reihenfolge:</b> {" → ".join(st.session_state.gram_steps) if st.session_state.gram_steps else "Noch keine Schritte gewählt."}</div>', unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 Reset", key=f"reset_gram_{case}"):
            reset_gram_game()
            st.session_state.gram_done = False
            st.rerun()

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
        st.image(microscope_info[case]["image"], caption="Mikroskopischer Befund", use_container_width=True)
        st.markdown(f'<div class="hint-card"><b>🧪 {microscope_info[case]["sample"]}</b></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hint-card">🔬 Führe zuerst die Gram-Färbung korrekt durch, damit das Präparat sichtbar wird.</div>', unsafe_allow_html=True)

    st.subheader("🧠 Interpretation des Mikroskops")
    st.markdown(f'<div class="result-card">{microscope_info[case]["view"]}</div>', unsafe_allow_html=True)

    if st.button("📓 Mikroskop-Befund ins Laborjournal übernehmen", key=f"journal_micro_{case}"):
        if "Mikroskop" not in st.session_state.lab_journal: st.session_state.lab_journal["Mikroskop"] = []
        if st.session_state.gram_result and st.session_state.gram_result != "Reihenfolge nicht korrekt":
            st.session_state.lab_journal["Mikroskop"].append(f"{microscope_info[case]['view']}")
            st.session_state.lab_journal["Mikroskop"].append(f"Gram-Ergebnis: {st.session_state.gram_result}")
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

    st.markdown('<div class="screen-box"><h1 style="text-align:center;">🩸 Blutanalyse</h1><p style="text-align:center;">Beurteile die Blutwerte und das Differentialblutbild.</p></div>', unsafe_allow_html=True)

    # 💡 KORREKTUR: Wissen-Sektion wieder eingefügt
    with st.expander("💡 Wissen: Was bedeuten diese Blutwerte?", expanded=False):
        st.markdown("""
        ### 🩸 Entzündungsmarker im Check
        * **CRP (C-reaktives Protein):** Allgemeiner Alarmwert. Werte über 100 mg/L deuten oft auf schwere bakterielle Infektionen hin.
        * **PCT (Procalcitonin):** Spezialist für Bakterien. Erhöht bei bakteriellen Infektionen oder Sepsis.
        * **Leukozyten:** Die Abwehrzellen. Erhöht bei Entzündungen.
        * **Differentialblutbild:** Aufteilung der Abwehrzellen (**Neutrophile** gegen Bakterien, **Lymphozyten** gegen Viren, **Eosinophile** gegen Parasiten).
        """)

    if not st.session_state.blood_loaded:
        st.markdown('<div class="machine-box">🧪 <b>Probenannahme:</b><br>Die EDTA-Blutprobe ist eingetroffen und wartet auf die Bearbeitung im Labor.</div>', unsafe_allow_html=True)
        if st.button("🧪 Probe ins Analysegerät laden", key=f"load_blood_{case}"):
            st.session_state.blood_loaded = True
            st.rerun()

    if st.session_state.blood_loaded:
        st.markdown('<div class="machine-box">✅ <b>Probe geladen:</b><br>Wähle jetzt, welche Analysegeräte verwendet werden sollen.</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            # 💡 KORREKTUR: Exakte Analyzer-Benennung wiederhergestellt
            st.markdown(f'<div class="analyzer-card"><div class="analyzer-title">🧪 Chemie-Analyzer</div><div class="analyzer-sub">Misst Entzündungsparameter und Basiswerte wie CRP, PCT und Leukozyten.</div><div class="analyzer-status">{"✅ abgeschlossen" if st.session_state.chem_done else "⏳ bereit"}</div></div>', unsafe_allow_html=True)
            if not st.session_state.chem_done and st.button("▶️ Chemie-Analyse starten", key=f"start_chem_{case}", use_container_width=True):
                with st.spinner("🧪 Chemie-Analyzer läuft..."):
                    p = st.progress(0)
                    for i in range(100): time.sleep(0.015); p.progress(i + 1)
                st.session_state.chem_done = True
                st.rerun()

        with col2:
            # 💡 KORREKTUR: Exakte Analyzer-Benennung wiederhergestellt
            st.markdown(f'<div class="analyzer-card"><div class="analyzer-title">🩸 Hämatologie-Analyzer</div><div class="analyzer-sub">Erstellt das Differentialblutbild und zeigt Veränderungen der Zellpopulationen.</div><div class="analyzer-status">{"✅ abgeschlossen" if st.session_state.hema_done else "⏳ bereit"}</div></div>', unsafe_allow_html=True)
            if not st.session_state.hema_done and st.button("▶️ Hämatologie-Analyse starten", key=f"start_hema_{case}", use_container_width=True):
                with st.spinner("🩸 Hämatologie-Analyzer läuft..."):
                    p = st.progress(0)
                    for i in range(100): time.sleep(0.015); p.progress(i + 1)
                st.session_state.hema_done = True
                st.rerun()

        values = blood_values.get(case, {})
        diff = blood_diff.get(case, {})

        if st.session_state.chem_done:
            st.subheader("🧪 Chemie-Resultate")
            for param, val in values.items():
                if param in REF:
                    low, high = REF[param]
                    st.markdown(f'<div class="result-card">{param}: <b>{val}</b> (Ref: {low}–{high}) <b>{flag(val, low, high)}</b></div>', unsafe_allow_html=True)

        if st.session_state.hema_done:
            st.subheader("🩸 Hämatologie-Resultate")
            for param, val in diff.items():
                if param in REF_BLOOD_DIFF:
                    low, high = REF_BLOOD_DIFF[param]
                    st.markdown(f'<div class="result-card">{param}: <b>{val}</b> (Ref: {low}–{high}) <b>{flag(val, low, high)}</b></div>', unsafe_allow_html=True)

        if st.session_state.chem_done or st.session_state.hema_done:
            st.subheader("🧠 Interpretation der Blutanalyse")
            if st.session_state.hema_done:
                for h in interpret_blood(diff): st.markdown(f'<div class="hint-card">{h}</div>', unsafe_allow_html=True)
            if st.session_state.chem_done:
                if "CRP" in values and values["CRP"] > 100: st.markdown('<div class="hint-card">🧠 CRP stark erhöht → deutlicher Entzündungsprozess.</div>', unsafe_allow_html=True)
                if "PCT" in values and values["PCT"] > 0.5: st.markdown('<div class="hint-card">🧠 PCT erhöht → Hinweis auf bakterielle Infektion möglich.</div>', unsafe_allow_html=True)
                if "Leukos" in values and values["Leukos"] > 10: st.markdown('<div class="hint-card">🧠 Leukozyten erhöht → passt zu einer Entzündungsreaktion.</div>', unsafe_allow_html=True)

            if st.session_state.chem_done and st.session_state.hema_done:
                st.markdown('<div class="analysis-step">🌟 Beide Geräte haben die Probe erfolgreich ausgewertet. Jetzt kannst du die Befunde ins Laborjournal übernehmen.</div>', unsafe_allow_html=True)
                if st.button("📓 Ins Laborjournal übernehmen", key=f"journal_blood_{case}"):
                    if "Blutanalyse" not in st.session_state.lab_journal: st.session_state.lab_journal["Blutanalyse"] = []
                    neue = [f"🧪 Chemie: " + " | ".join([f"{p}: {v}" for p, v in values.items()])]
                    neue.append(f"🩸 Hämatologie: " + " | ".join([f"{p}: {v}" for p, v in diff.items()]))
                    for h in interpret_blood(diff): neue.append(h)
                    for e in neue:
                        if e not in st.session_state.lab_journal["Blutanalyse"]: st.session_state.lab_journal["Blutanalyse"].append(e)
                    st.success("✅ Komplette Blutanalyse wurde ins Journal übernommen!")