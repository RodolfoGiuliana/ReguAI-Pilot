import streamlit as st
import os
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv

# Caricamento variabili d'ambiente
load_dotenv()

# --- CONFIGURAZIONE PAGINA (Deve essere la prima istruzione Streamlit) ---
st.set_page_config(
    page_title="ReguAI-Pilot | Cerberus R&D",
    page_icon="🛡️",
    layout="wide"
)

# --- INIZIALIZZAZIONE CLIENT OPENAI ---
api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ Chiave API OpenAI non trovata. Configura la variabile 'OPENAI_API_KEY' su Railway.")
    client = None
else:
    client = OpenAI(api_key=api_key)

# --- CONFIGURAZIONE MODELLO ---
MODEL_NAME = "gpt-4" 
MAX_TOKENS = 7000 

# --- GESTIONE PROMPT (Con Fallback anti-crash) ---
def load_prompt(analysis_type):
    # Prompt di emergenza se i file non vengono trovati
    fallbacks = {
        "MiFID II": "Agisci come esperto di compliance MiFID II. Analizza questo testo e trova criticità: {document_text}",
        "AI Act": "Agisci come consulente legale AI Act. Valuta i rischi di questo sistema AI: {document_text}"
    }
    
    filename = "mifid_ii_compliance_prompt.txt" if "MiFID" in analysis_type else "ai_act_implications_prompt.txt"
    path = os.path.join("prompt_templates", filename)
    
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return fallbacks.get("MiFID II" if "MiFID" in analysis_type else "AI Act")

# --- LOGICA DI ANALISI ---
def run_analysis(user_input, p_template):
    if not client:
        return "Errore: Client OpenAI non configurato."
    
    try:
        # Semplice troncamento per evitare errori di context window su Railway
        truncated_text = user_input[:12000] 
        full_prompt = p_template.replace("{document_text}", truncated_text)
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "system", "content": "Sei un analista di compliance d'élite."},
                      {"role": "user", "content": full_prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Errore durante l'analisi: {str(e)}"

# --- INTERFACCIA UTENTE ---
st.title("🛡️ ReguAI-Pilot")
st.caption("Boutique Compliance Engine by Cerberus R&D")

col1, col2 = st.columns([2, 1])

with col1:
    document_input = st.text_area("Incolla il documento finanziario qui:", height=450)

with col2:
    st.info("Configurazione Analisi")
    analysis_type = st.selectbox("Focus Normativo", ["MiFID II Compliance", "AI Act Implications"])
    
    analyze_btn = st.button("AVVIA SCREENING", use_container_width=True)
    
    st.divider()
    st.markdown("### Compliance Score")
    st.warning("Analisi preliminare automatizzata")

if analyze_btn:
    if not document_input:
        st.warning("Inserisci un testo per procedere.")
    else:
        prompt = load_prompt(analysis_type)
        with st.spinner("L'intelligenza artificiale sta analizzando i rischi..."):
            report = run_analysis(document_input, prompt)
            st.subheader("Report Risultati")
            st.markdown(report)

st.markdown("---")
st.markdown("© 2026 Cerberus R&D LTD | Rodolfo Giuliana - CEO & Executive Director")
