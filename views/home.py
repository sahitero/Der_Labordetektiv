import streamlit as st

st.markdown("""
    <style>
    .stApp {
        background-color: #FFC0CB;
    }
    </style>
    """, unsafe_allow_html=True)
# -------------------------
# HOME SCREEN
# -------------------------

# Falls 'screen' noch nicht existiert, hier lokal initialisieren
if "screen" not in st.session_state:
    st.session_state.screen = "home"

if st.session_state.screen == "home":
    st.title("🔬 Der Labordetektiv")

    # Begrüßung mit Persona-Bezug
    st.markdown(f"""
    <div class="cute-card">
        <h3>Willkommen im Team! 🕵️‍♀️</h3>
        <p>In diesem Labor kombinieren wir Wissenschaft mit Spürsinn. Deine Aufgabe ist es, durch präzise Analysen die richtige Diagnose für unsere Patienten zu finden.</p>
    </div>
    """, unsafe_allow_html=True)

    # Spielablauf als schicke Spalten (User Experience)
    st.subheader("Dein Weg zur Diagnose")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="hint-card" style="min-height: 10px;">
        <b>1. Akte wählen</b><br>
        Suche dir einen der sechs spannenden Fälle aus.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="hint-card" style="min-height: 10px;">
        <b>2. Laborbesuch</b><br>
        Nutze Informationen von Mikroskop, Agarplatten und dem Blutbild.
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="hint-card" style="min-height: 10px;">
        <b>3. Rätsel lösen</b><br>
        Kombiniere die Befunde und stelle die Diagnose.
        </div>
        """, unsafe_allow_html=True)

    # Der zentrale Start-Button
    st.markdown("""
    <style>
    .stButton button {
        background-color: #FFD6E8;
        color: #4B0082 !important; 
        border-radius: 22px;
        border: none;
        padding: 0.6em 1.1em;
        font-weight: 700;           
    }
    </style>
    """, unsafe_allow_html=True)

    st.write("---")
    if st.button("Jetzt Ermittlung starten!", use_container_width=True):
        st.switch_page("views/Der Labordetektiv.py")

    # Autoren dezent im Footer
    st.write("---")
    with st.expander("👥 Das Team hinter dem Labordetektiv"):
        st.markdown("""
        * **Eronita Sahiti** (sahitero@students.zhaw.ch)
        * **Lilia Totila** (totillil@students.zhaw.ch)
        * **Lia Bütikofer** (buetilia@students.zhaw.ch)
        * **Vanessa Cakoncev** (cakonvan@students.zhaw.ch)
        """)