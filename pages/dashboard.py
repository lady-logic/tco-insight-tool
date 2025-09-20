# pages/dashboard.py - Korrigierte Version

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def get_industrial_dashboard_data():
    """Mock-Daten für 3 Kern-Equipment-Typen"""
    return {
        "total_assets": 498,
        "total_tco": 12400000,  # €12.4M
        "estimated_costs": 2100000,  # €2.1M
        "estimated_percentage": 22,
        "separators": 142,
        "homogenizers": 89,
        "pumps": 267
    }

def get_industrial_assets_data():
    """Mock-Assets für 3 Kategorien"""
    assets = [
        # Separatoren
        {"name": "SEP-GFA-001", "category": "Separator", "manufacturer": "GEA", 
         "model": "GFA 200-30-820", "price": 344261, "annual_maintenance": 41311, "location": "Oelde", "age": 1.2},
        {"name": "SEP-GFA-002", "category": "Separator", "manufacturer": "GEA", 
         "model": "GFA 100-69-357", "price": 234070, "annual_maintenance": 28088, "location": "Düsseldorf", "age": 2.1},
        {"name": "SEP-ALF-003", "category": "Separator", "manufacturer": "Alfa Laval", 
         "model": "LAPX 404", "price": 189000, "annual_maintenance": 24570, "location": "Berlin", "age": 3.4},
        
        # Homogenizer
        {"name": "HOM-ARI-001", "category": "Homogenizer", "manufacturer": "GEA", 
         "model": "Ariete 5400", "price": 189500, "annual_maintenance": 28425, "location": "Oelde", "age": 0.8},
        {"name": "HOM-TET-002", "category": "Homogenizer", "manufacturer": "Tetra Pak", 
         "model": "Rannie 1000", "price": 156000, "annual_maintenance": 23400, "location": "Hamburg", "age": 4.2},
        
        # Pumpen
        {"name": "PMP-GEA-001", "category": "Pump", "manufacturer": "GEA", 
         "model": "Hilge HYGIA", "price": 45000, "annual_maintenance": 5400, "location": "Düsseldorf", "age": 2.8},
        {"name": "PMP-ALF-002", "category": "Pump", "manufacturer": "Alfa Laval", 
         "model": "LKH Prime", "price": 38500, "annual_maintenance": 4620, "location": "Oelde", "age": 1.9},
        {"name": "PMP-GRU-003", "category": "Pump", "manufacturer": "Grundfos", 
         "model": "CRN 32", "price": 28000, "annual_maintenance": 3360, "location": "Berlin", "age": 5.1}
    ]
    return pd.DataFrame(assets)

def create_gea_overview_chart():
    """Erstellt Portfolio-Übersicht für 3 Equipment-Typen"""
    
    data = get_industrial_dashboard_data()
    
    categories = ['Pumpen', 'Separatoren', 'Homogenizer']
    counts = [data['pumps'], data['separators'], data['homogenizers']]
    
    # GEA Blau-Farbpalette
    colors = ['#0052A3', '#003875', '#1976D2']
    
    fig = go.Figure(data=[
        go.Bar(
            x=categories, 
            y=counts, 
            marker_color=colors,
            text=counts, 
            textposition='outside',
            textfont=dict(size=14, color='#003875', weight='bold'),
            hovertemplate='<b>%{x}</b><br>Assets: %{y}<br>Anteil: %{customdata:.1f}%<extra></extra>',
            customdata=[c/sum(counts)*100 for c in counts]
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="🏭 GEA Kern-Equipment Portfolio",
            font=dict(size=20, color='#003875', family="Arial Black")
        ),
        yaxis_title="Anzahl Assets",
        yaxis=dict(title_font=dict(color='#455A64'), tickfont=dict(color='#455A64')),
        xaxis=dict(title_font=dict(color='#455A64'), tickfont=dict(color='#455A64', size=12)),
        height=420,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=70, b=50, l=60, r=40)
    )
    
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor='#E2E8F0', gridwidth=1)
    
    return fig

