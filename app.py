import streamlit as st
import os

# --- CONFIGURAZIONE PAGINA ---
st.set_page_config(
    page_title="ReguAI-Pilot | Cerberus R&D",
    page_icon="🛡️",
    layout="wide"
)

# --- LOGICA DI ANALISI DETERMINISTICA (Simulazione AI) ---
def analyze_document_local(text, focus):
    text = text.lower()
    report = []
    risk_score = 1
    
    # 1. Dizionario di criticità per MiFID II
    mifid_keywords = {
        "costi": "⚠️ Sezione Costi: Verificare la trasparenza ex-ante secondo MiFID II.",
        "incentivi": "⚠️ Incentivi: Possibile conflitto di interesse rilevato (Inducements).",
        "adeguatezza": "✅ Adeguatezza: Menzionata la valutazione del profilo di rischio cliente.",
        "target market": "ℹ️ Target Market: Definizione del mercato di riferimento individuata."
    }
    
    # 2. Dizionario di criticità per AI Act
    ai_act_keywords = {
        "profilazione": "🔴 Rischio Alto: Rilevata attività di profilazione finanziaria automatizzata.",
        "biometrico": "🚫 Divieto: Riferimento a dati biometrici (Verificare conformità AI Act).",
        "trasparenza": "✅ Trasparenza: Il documento cita la spiegabilità dell'algoritmo.",
        "black box": "⚠️ Criticità: Possibile mancanza di sorveglianza umana rilevata."
    }

    selected_keywords = mifid_keywords if "MiFID" in focus else ai_act_keywords
    
    # Esecuzione analisi
    for key, val in selected_keywords.items():
        if key in text:
            report.append(val)
            risk_score += 1

    if not report:
        return "Nessuna criticità immediata rilevata nei pattern standard.", 1
    
    return "\n\n".join(report), min(risk_score, 5)

# --- INTERFACCIA UTENTE ---
st.title("🛡️ ReguAI-Pilot (Offline Version)")
st.caption("Boutique Compliance Engine by Cerberus R&D - Analisi Locale Strategica")

st.markdown("""
Questa versione di **ReguAI-Pilot** utilizza un motore di analisi euristico per identificare 
clausole critiche senza inviare dati all'esterno.
""")

col1, col2 = st.columns([2, 1])

with col1:
    document_input = st.text_area("Incolla il documento finanziario qui:", 
                                  height=400, 
                                  placeholder="Esempio: 'Il prodotto prevede costi di gestione e incentivi per la rete...'")

with col2:
    st.info("Parametri di Screening")
    analysis_type = st.selectbox("Normativa di riferimento", 
                                 ["MiFID II (Mercati Finanziari)", "EU AI Act (Intelligenza Artificiale)"])
    
    analyze_btn = st.button("AVVIA ANALISI LOCALE", use_container_width=True)
    
    st.divider()
    if analyze_btn and document_input:
        findings, score = analyze_document_local(document_input, analysis_type)
        st.metric("Risk Score", f"{score}/5")
        if score > 3:
            st.error("Rischio Elevato")
        elif score > 1:
            st.warning("Attenzione Richiesta")
        else:
            st.success("Profilo di Rischio Basso")

if analyze_btn:
    if not document_input:
        st.warning("Inserisci un testo per procedere.")
    else:
        findings, score = analyze_document_local(document_input, analysis_type)
        st.subheader("Risultati dello Screening")
        st.markdown(findings)

st.markdown("---")
st.markdown("© 2026 **Cerberus R&D LTD** | Rodolfo Giuliana - CEO & Executive Director")
