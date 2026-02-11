# ReguAI-Pilot
Un prototipo di assistente basato su LLM per la pre-analisi di conformità (MiFID II / AI Act) di un documento finanziario, fornendo un riassunto dei rischi potenziali e delle aree critiche.

# ReguAI-Pilot 🛡️: Il tuo assistente AI per la Compliance Finanziaria

**ReguAI-Pilot** è un prototipo dimostrativo che esplora il potenziale dei Large Language Models (LLM) nell'assistere le istituzioni finanziarie nella pre-analisi di conformità di documenti complessi. Sviluppato da [Cerberus R&D LTD](https://www.cerberusrd.com), questa applicazione web (Streamlit) offre una prima valutazione di testi relativi a prodotti o servizi finanziari, con un focus sui requisiti **MiFID II** e sulle implicazioni emergenti dell'**AI Act** europeo per i sistemi basati su Intelligenza Artificiale.

---

## 🎯 Il Problema che Risolviamo

La compliance normativa nel settore finanziario è onerosa, complessa e in continua evoluzione. L'introduzione di nuove normative (come l'AI Act) e la crescente complessità dei prodotti rendono la revisione documentale un processo estremamente dispendioso in termini di tempo e risorse. ReguAI-Pilot mira a:

* **Accelerare la Pre-Analisi:** Identificare rapidamente potenziali aree di rischio o non conformità.
* **Aumentare la Consapevolezza:** Offrire una prima valutazione delle implicazioni normative per i nuovi prodotti.
* **Dimostrare il Potenziale dell'AI:** Evidenziare come gli LLM possano diventare strumenti di supporto strategico nel RegTech.

---

## ✨ Caratteristiche Principali (MVP)

* **Analisi Multi-Normativa:** Supporto per l'analisi basata sui principi di MiFID II e sulle implicazioni dell'AI Act.
* **Interfaccia Utente Semplice:** Carica il testo del documento direttamente nell'applicazione.
* **Report Preliminari:** Genera un report strutturato che evidenzia i punti critici, i rischi e suggerisce aree di miglioramento.
* **Prototipo Basato su LLM:** Utilizza i modelli linguistici avanzati di OpenAI per l'interpretazione e la sintesi.
* **Hostable su Cloud:** Progettato per essere facilmente deployato su piattaforme come Railway, Streamlit Cloud, o Hugging Face Spaces.

---

## 🚀 Come Funziona (Dietro le Quinte)

ReguAI-Pilot sfrutta un'architettura a **agenti LLM** dove un modello linguistico viene istruito con un prompt specifico per agire come un "esperto di compliance" per una determinata normativa (es. MiFID II, AI Act).

1.  L'utente incolla il testo del documento finanziario.
2.  Il testo viene inviato a un LLM (es. GPT-4) insieme a un prompt dettagliato che definisce il ruolo dell'AI, gli obiettivi dell'analisi e la normativa di riferimento.
3.  L'LLM elabora il testo e genera un report strutturato che evidenzia i rischi, le potenziali non conformità e le raccomandazioni, simulando il lavoro di un analista umano.
4.  Viene applicato un meccanismo di gestione dei token per tentare di troncare documenti molto lunghi e rientrare nei limiti dei modelli, con avvisi chiari all'utente.

---

## 🛠️ Setup Locale e Deployment

### Prerequisiti

* Python 3.8+
* Un account OpenAI e una chiave API valida.

### Installazione

1.  Clona il repository:
    ```bash
    git clone [https://github.com/your-github-username/ReguAI-Pilot.git](https://github.com/your-github-username/ReguAI-Pilot.git)
    cd ReguAI-Pilot
    ```
2.  Crea un ambiente virtuale (consigliato):
    ```bash
    python -m venv venv
    source venv/bin/activate  # macOS/Linux
    # venv\Scripts\activate   # Windows
    ```
3.  Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```
4.  Crea un file `.env` nella root del progetto e aggiungi la tua chiave API di OpenAI:
    ```
    OPENAI_API_KEY=sk-your_openai_api_key_here
    ```
    **ATTENZIONE:** Non committare mai il file `.env` su GitHub! È già incluso nel `.gitignore`.

### Esecuzione

Per avviare l'applicazione Streamlit in locale:
```bash
streamlit run app.py


⚠️ Disclaimer Importante
ReguAI-Pilot è un prototipo. NON è uno strumento di compliance legale o professionale. Le analisi generate sono indicative e basate sull'interpretazione del testo da parte di un modello AI, che può "allucinare", commettere errori o non comprendere le sfumature legali. È indispensabile che ogni risultato sia verificato da un consulente legale o un esperto di compliance qualificato. Cerberus R&D LTD non si assume alcuna responsabilità per decisioni prese basandosi sui risultati di questo prototipo.

🤝 Contribuzioni
Siamo aperti a suggerimenti e collaborazioni per migliorare questo prototipo. Se hai idee, fork the repository, crea la tua branch e invia una Pull Request!

📜 Licenza
Questo progetto è rilasciato sotto licenza MIT.

Contatti
Per maggiori informazioni o per esplorare soluzioni AI personalizzate per il tuo business, visita il sito di Cerberus R&D LTD o contatta www.cerberusrd.com
