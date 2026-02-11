import streamlit as st
import os
from openai import OpenAI # Utilizzo di OpenAI per semplicità (spazio per altri LLM)
import tiktoken # Per il calcolo dei token
from dotenv import load_dotenv

load_dotenv() # Caricare le variabili d'ambiente dal file .env

# --- Configurazione OpenAI ---
try:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
except Exception as e:
    st.error(f"Errore di configurazione OpenAI: {e}. Assicurati di avere OPENAI_API_KEY nel tuo file .env")
    st.stop()

# --- Parametri del Modello ---
MODEL_NAME = "gpt-4" # O "gpt-3.5-turbo" per costi inferiori
MAX_TOKENS = 8000 # Max tokens per GPT-4, adattare se si usa gpt-3.5-turbo
OUTPUT_TOKENS = 1500 # Token massimi per risposta AI

# --- Prompt Templates (da file esterni per pulizia) ---
def load_prompt(filename):
    with open(os.path.join("prompt_templates", filename), "r", encoding="utf-8") as f:
        return f.read()

# --- Funzioni di Utility ---
def count_tokens(text):
    """Conta i token di un testo usando il codificatore di OpenAI."""
    try:
        encoding = tiktoken.encoding_for_model(MODEL_NAME)
        return len(encoding.encode(text))
    except Exception as e:
        st.warning(f"Errore nel calcolo dei token: {e}. Il conteggio potrebbe essere impreciso.")
        return len(text.split()) / 4 # Stima approssimativa

def get_llm_response(prompt_template, user_input, max_output_tokens=OUTPUT_TOKENS):
    """Invia il prompt all'LLM e restituisce la risposta."""
    try:
        full_prompt = prompt_template.format(document_text=user_input)
        
        
        prompt_tokens = count_tokens(full_prompt)
        if prompt_tokens + max_output_tokens > MAX_TOKENS:
            st.warning(f"Il prompt generato è troppo lungo ({prompt_tokens} token). Verrà troncato per rientrare nel limite del modello ({MAX_TOKENS - max_output_tokens} token).")
            # Trovare un modo più intelligente per troncare
            max_input_tokens = MAX_TOKENS - max_output_tokens - 100 # Lasciare un buffer
            user_input_tokens = count_tokens(user_input)
            
            if user_input_tokens > max_input_tokens:
                # Esempio di troncamento semplice: prendere l'inizio e la fine
                # In un caso reale, si usa un sommario intelligente o si dividerebbe il documento
                st.info("Tentativo di troncamento: mantenendo inizio e fine del documento.")
                user_input_parts = user_input.split()
                # Considerare solo la prima parte e l'ultima parte
                # Questo è un placeholder, un vero sistema userebbe text-splitting intelligente
                truncated_user_input = " ".join(user_input_parts[:int(len(user_input_parts)*0.4)]) + \
                                      "\n\n[... Documento troncato per limite di token ...]\n\n" + \
                                      " ".join(user_input_parts[int(len(user_input_parts)*0.6):])
                
                full_prompt = prompt_template.format(document_text=truncated_user_input)
                prompt_tokens = count_tokens(full_prompt)
                if prompt_tokens > MAX_TOKENS - max_output_tokens:
                    st.error("Anche dopo il troncamento, il prompt è troppo lungo. Prova con un documento più corto.")
                    return "Errore: Documento troppo grande per l'analisi."
            
        messages = [{"role": "user", "content": full_prompt}]
        
        with st.spinner("Analisi in corso... Questo potrebbe richiedere alcuni secondi."):
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=max_output_tokens,
                temperature=0.4 # Temperatura più bassa per risposte più conservative
            )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Si è verificato un errore durante la comunicazione con l'LLM: {e}")
        return "Impossibile completare l'analisi."

# --- Interfaccia Utente Streamlit ---
st.set_page_config(page_title="ReguAI-Pilot", layout="wide")

st.title("🛡️ ReguAI-Pilot: Compliance Assistant (MiFID II / AI Act)")
st.subheader("Un prototipo per l'analisi preliminare di documenti finanziari con LLM.")

st.markdown("""
Questo strumento dimostra come un **agente LLM** possa supportare l'analisi di conformità per prodotti e servizi finanziari, focalizzandosi su MiFID II e i principi emergenti dell'AI Act. 
Carica un documento (es. KIID, Termini e Condizioni di un prodotto finanziario) e ReguAI-Pilot evidenzierà potenziali rischi o aree di attenzione.
""")

st.warning("⚠️ **Disclaimer:** Questo è un prototipo dimostrativo e non sostituisce in alcun modo la consulenza legale, la due diligence professionale o l'analisi di compliance qualificata. Le informazioni fornite dall'AI sono indicative e potrebbero contenere imprecisioni o allucinazioni. Usalo con cautela e a proprio rischio.")

document_input = st.text_area(
    "Incolla qui il testo del tuo documento finanziario (es. KIID, Prospetto Informativo, T&C):",
    height=400,
    placeholder="Incolla il testo del documento qui..."
)

analysis_type = st.radio(
    "Seleziona il focus dell'analisi:",
    ("MiFID II Compliance", "AI Act Implications (per prodotti AI-driven)"),
    index=0 # Default to MiFID II
)

if st.button("Avvia Analisi di Conformità"):
    if not document_input:
        st.error("Per favore, incolla il testo del documento per avviare l'analisi.")
    else:
        # Carica il prompt template specifico
        if analysis_type == "MiFID II Compliance":
            prompt_file = "mifid_ii_compliance_prompt.txt"
        else: # AI Act Implications
            prompt_file = "ai_act_implications_prompt.txt"
            
        compliance_prompt = load_prompt(prompt_file)
        
        st.info(f"Avviando l'analisi per '{analysis_type}'...")
        
        # Esegui l'analisi
        compliance_report = get_llm_response(compliance_prompt, document_input)
        
        st.subheader(f"Report di Conformità Preliminare: {analysis_type}")
        st.markdown(compliance_report)

        st.success("Analisi completata!")

st.markdown("---")
st.markdown("Sviluppato da [Cerberus R&D LTD](https://www.cerberusrd.com) | [GitHub Repository](https://github.com/your-github-username/ReguAI-Pilot)")
