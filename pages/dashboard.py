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
    
    col_energy1, col_energy2 = st.columns([1, 2])
    
    with col_energy1:
        energy_available = show_energy_widget()
    
    with col_energy2:
        if energy_available:
            st.info("🔋 **Energy Agent aktiv** - Echtzeit-Strompreise verfügbar für optimierte TCO-Berechnungen")
        else:
            st.warning("⚠️ **Energy Agent offline** - Standard-Energiepreise werden verwendet")
            
    show_energy_optimization_summary()
    
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
    

def show_energy_widget():
    """Zeigt Energy-Widget im Dashboard"""
    
    try:
        from energy.energy_agent import EnergyAgent
        energy_agent = EnergyAgent()
        
        # Aktueller Strompreis für HQ
        current_price, source, is_realtime = energy_agent.get_current_electricity_price('Düsseldorf (HQ)')
        
        # Status-Farbe
        status_color = "#28a745" if is_realtime else "#ffc107"
        status_icon = "🟢" if is_realtime else "🟡"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6600, #FF8800); color: white; 
                    border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">⚡ Strompreis (Düsseldorf)</div>
                    <div style="font-size: 1.5rem; font-weight: bold;">€{current_price:.4f}/kWh</div>
                    <div style="font-size: 0.7rem; opacity: 0.9;">{source}</div>
                </div>
                <div style="font-size: 2rem;">{status_icon}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return True
        
    except ImportError:
        # Fallback wenn Energy Agent nicht verfügbar
        st.markdown("""
        <div style="background: #6c757d; color: white; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
            <div style="font-size: 0.8rem; opacity: 0.8;">⚡ Strompreis</div>
            <div style="font-size: 1.5rem; font-weight: bold;">€0.2600/kWh</div>
            <div style="font-size: 0.7rem; opacity: 0.9;">Standard (Energy Agent offline)</div>
        </div>
        """, unsafe_allow_html=True)
        
        return False

def show_energy_optimization_summary():
    """Zeigt Energy-Optimierungs-Übersicht"""
    
    # Mock-Daten für Demo (könnte aus Datenbank kommen)
    energy_stats = {
        'total_assets_with_energy': 342,
        'monthly_energy_cost': 28500,
        'optimization_potential': 4200,
        'assets_with_optimization': 67
    }
    
    st.markdown("### ⚡ Energie-Optimierung Übersicht")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Assets mit Energieverbrauch", 
            f"{energy_stats['total_assets_with_energy']:,}",
            help="Anzahl Assets mit Stromverbrauch"
        )
    
    with col2:
        st.metric(
            "Monatliche Energiekosten", 
            f"€{energy_stats['monthly_energy_cost']:,}",
            help="Geschätzte monatliche Stromkosten aller Assets"
        )
    
    with col3:
        savings_pct = (energy_stats['optimization_potential'] / energy_stats['monthly_energy_cost']) * 100
        st.metric(
            "Einsparpotential", 
            f"€{energy_stats['optimization_potential']:,}",
            f"{savings_pct:.1f}% möglich",
            help="Geschätztes monatliches Einsparpotential"
        )
    
    with col4:
        st.metric(
            "Optimierbare Assets", 
            f"{energy_stats['assets_with_optimization']:,}",
            help="Assets mit identifizierten Optimierungsmöglichkeiten"
        )


    """Zeigt die Dashboard-Startseite mit Energy Integration"""
    
    # ... bestehender Code für KPI-Cards ...
    
    # NEW: Energy Widget nach den KPI-Cards
    col_energy1, col_energy2 = st.columns([1, 2])
    
    with col_energy1:
        energy_available = show_energy_widget()
    
    with col_energy2:
        if energy_available:
            st.info("🔋 **Energy Agent aktiv** - Echtzeit-Strompreise verfügbar für optimierte TCO-Berechnungen")
        else:
            st.warning("⚠️ **Energy Agent offline** - Standard-Energiepreise werden verwendet")
    
    # ... bestehender Code für Asset hinzufügen ...
    
    # NEW: Energy Optimization Summary
    show_energy_optimization_summary()
    
    # ... Rest der Dashboard-Funktion bleibt gleich ...