import streamlit as st

# Seitenkonfiguration
st.set_page_config(
    page_title="GEA TCO Analyse Tool",
    page_icon="🏭",
    layout="wide"
)

# Import des reduzierten Dashboards
try:
    from pages.dashboard_simple import show as show_dashboard
except ImportError as e:
    st.error(f"❌ Import-Fehler: {e}")
    st.stop()

# Einfaches GEA Styling
st.markdown("""
<style>
:root {
    --gea-blue: #0052A3;
    --gea-dark-blue: #003875;
}

.stButton > button {
    background: linear-gradient(135deg, var(--gea-blue), var(--gea-dark-blue));
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
}

.stSelectbox > div > div {
    border: 2px solid #E2E8F0;
    border-radius: 6px;
}

h1 {
    color: var(--gea-dark-blue);
}

.stTable {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Hauptinhalt
show_dashboard()