def create_metric_card(value, label, color="#0052A3"):
    """Erstellt eine GEA Metric Card"""
    return f"""
    <div style="background: linear-gradient(135deg, {color}, #1976D2); 
                color: white; border-radius: 12px; padding: 1.8rem 1.2rem; 
                text-align: center; margin: 0.5rem; box-shadow: 0 6px 20px rgba(0, 82, 163, 0.3);">
        <div style="font-size: 2.2rem; font-weight: 800; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            {value}
        </div>
        <div style="font-size: 0.9rem; opacity: 0.9; margin: 0.5rem 0 0 0; font-weight: 400;">
            {label}
        </div>
    </div>
    """

def show_gea_kpis():
    """Zeigt GEA KPIs"""
    
    assets_df = get_industrial_assets_data()
    data = get_industrial_dashboard_data()
    
    avg_asset_value = assets_df['price'].mean()
    avg_maintenance_ratio = (assets_df['annual_maintenance'] / assets_df['price']).mean() * 100
    high_value_assets = len(assets_df[assets_df['price'] > 100000])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        metric_html = create_metric_card(f"{data['total_assets']:,}", "GEA Assets", "#003875")
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col2:
        metric_html = create_metric_card(f"€{avg_asset_value:,.0f}", "Ø Asset-Wert", "#0052A3")
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col3:
        metric_html = create_metric_card(f"{avg_maintenance_ratio:.1f}%", "Ø Wartungsratio", "#1976D2")
        st.markdown(metric_html, unsafe_allow_html=True)
    
    with col4:
        metric_html = create_metric_card(f"{high_value_assets}", "High-Value Assets", "#42A5F5")
        st.markdown(metric_html, unsafe_allow_html=True)

def show_equipment_insights():
    """Equipment-Insights für 3 Typen"""
    
    st.markdown("### 🔧 Equipment-Insights")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Portfolio Chart
        overview_fig = create_gea_overview_chart()
        st.plotly_chart(overview_fig, use_container_width=True)
    
    with col2:
        # Equipment Statistiken
        assets_df = get_industrial_assets_data()
        
        st.markdown("**📊 Equipment-Statistiken:**")
        
        equipment_stats = {
            'Separatoren': {'count': len(assets_df[assets_df['category'] == 'Separator']), 
                           'avg_price': assets_df[assets_df['category'] == 'Separator']['price'].mean(),
                           'icon': '🌀', 'color': '#003875'},
            'Homogenizer': {'count': len(assets_df[assets_df['category'] == 'Homogenizer']),
                           'avg_price': assets_df[assets_df['category'] == 'Homogenizer']['price'].mean(),
                           'icon': '🔄', 'color': '#1976D2'},
            'Pumpen': {'count': len(assets_df[assets_df['category'] == 'Pump']),
                      'avg_price': assets_df[assets_df['category'] == 'Pump']['price'].mean(),
                      'icon': '⚙️', 'color': '#0052A3'}
        }
        
        for equipment, stats in equipment_stats.items():
            st.markdown(f"""
            <div style="display: flex; align-items: center; justify-content: space-between; 
                        padding: 1rem; margin: 0.5rem 0; 
                        background: linear-gradient(135deg, #F5F7FA, white); 
                        border-left: 4px solid {stats['color']}; border-radius: 8px;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.8rem; margin-right: 1rem;">{stats['icon']}</span>
                    <div>
                        <strong style="color: #003875;">{equipment}</strong><br>
                        <small style="color: #455A64;">{stats['count']} Assets</small>
                    </div>
                </div>
                <div style="text-align: right;">
                    <strong style="color: {stats['color']};">€{stats['avg_price']:,.0f}</strong><br>
                    <small style="color: #666;">Ø Anschaffung</small>
                </div>
            </div>
            """, unsafe_allow_html=True)

