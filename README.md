# AI Content Creator - Streamlit Version

Un'applicazione web moderna per generare contenuti AI utilizzando Google Gemini e tecniche di prompt engineering avanzate.

## 🚀 Caratteristiche

- **Interfaccia Moderna**: Interfaccia web intuitiva basata su Streamlit
- **Template Predefiniti**: 4 template di contenuto (LinkedIn, Blog, Email, Prodotto)
- **Tecniche Avanzate**: Supporta Few-Shot, Chain-of-Thought e Role Prompting
- **Generazione Real-time**: Integrazione con Google Gemini API
- **Esportazione Facile**: Scarica o copia il contenuto generato

## 📋 Requisiti

- Python 3.7+
- Chiave API Google Gemini

## 🔧 Installazione

1. **Installa le dipendenze**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configura la chiave API**:
   Crea un file `.env` nella directory principale con:
   ```
   GEMINI_API_KEY=tua_chiave_api_gemini
   ```

3. **Esegui l'applicazione**:
   ```bash
   streamlit run app_streamlit.py
   ```

## 🎯 Come Usare

1. **Seleziona un Template**: Scegli il tipo di contenuto da generare
2. **Scegli la Modalità**: 
   - **Few-Shot**: Usa esempi per guidare la generazione
   - **Chain-of-Thought**: Spiega il processo passo-passo
   - **Role Prompting**: Definisci un ruolo specifico per l'AI
3. **Inserisci Parametri**: Fornisci i parametri in formato JSON
4. **Genera**: Clicca su "Genera Contenuto" e ottieni il risultato!

## 📄 Esempi di Parametri JSON

```json
{"tema": "intelligenza artificiale", "target": "imprenditori"}
{"prodotto": "app di fitness", "caratteristiche": "tracking workout, nutrizione"}
{"argomento": "sviluppo personale", "tono": "ispirazionale"}
```

## 🆕 Novità nella Versione Streamlit

- ✅ Interfaccia responsive e moderna
- ✅ Sidebar organizzata per configurazioni
- ✅ Preview in tempo reale del contenuto
- ✅ Pulsanti per copiare e scaricare
- ✅ Gestione degli stati di sessione
- ✅ Messaggi di errore migliorati
- ✅ Layout a due colonne per migliore UX

## 🔗 Confronto con Versione Tkinter

| Feature | Tkinter | Streamlit |
|---------|---------|-----------|
| Interfaccia | Desktop classica | Web moderna |
| Installazione | Python base | `pip install streamlit` |
| Layout | Fisso | Responsive |
| Condivisione | File locale | URL condivisibile |
| UX | Base | Intuitiva e bella |

## 🛠️ Struttura del Progetto

```
ai_content_creator_gui/
├── app_streamlit.py      # Nuova versione Streamlit
├── app_gui.py           # Versione originale Tkinter
├── prompt_advanced.py   # Logica di prompt engineering
├── templates.json       # Template di contenuto
├── requirements.txt     # Dipendenze
├── .env                 # Configurazione API
└── examples/           # Output generati
    └── output.txt
```

## 📚 Risorse

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Gemini API](https://ai.google.dev/gemini-api/docs)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

---

**Nota**: L'applicazione richiede una connessione internet attiva per funzionare con Google Gemini API.