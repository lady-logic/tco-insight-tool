# Ergänzungen für app.py

import streamlit as st
from pages import dashboard, step1, step2, step3, step4

# NEW: Energy Agent Check
def check_energy_agent_status():
    """Prüft Status des Energy Agents"""
    try:
        from energy.energy_agent import EnergyAgent
        agent = EnergyAgent()
        # Test connection
        test_price, test_source, is_realtime = agent.get_current_electricity_price('Düsseldorf (HQ)')
        return True, f"✅ Energy Agent aktiv ({test_source})"
    except ImportError as e:
        return False, f"❌ Energy Agent Module fehlt: {e}"
    except Exception as e:
        return False, f"⚠️ Energy Agent Fehler: {e}"

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
    .energy-status-success {
        background: linear-gradient(135deg, #28a745, #20c997);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 0.8rem;
    }
    .energy-status-warning {
        background: linear-gradient(135deg, #ffc107, #fd7e14);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        font-size: 0.8rem;
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

# NEW: Energy Agent Status Check (einmalig pro Session)
if 'energy_agent_status' not in st.session_state:
    energy_available, energy_status = check_energy_agent_status()
    st.session_state.energy_agent_status = energy_available
    st.session_state.energy_status_message = energy_status

# Header mit GEA-Design und Energy Status
col_header1, col_header2 = st.columns([3, 1])

with col_header1:
    st.markdown("""
    <div class="gea-header">
        <h1>🔧 TCO INSIGHT TOOL</h1>
        <p>Das skalierbare Tool für volle Kostentransparenz</p>
    </div>
    """, unsafe_allow_html=True)

with col_header2:
    # Energy Agent Status Display
    if st.session_state.energy_agent_status:
        st.markdown(f"""
        <div class="energy-status-success">
            {st.session_state.energy_status_message}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="energy-status-warning">
            {st.session_state.energy_status_message}
        </div>
        """, unsafe_allow_html=True)

# Navigation Sidebar mit Energy Info
with st.sidebar:
    st.markdown("### 🧭 Navigation")
    
    # Energy Agent Status in Sidebar
    if st.session_state.energy_agent_status:
        st.success("⚡ Energy Agent: Aktiv")
        st.caption("Echtzeit-Strompreise verfügbar")
    else:
        st.warning("⚡ Energy Agent: Offline")
        st.caption("Standard-Energiepreise werden verwendet")
    
    st.markdown("---")
    
    # Progress Indicator für Wizard
    if st.session_state.page in ['step1', 'step2', 'step3', 'step4']:
        progress_steps = ['step1', 'step2', 'step3', 'step4']
        current_step = progress_steps.index(st.session_state.page) + 1
        
        # Progress Bar
        progress = current_step / 4
        st.progress(progress)
        st.write(f"**Schritt {current_step} von 4**")
        
        # Step Labels with Energy Info
        step_labels = {
            'step1': '1️⃣ Asset-Typ wählen',
            'step2': '2️⃣ Grunddaten eingeben', 
            'step3': '3️⃣ KI-Schätzung ⚡',  # Energy Icon für Enhanced Analysis
            'step4': '4️⃣ TCO-Übersicht'
        }
        
        for step, label in step_labels.items():
            if step == st.session_state.page:
                st.markdown(f"**➤ {label}**")  # Current step
            elif progress_steps.index(step) < current_step - 1:
                st.markdown(f"✅ {label}")     # Completed steps
            else:
                st.markdown(f"⏸️ {label}")      # Future steps
        
        # Energy Enhancement Info für Step 3
        if st.session_state.page == 'step3' and st.session_state.energy_agent_status:
            st.info("🔋 **Enhanced Mode verfügbar!**\nEchtzeit-Energieanalyse aktiv")
        
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
    
    # NEW: Energy Agent Restart Button (wenn offline)
    if not st.session_state.energy_agent_status:
        st.markdown("---")
        if st.button("🔄 Energy Agent neu starten", use_container_width=True):
            # Reset Energy Agent Status
            del st.session_state.energy_agent_status
            del st.session_state.energy_status_message
            st.rerun()
    
    # Debug Panel (nur während Entwicklung)
    with st.expander("🐛 Debug Info"):
        st.write("**Current Page:**", st.session_state.page)
        st.write("**Energy Agent:**", "✅ Aktiv" if st.session_state.energy_agent_status else "❌ Offline")
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
        # NEW: Enhanced Step 3 mit Energy Agent als Standard
        if st.session_state.energy_agent_status:
            # Enhanced Mode with Energy Agent
            import pages.step3_erweitert as step3_enhanced
            step3_enhanced.show()
        else:
            # Fallback auf Standard Step 3
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
    st.write("- Energy Agent Module installiert?")
    
    if st.button("🏠 Zurück zum Dashboard"):
        st.session_state.page = 'dashboard'
        st.rerun()

# Footer mit Energy Info
st.markdown("---")
energy_info = "⚡ Energy Agent aktiv" if st.session_state.energy_agent_status else "⚠️ Energy Agent offline"
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>TCO Insight Tool - Entwickelt für GEA Group | {energy_info} | 
    <a href="#" style="color: #FF6600;">Dokumentation</a> | 
    <a href="#" style="color: #FF6600;">Support</a></p>
</div>
""", unsafe_allow_html=True)