# functions/helpers.py
import base64
import streamlit as st

def get_base64(file_path):
    """Wandelt Bilder in Text um für CSS-Hintergründe."""
    try:
        with open(file_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def flag(value, low, high):
    """Setzt die Pfeile für zu hohe oder zu niedrige Laborwerte."""
    if value < low: return "↓"
    if value > high: return "↑"
    return "✓"

def interpret_blood(diff: dict) -> list[str]:
    """Interpretiert das Differentialblutbild."""
    hints = []
    neut = float(diff.get("Neutrophile (%)", 0))
    lymph = float(diff.get("Lymphozyten (%)", 0))
    eos = float(diff.get("Eosinophile (%)", 0))

    if neut >= 70: hints.append("Neutrophile ↑ spricht eher für bakterielle Ursache (akut)")
    if lymph >= 45: hints.append("Lymphozyten ↑ spricht eher für virale Ursache")
    if eos >= 6: hints.append("Eosinophile ↑ spricht für Parasiten oder Allergie")
    if not hints: hints.append("Differentialblutbild: kein klarer Hinweis → weitere Tests wichtig")
    return hints

def interpret_micro(mt: dict) -> list[str]:
    """Interpretiert die mikrobiologischen Schnelltests."""
    hints = []
    gram = mt.get("Gram", "").lower()
    kat = mt.get("Katalase", "").lower()
    koa = mt.get("Koagulase", "").lower()

    if "gram-positiv" in gram and "kokken" in gram and "haufen" in gram and "positiv" in kat:
        hints.append("Grampositive Kokken in Haufen + Katalase positiv = Staphylokokken")
        if "positiv" in koa: hints.append("Koagulase positiv = Hinweis auf Staphylococcus aureus")
        elif "negativ" in koa: hints.append("Koagulase negativ = eher Staphylococcus epidermidis")

    if "gram-positiv" in gram and "ketten" in gram and "negativ" in kat:
        hints.append("Grampositive Kokken in Ketten + Katalase negativ = Hinweis auf Streptokokken")

    if not hints: hints.append("Mikrotests: kein eindeutiger Shortcut = Kultur/ weitere Schritte beachten")
    return hints

def reset_gram_game():
    """Setzt das Gram-Färbungsspiel zurück."""
    st.session_state.gram_steps = []
    st.session_state.gram_result = None