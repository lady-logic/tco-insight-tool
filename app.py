# app.py - Mit echtem GEA Logo aus Datei

import streamlit as st
import base64
import os

# Sichere Imports mit Fallback
try:
    from pages import dashboard, step1, step2, step3, step4
except ImportError as e:
    st.error(f"❌ Import-Fehler: {e}")
    st.stop()

def load_logo(logo_path):
    """Lädt das GEA Logo aus einer Datei"""
    try:
        # Verschiedene mögliche Pfade probieren
        possible_paths = [
            logo_path,
            f"assets/{logo_path}",
            f"images/{logo_path}",
            f"static/{logo_path}",
            f"./{logo_path}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, "rb") as f:
                    logo_bytes = f.read()
                    logo_base64 = base64.b64encode(logo_bytes).decode()
                    
                    # Detect file type
                    if path.lower().endswith('.svg'):
                        return f"data:image/svg+xml;base64,{logo_base64}"
                    elif path.lower().endswith('.png'):
                        return f"data:image/png;base64,{logo_base64}"
                    elif path.lower().endswith('.jpg') or path.lower().endswith('.jpeg'):
                        return f"data:image/jpeg;base64,{logo_base64}"
                    else:
                        return f"data:image/png;base64,{logo_base64}"  # Default to PNG
        
        # If no file found, return None
        return None
        
    except Exception as e:
        st.sidebar.error(f"Logo-Fehler: {e}")
        return None

def create_fallback_logo():
    """Erstellt ein einfaches Text-Logo als Fallback"""
    return """
    <div style="font-family: 'Arial Black', Arial, sans-serif; font-size: 3rem; 
                font-weight: 900; color: white; text-shadow: 0 3px 6px rgba(0,0,0,0.4);
                letter-spacing: -2px; margin-bottom: 1rem;">
        GEA
    </div>
    """

def apply_gea_styling():
    """GEA Corporate Design"""
    st.markdown("""
    <style>
    /* GEA 2022 Farbpalette */
    :root {
        --gea-ultramarine: #003875;
        --gea-blue-primary: #0052A3;
        --gea-blue-light: #1976D2;
        --gea-blue-accent: #42A5F5;
        --gea-blue-pale: #E3F2FD;
        --gea-navy: #1A365D;
        --gea-white: #FFFFFF;
        --gea-light-gray: #F5F7FA;
        --gea-medium-gray: #E2E8F0;
        --gea-steel: #455A64;
    }
    
    /* GEA Header */
    .gea-header {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-blue-primary));
        color: var(--gea-white);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 56, 117, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .gea-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at 30% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
        opacity: 0.6;
    }
    
    .gea-logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 2;
    }
    
    .gea-logo {
        max-height: 80px;
        max-width: 200px;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.4));
        margin-bottom: 1rem;
    }
    
    .gea-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 2;
    }
    
    .gea-header p {
        margin: 0.8rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
        position: relative;
        z-index: 2;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--gea-blue-primary), var(--gea-blue-light));
        color: var(--gea-white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-blue-primary));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 56, 117, 0.4);
    }
    
    /* Primary Button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-navy));
        box-shadow: 0 6px 16px rgba(0, 56, 117, 0.4);
        font-weight: 700;
        font-size: 1rem;
    }
    
    /* Cards */
    .gea-card {
        background: var(--gea-white);
        border: 2px solid var(--gea-medium-gray);
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: 0 4px 16px rgba(0, 82, 163, 0.08);
        transition: all 0.3s ease;
    }
    
    .gea-card:hover {
        border-color: var(--gea-blue-light);
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 82, 163, 0.15);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--gea-blue-primary), var(--gea-blue-light));
        border-radius: 4px;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--gea-light-gray), var(--gea-white));
        border-right: 1px solid var(--gea-medium-gray);
    }
    
    /* Success/Info Messages */
    .stSuccess > div {
        background-color: rgba(25, 118, 210, 0.1);
        border-left-color: var(--gea-blue-primary);
    }
    
    .stInfo > div {
        background-color: rgba(66, 165, 245, 0.1);
        border-left-color: var(--gea-blue-accent);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

def create_gea_header(title, subtitle=""):
    """GEA Header mit echtem Logo"""
    
    # Versuche verschiedene Logo-Dateinamen
    logo_files = [
        "gea_logo.svg",
        "gea_logo.png", 
        "gea-logo.svg",
        "gea-logo.png",
        "GEA_logo.svg",
        "GEA_logo.png",
        "logo.svg",
        "logo.png"
    ]
    
    logo_data = None
    for logo_file in logo_files:
        logo_data = load_logo(logo_file)
        if logo_data:
            break
    
    if logo_data:
        # Echtes Logo verwenden
        logo_html = f'<img src="{logo_data}" class="gea-logo" alt="GEA Logo">'
        st.sidebar.success("✅ GEA Logo geladen")
    else:
        # Fallback auf Text-Logo
        logo_html = create_fallback_logo()
        st.sidebar.warning("⚠️ Logo-Datei nicht gefunden - Text-Logo verwendet")
        st.sidebar.caption("Erwartete Dateien: gea_logo.svg/.png in assets/, images/ oder Hauptordner")
    
    return f"""
    <div class="gea-header">
        <div class="gea-logo-container">
            {logo_html}
        </div>
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """

def safe_show_page(page_module, page_name):
    """Sichere Ausführung einer Page mit Fehlerbehandlung"""
    try:
        if hasattr(page_module, 'show'):
            page_module.show()
        else:
            st.error(f"❌ Seite '{page_name}' hat keine 'show()' Funktion")
            st.write("**Debug Info:**")
            st.write(f"Verfügbare Funktionen in {page_name}: {dir(page_module)}")
            
            if st.button("🏠 Zurück zum Dashboard"):
                st.session_state.page = 'dashboard'
                st.rerun()
                
    except Exception as e:
        st.error(f"❌ Fehler beim Laden von '{page_name}': {e}")
        st.exception(e)
        
        if st.button("🏠 Zurück zum Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()

# Seitenkonfiguration
st.set_page_config(
    page_title="GEA TCO Insight Tool",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GEA Styling anwenden
apply_gea_styling()

# Session State initialisieren
if 'page' not in st.session_state:
    st.session_state.page = 'dashboard'
if 'asset_data' not in st.session_state:
    st.session_state.asset_data = {}

# GEA Header mit echtem Logo
header_html = create_gea_header(
    title="TCO INSIGHT TOOL",
    subtitle="Engineering for a better world - Speziell für GEA Industrie-Anlagen"
)
st.markdown(header_html, unsafe_allow_html=True)

# Navigation Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    # Logo-Status anzeigen
    logo_status = "✅ Logo geladen" if any(load_logo(f) for f in ["gea_logo.svg", "gea_logo.png", "logo.svg", "logo.png"]) else "⚠️ Text-Logo"
    st.caption(f"Logo-Status: {logo_status}")
    
    # Progress Indicator
    if st.session_state.page in ['step1', 'step2', 'step3', 'step4']:
        progress_steps = ['step1', 'step2', 'step3', 'step4']
        current_step = progress_steps.index(st.session_state.page) + 1
        
        progress = current_step / 4
        st.progress(progress)
        st.markdown(f"**Schritt {current_step} von 4**")
        
        step_labels = {
            'step1': '1️⃣ Equipment wählen',
            'step2': '2️⃣ Grunddaten eingeben', 
            'step3': '3️⃣ KI-Schätzung',
            'step4': '4️⃣ TCO-Übersicht'
        }
        
        for step, label in step_labels.items():
            if step == st.session_state.page:
                st.markdown(f"**➤ {label}**")
            elif progress_steps.index(step) < current_step - 1:
                st.markdown(f"✅ {label}")
            else:
                st.markdown(f"⏸️ {label}")
        
        st.markdown("---")
    
    # Navigation Buttons
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    # Logo Upload Option
    with st.expander("📎 Logo hochladen"):
        st.markdown("**GEA Logo hinzufügen:**")
        uploaded_file = st.file_uploader(
            "Wählen Sie das GEA Logo",
            type=['svg', 'png', 'jpg', 'jpeg'],
            help="Unterstützte Formate: SVG, PNG, JPG"
        )
        
        if uploaded_file is not None:
            # Save uploaded file
            os.makedirs("assets", exist_ok=True)
            logo_path = f"assets/gea_logo.{uploaded_file.name.split('.')[-1]}"
            
            with open(logo_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.success(f"✅ Logo gespeichert: {logo_path}")
            st.info("🔄 Seite neu laden um Logo zu sehen")
            
            if st.button("🔄 Neu laden"):
                st.rerun()
    
    # GEA Info
    with st.expander("ℹ️ GEA TCO Insight Tool"):
        st.markdown("""
        **🏭 Engineering for a better world**
        
        • **🌀 Separatoren** - Zentrifugal-Technologie
        • **🔄 Homogenizer** - Hochdruck-Systeme  
        • **⚙️ Pumpen** - Sanitär & Industrie
        
        **🧠 KI-gestützte Vorhersagen** mit Machine Learning
        """)
        
        st.markdown("**🌍 GEA Standorte:**")
        st.write("Düsseldorf (HQ) • Oelde • Berlin • Hamburg")
    
    # Cancel Button (nur im Wizard)
    if st.session_state.page != 'dashboard':
        st.markdown("---")
        if st.button("❌ Vorgang abbrechen", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.session_state.asset_data = {}
            st.rerun()

# Main Content Area - Sichere Page Router
try:
    if st.session_state.page == 'dashboard':
        safe_show_page(dashboard, 'dashboard')
    elif st.session_state.page == 'step1':
        safe_show_page(step1, 'step1')
    elif st.session_state.page == 'step2':
        safe_show_page(step2, 'step2')
    elif st.session_state.page == 'step3':
        safe_show_page(step3, 'step3')
    elif st.session_state.page == 'step4':
        safe_show_page(step4, 'step4')
    else:
        st.error(f"❌ Unbekannte Seite: **{st.session_state.page}**")
        if st.button("🏠 Zurück zum Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()

except Exception as e:
    st.error(f"❌ **Kritischer Anwendungsfehler**")
    st.exception(e)
    
    st.markdown("**🔧 Mögliche Lösungen:**")
    st.write("• Prüfen Sie ob alle Page-Dateien existieren")
    st.write("• Stellen Sie sicher, dass jede Page eine show() Funktion hat")
    st.write("• Überprüfen Sie die Python-Syntax in den Page-Dateien")
    
    if st.button("🔄 Anwendung neu laden", type="primary"):
        st.rerun()

# GEA Footer
st.markdown("---")

# Footer Logo (kleiner)
footer_logo_data = load_logo("gea_logo.svg") or load_logo("gea_logo.png")
if footer_logo_data:
    footer_logo_html = f'<img src="{footer_logo_data}" style="height: 40px; margin-bottom: 1rem;" alt="GEA Logo">'
else:
    footer_logo_html = '<div style="font-size: 1.5rem; font-weight: bold; color: #003875; margin-bottom: 1rem;">GEA</div>'

st.markdown(f"""
<div style="text-align: center; color: #455A64; padding: 2rem; 
           background: linear-gradient(135deg, #F5F7FA, white); 
           border-radius: 8px; margin-top: 2rem;">
    {footer_logo_html}
    <p style="margin: 0; font-size: 0.9rem;">
        © 2025 GEA Group Aktiengesellschaft | TCO Insight Tool<br>
        <strong style="color: #003875;">Engineering for a better world</strong>
    </p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.8rem; opacity: 0.8;">
        Ein Unternehmen des MDAX und STOXX® Europe 600
    </p>
</div>
""", unsafe_allow_html=True)