def show():
    """Hauptfunktion für Dashboard"""
    
    # KPIs anzeigen
    show_gea_kpis()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hauptaktion: Neue Anlage
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 2.5rem; 
                    background: linear-gradient(135deg, #E3F2FD, white); 
                    border: 3px solid #0052A3; border-radius: 15px;
                    box-shadow: 0 8px 24px rgba(0, 82, 163, 0.2);">
            <div style="font-size: 3rem; margin-bottom: 1rem; color: #003875;">🏭</div>
            <h3 style="color: #003875; margin: 0.5rem 0;">Neue GEA Anlage hinzufügen</h3>
            <p style="color: #455A64; margin: 0;">
                Starten Sie die TCO-Analyse für eine neue GEA Industrie-Anlage
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("+ NEUE GEA ANLAGE HINZUFÜGEN", key="add_asset", type="primary", use_container_width=True):
            st.session_state.page = 'step1'
            st.session_state.asset_data = {}
            st.rerun()
    
    # Equipment Insights
    show_equipment_insights()
    
    # Asset-Tabelle
    st.markdown("### 📋 Aktuelle GEA Assets")
    
    assets_df = get_industrial_assets_data()
    display_df = assets_df.copy()
    
    # Formatierung
    display_df['Anschaffung'] = display_df['price'].apply(lambda x: f"€{x:,.0f}")
    display_df['Wartung/Jahr'] = display_df['annual_maintenance'].apply(lambda x: f"€{x:,.0f}")
    display_df['Wartungsratio'] = ((display_df['annual_maintenance'] / display_df['price']) * 100).apply(lambda x: f"{x:.1f}%")
    display_df['Alter'] = display_df['age'].apply(lambda x: f"{x:.1f} Jahre")
    
    # Spalten auswählen
    columns_to_show = ['name', 'category', 'manufacturer', 'model', 'location', 
                      'Anschaffung', 'Wartung/Jahr', 'Wartungsratio', 'Alter']
    
    display_df_final = display_df[columns_to_show].rename(columns={
        'name': 'Asset-Name',
        'category': 'Typ',
        'manufacturer': 'Hersteller',
        'model': 'Modell',
        'location': 'GEA Standort'
    })
    
    st.dataframe(display_df_final, use_container_width=True, hide_index=True)
    
    # Quick Actions
    st.markdown("### ⚡ GEA Quick Actions")
    
    col4, col5, col6, col7 = st.columns(4)
    
    with col4:
        if st.button("📊 TCO-Report", use_container_width=True):
            st.success("✅ GEA TCO-Report wird generiert...")
    
    with col5:
        if st.button("🔍 Asset-Suche", use_container_width=True):
            st.info("🔍 GEA Asset-Datenbank durchsuchen...")
    
    with col6:
        if st.button("📈 Trend-Analyse", use_container_width=True):
            st.info("📈 GEA Portfolio-Trends analysieren...")
    
    with col7:
        if st.button("⚙️ Service-Portal", use_container_width=True):
            st.info("⚙️ GEA Service-Portal öffnen...")
    
    # Portfolio Info
    st.markdown("### 💼 Portfolio-Übersicht")
    
    data = get_industrial_dashboard_data()
    
    col8, col9, col10 = st.columns(3)
    
    with col8:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003875, #0052A3); 
                    color: white; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="margin: 0; color: white;">💰 Gesamt-Portfolio</h4>
            <p style="margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold;">
                €{data['total_tco']/1000000:.1f}M
            </p>
            <small style="opacity: 0.9;">Total Cost of Ownership</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col9:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #1976D2, #42A5F5); 
                    color: white; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="margin: 0; color: white;">🧠 KI-Abdeckung</h4>
            <p style="margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold;">
                {data['estimated_percentage']}%
            </p>
            <small style="opacity: 0.9;">Assets ML-analysiert</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col10:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #455A64, #607D8B); 
                    color: white; border-radius: 12px; padding: 1.5rem; text-align: center;">
            <h4 style="margin: 0; color: white;">📈 Optimierung</h4>
            <p style="margin: 0.5rem 0; font-size: 1.8rem; font-weight: bold;">
                €{(data['total_tco'] * 0.15)/1000000:.1f}M
            </p>
            <small style="opacity: 0.9;">Einsparpotential</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()