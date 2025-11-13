import streamlit as st
import os
import json
import requests
from dotenv import load_dotenv
from prompt_advanced import few_shot_prompt, cot_prompt, role_prompt

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

# Load templates
@st.cache_data
def load_templates():
    with open(os.path.join(os.path.dirname(__file__), "templates.json")) as f:
        return json.load(f)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""
if 'is_generating' not in st.session_state:
    st.session_state.is_generating = False

def generate_content_streamlit(template_key, mode, params, role):
    """Generate content using the selected template and mode"""
    if not template_key or not mode:
        st.error("⚠️ Seleziona un template e una modalità.")
        return None

    try:
        params_dict = json.loads(params) if params else {}
    except json.JSONDecodeError:
        st.error("⚠️ I parametri devono essere in formato JSON valido.")
        return None

    # Generate prompt based on mode
    if mode == "Few-Shot":
        examples = [
            {"input": {"tema": "leadership"}, "output": "Hook: La leadership è comunicazione..."},
            {"input": {"tema": "innovazione"}, "output": "Hook: L'innovazione nasce dal rischio..."}
        ]
        prompt = few_shot_prompt(template_key, params_dict, examples)
    elif mode == "Chain-of-Thought":
        prompt = cot_prompt(template_key, params_dict)
    else:  # Role Prompting
        if not role:
            st.error("⚠️ Inserisci una descrizione del ruolo per la modalità Role Prompting.")
            return None
        prompt = role_prompt(template_key, params_dict, role)

    # Display generated prompt
    st.text_area("📝 Prompt Generato", prompt, height=200, disabled=True)

    # Check API key
    if not API_KEY:
        st.warning("🔑 Modalità demo: imposta GEMINI_API_KEY nel file .env per generazioni reali")
        return "[Modalità demo - imposta GEMINI_API_KEY per generazioni reali]"

    # Make API request
    try:
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(f"{API_URL}?key={API_KEY}", json=payload)
        
        if response.status_code == 200:
            text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            return text
        else:
            st.error(f"❌ Errore API: {response.text}")
            return None
    except Exception as e:
        st.error(f"❌ Errore durante la generazione: {str(e)}")
        return None

# Main app
def main():
    st.set_page_config(
        page_title="AI Content Creator",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.title("🤖 AI Content Creator")
    st.markdown("### Genera contenuti AI con template avanzati")
    
    # Load templates
    TEMPLATES = load_templates()
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configurazione")
        
        # Template selection
        template_options = list(TEMPLATES.keys())
        template_labels = [TEMPLATES[key]["name"] for key in template_options]
        selected_template_label = st.selectbox("📋 Seleziona Template", template_labels)
        selected_template = template_options[template_labels.index(selected_template_label)]

        # Show template instructions and variables
        st.markdown("---")
        st.subheader("📘 Istruzioni del Template")
        st.markdown(TEMPLATES[selected_template].get("instructions", ""))
        vars_required = ", ".join(TEMPLATES[selected_template].get("variables", []))
        st.caption(f"Variabili richieste: {vars_required}")
        
        # Mode selection
        mode = st.selectbox("🎯 Modalità", ["Few-Shot", "Chain-of-Thought", "Role Prompting"])
        
        # Role description (only for Role Prompting mode)
        role_description = ""
        if mode == "Role Prompting":
            role_description = st.text_area(
                "👤 Descrizione Ruolo",
                placeholder="Es: Sei un esperto di marketing digitale...",
                height=100
            )
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("🎛️ Parametri")
        
        # Input fields separati per parametri comuni
        tema = st.text_input("📍 Tema", placeholder="Es: tecnologia, marketing, salute")
        prodotto = st.text_input("📦 Prodotto", placeholder="Es: app fitness, software CRM")
        target = st.text_input("👥 Target", placeholder="Es: giovani, professionisti, aziende")
        argomento = st.text_input("📝 Argomento", placeholder="Es: intelligenza artificiale, sviluppo personale")
        tono = st.selectbox("🎨 Tono", ["professionale", "informale", "ispirazionale", "tecnico", "amichevole"])
        
        # Costruisci il dizionario dei parametri
        params_dict = {}
        if tema:
            params_dict["tema"] = tema
        if prodotto:
            params_dict["prodotto"] = prodotto
        if target:
            params_dict["target"] = target
        if argomento:
            params_dict["argomento"] = argomento
        if tono:
            params_dict["tono"] = tono
        
        # Mostra i parametri generati (opzionale, per debug)
        with st.expander("🔍 Visualizza parametri JSON generati"):
            st.json(params_dict)
        
        # Converti in JSON string per la funzione di generazione
        params_input = json.dumps(params_dict) if params_dict else ""
        
        # Generate button
        if st.button("🚀 Genera Contenuto", type="primary", use_container_width=True):
            st.session_state.is_generating = True
            with st.spinner("🔄 Generazione in corso..."):
                content = generate_content_streamlit(selected_template, mode, params_input, role_description)
                if content:
                    st.session_state.generated_content = content
                    # Save to file
                    BASE_DIR = os.path.join(os.path.dirname(__file__), "examples")
                    os.makedirs(BASE_DIR, exist_ok=True)
                    with open(os.path.join(BASE_DIR, "output.txt"), "w", encoding="utf-8") as f:
                        f.write(content)
            st.session_state.is_generating = False
    
    with col2:
        st.header("📄 Contenuto Generato")
        
        if st.session_state.generated_content:
            st.text_area(
                "✅ Risultato",
                st.session_state.generated_content,
                height=400
            )
            
            # Copy to clipboard button
            st.button("📋 Copia", on_click=lambda: st.write("✅ Contenuto copiato!"))
            
            # Download button
            st.download_button(
                label="💾 Scarica",
                data=st.session_state.generated_content,
                file_name="contenuto_generato.txt",
                mime="text/plain"
            )
        else:
            st.info("👆 Inserisci i parametri e clicca 'Genera Contenuto' per iniziare")
    
    # Footer
    st.markdown("---")
    st.markdown("💡 **Tips**: Compila i campi sopra e clicca 'Genera Contenuto' per creare il tuo contenuto AI!")

if __name__ == "__main__":
    main()