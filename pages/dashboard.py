import streamlit as st
import plotly.express as px
import pandas as pd

def get_mock_dashboard_data():
    """Mock-Daten direkt in der Datei (temporär)"""
    return {
        "total_assets": 1247,
        "total_tco": 12400000,
        "estimated_costs": 2100000,
        "estimated_percentage": 17
    }

def get_mock_assets_data():
    """Mock-Assets direkt hier"""
    assets = [
        {"name": "SRV-DUS-001", "category": "Server", "manufacturer": "Dell", 
         "model": "PowerEdge R740", "price": 8500, "annual_maintenance": 1700, "location": "Düsseldorf"},
        {"name": "SRV-DUS-002", "category": "Server", "manufacturer": "HP", 
         "model": "ProLiant DL380", "price": 7200, "annual_maintenance": 1440, "location": "Düsseldorf"},
        {"name": "LAP-HH-089", "category": "Laptop", "manufacturer": "Lenovo", 
         "model": "ThinkPad X1", "price": 2200, "annual_maintenance": 330, "location": "Hamburg"},
        {"name": "Separator-A12", "category": "Separator", "manufacturer": "GEA", 
         "model": "WSP 5000", "price": 125000, "annual_maintenance": 18750, "location": "Oelde"},
    ]
    return pd.DataFrame(assets)

def show():
    """Zeigt die Dashboard-Startseite"""
    
    # Dashboard Metriken holen
    metrics = get_mock_dashboard_data()
    assets_df = get_mock_assets_data()
    
    # KPI-Cards im oberen Bereich
    st.markdown("## 📊 Übersicht")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Aktuelle Assets", f"{metrics['total_assets']:,}")
    
    with col2:
        st.metric("Gesamte TCO", f"€{metrics['total_tco']/1000000:.1f}M")
    
    with col3:
        st.metric("Geschätzte Kosten", f"€{metrics['estimated_costs']/1000000:.1f}M")
    
    with col4:
        st.metric("KI-Schätzungen", f"{metrics['estimated_percentage']}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hauptaktion: Neues Asset hinzufügen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="gea-card" style="text-align: center; padding: 2rem; background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px;">
            <h3>🚀 Neues Asset hinzufügen</h3>
            <p>Starten Sie die TCO-Analyse für ein neues Asset</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("+ NEUES ASSET HINZUFÜGEN", key="add_asset", type="primary", use_container_width=True):
            st.session_state.page = 'step1'
            st.session_state.asset_data = {}  # Reset
            st.rerun()
    
    # Asset-Übersicht Tabelle
    st.markdown("### 📋 Asset-Übersicht")
    
    # Einfache Tabelle
    display_df = assets_df.copy()
    display_df['TCO (5 Jahre)'] = display_df['price'] + (display_df['annual_maintenance'] * 5)
    display_df['TCO (5 Jahre)'] = display_df['TCO (5 Jahre)'].apply(lambda x: f"€{x:,.0f}")
    display_df['Anschaffung'] = display_df['price'].apply(lambda x: f"€{x:,.0f}")
    display_df['Wartung/Jahr'] = display_df['annual_maintenance'].apply(lambda x: f"€{x:,.0f}")
    
    # Nur relevante Spalten anzeigen
    st.dataframe(
        display_df[['name', 'category', 'manufacturer', 'location', 'Anschaffung', 'Wartung/Jahr', 'TCO (5 Jahre)']],
        use_container_width=True,
        hide_index=True
    )