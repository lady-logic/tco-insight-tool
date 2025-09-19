import streamlit as st
from pages import dashboard, step1, step2, step3, step4

def apply_gea_styling():
    st.markdown("""
    <style>
    .gea-header {
        background: linear-gradient(135deg, #003366, #0066CC);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .gea-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .gea-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    .gea-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .stButton > button {
        background-color: #FF6600;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# Seitenkonfiguration
st.set_page_config(
    page_title="TCO Insight Tool - GEA",
    page_icon="🔧",
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

# Header mit GEA-Design
st.markdown("""
<div class="gea-header">
    <h1>🔧 TCO INSIGHT TOOL</h1>
    <p>Das skalierbare Tool für volle Kostentransparenz</p>
</div>
""", unsafe_allow_html=True)

# Navigation Sidebar
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    # Progress Indicator für Wizard
    if st.session_state.page in ['step1', 'step2', 'step3', 'step4']:
        progress_steps = ['step1', 'step2', 'step3', 'step4']
        current_step = progress_steps.index(st.session_state.page) + 1
        
        # Progress Bar
        progress = current_step / 4
        st.progress(progress)
        st.write(f"**Schritt {current_step} von 4**")
        
        # Step Labels
        step_labels = {
            'step1': '1️⃣ Asset-Typ wählen',
            'step2': '2️⃣ Grunddaten eingeben', 
            'step3': '3️⃣ KI-Schätzung',
            'step4': '4️⃣ TCO-Übersicht'
        }
        
        for step, label in step_labels.items():
            if step == st.session_state.page:
                st.markdown(f"**➤ {label}**")  # Current step
            elif progress_steps.index(step) < current_step - 1:
                st.markdown(f"✅ {label}")     # Completed steps
            else:
                st.markdown(f"⏸️ {label}")      # Future steps
        
        st.markdown("---")
    
    # Navigation Buttons
    if st.button("🏠 Dashboard", use_container_width=True):
        st.session_state.page = 'dashboard'
        st.rerun()
    
    # Cancel Button (nur im Wizard)
    if st.session_state.page != 'dashboard':
        if st.button("❌ Vorgang abbrechen", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.session_state.asset_data = {}  # Reset data
            st.rerun()
    
    # Debug Panel (nur während Entwicklung)
    with st.expander("🐛 Debug Info"):
        st.write("**Current Page:**", st.session_state.page)
        st.write("**Asset Data:**")
        st.json(st.session_state.asset_data)
        
        # Quick Page Navigation (für Entwicklung)
        st.write("**Quick Nav:**")
        nav_col1, nav_col2 = st.columns(2)
        with nav_col1:
            if st.button("→ Step1", key="debug_step1"):
                st.session_state.page = 'step1'
                st.rerun()
            if st.button("→ Step3", key="debug_step3"):
                st.session_state.page = 'step3' 
                st.rerun()
        with nav_col2:
            if st.button("→ Step2", key="debug_step2"):
                st.session_state.page = 'step2'
                st.rerun()
            if st.button("→ Step4", key="debug_step4"):
                st.session_state.page = 'step4'
                st.rerun()

# Main Content Area - Page Router
try:
    if st.session_state.page == 'dashboard':
        dashboard.show()
    elif st.session_state.page == 'step1':
        step1.show()
    elif st.session_state.page == 'step2':
        step2.show()
    elif st.session_state.page == 'step3':
        if st.checkbox("🚀 Erweiterte TCO-Analyse verwenden", value=True):
            import pages.step3_erweitert as step3_enhanced
            step3_enhanced.show()
        else:
            step3.show()
    elif st.session_state.page == 'step4':
        step4.show()
    else:
        # Fallback für unbekannte Seiten
        st.error(f"❌ Unbekannte Seite: **{st.session_state.page}**")
        st.write("Verfügbare Seiten: dashboard, step1, step2, step3, step4")
        
        if st.button("🏠 Zurück zum Dashboard"):
            st.session_state.page = 'dashboard'
            st.rerun()

except Exception as e:
    # Error Handling
    st.error(f"❌ **Fehler beim Laden der Seite:** {st.session_state.page}")
    st.exception(e)
    
    st.write("**Mögliche Lösungen:**")
    st.write("- Prüfen Sie ob alle Page-Dateien existieren")
    st.write("- Prüfen Sie die Python-Syntax in den Page-Dateien")
    
    if st.button("🏠 Zurück zum Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>TCO Insight Tool - Entwickelt für GEA Group | 
    <a href="#" style="color: #FF6600;">Dokumentation</a> | 
    <a href="#" style="color: #FF6600;">Support</a></p>
</div>
""", unsafe_allow_html=True)