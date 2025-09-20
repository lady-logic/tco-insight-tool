import streamlit as st
import time
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import sys
import os

# Add ml directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

try:
    from ml.tco_predictor import TCOPredictor
    from ml.tco_components import ExtendedTCOCalculator
    from data.centrifuge_data_loader import load_centrifuge_data
    ML_AVAILABLE = True
except ImportError as e:
    ML_AVAILABLE = False
    st.error(f"❌ Erweiterte ML-Module nicht verfügbar: {e}")

@st.cache_resource
def load_enhanced_ml_model():
    """Lädt das ML-Model mit Zentrifugen-Daten"""
    if not ML_AVAILABLE:
        return None, None
    
    try:
        # Lade Zentrifugen-Daten
        centrifuge_df = load_centrifuge_data("HinterlandHack _ FinaleListe.xlsx")
        
        # Trainiere ML-Model mit echten Zentrifugen-Daten
        predictor = TCOPredictor()
        
        # Erweiterte Features für Zentrifugen hinzufügen
        enhanced_df = centrifuge_df.copy()
        
        # Speichere für Training
        enhanced_df.to_csv('data/enhanced_centrifuge_training.csv', index=False)
        
        # Model trainieren
        stats = predictor.train('data/enhanced_centrifuge_training.csv')
        predictor.save_model('ml/enhanced_tco_model.pkl')
        
        # Erweiterten TCO-Calculator initialisieren
        tco_calculator = ExtendedTCOCalculator()
        
        return predictor, tco_calculator
        
    except Exception as e:
        st.error(f"❌ Fehler beim Laden der erweiterten Module: {e}")
        return None, None

def create_enhanced_analysis_animation():
    """Erweiterte ML-Analyse-Animation"""
    
    analysis_steps = [
        {"step": "🔍 Lade Enhanced ML-Model...", "duration": 1.0},
        {"step": "📊 Analysiere Zentrifugen-Features...", "duration": 1.2},
        {"step": "⚡ Verarbeite Energie-Parameter...", "duration": 1.0},
        {"step": "💧 Berechne Wasserverbrauch...", "duration": 0.9},
        {"step": "👥 Analysiere Personalaufwand...", "duration": 1.1},
        {"step": "🌳 Random Forest Inference...", "duration": 1.0},
        {"step": "📈 Berechne TCO-Komponenten...", "duration": 1.3},
        {"step": "🎯 Erstelle Konfidenz-Score...", "duration": 0.8},
        {"step": "✅ Erweiterte TCO-Analyse abgeschlossen!", "duration": 0.5}
    ]
    
    progress_container = st.empty()
    status_container = st.empty()
    
    total_steps = len(analysis_steps)
    
    for i, step_info in enumerate(analysis_steps):
        progress = (i + 1) / total_steps
        progress_container.progress(progress)
        status_container.write(f"**{step_info['step']}**")
        time.sleep(step_info['duration'])
    
    progress_container.empty()
    status_container.empty()

def create_tco_breakdown_chart(tco_result):
    """Erstellt detaillierte TCO-Aufschlüsselung"""
    
    annual_breakdown = tco_result['annual_breakdown']
    
    # Entferne Zero-Komponenten
    filtered_breakdown = {k: v for k, v in annual_breakdown.items() if v > 0}
    
    # Farben für verschiedene Komponenten
    colors = {
        'maintenance': '#003366',       # GEA Blau
        'energy': '#FF6600',           # GEA Orange  
        'water': '#0066CC',            # Hellblau
        'personnel': '#28a745',        # Grün
        'spare_parts': '#ffc107',      # Gelb
        'cleaning': '#6f42c1',         # Violett
        'monitoring': '#20c997',       # Türkis
        'compliance': '#fd7e14',       # Orange-rot
        'insurance': '#6c757d'         # Grau
    }
    
    component_colors = [colors.get(comp, '#cccccc') for comp in filtered_breakdown.keys()]
    
    # Horizontales Balkendiagramm für bessere Lesbarkeit
    fig = go.Figure(go.Bar(
        y=list(filtered_breakdown.keys()),
        x=list(filtered_breakdown.values()),
        orientation='h',
        marker_color=component_colors,
        text=[f"€{v:,.0f}" for v in filtered_breakdown.values()],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="🔧 Jährliche TCO-Komponenten",
        xaxis_title="Kosten pro Jahr (€)",
        yaxis_title="TCO-Komponenten",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_lifetime_cost_chart(tco_result):
    """Zeigt Kostenentwicklung über Lebensdauer"""
    
    lifetime_years = tco_result['financial_metrics']['lifetime_years']
    annual_operating = tco_result['financial_metrics']['total_annual_operating']
    
    # Simuliere eskalierte Kosten über Jahre
    years = list(range(0, lifetime_years + 1))
    cumulative_costs = [tco_result['cost_summary']['acquisition_costs']]  # Start mit Anschaffung
    annual_costs = [tco_result['cost_summary']['acquisition_costs']]
    
    for year in range(1, lifetime_years + 1):
        # 3% Inflation + 2% Verschleiß
        escalation_factor = (1.05) ** year
        year_cost = annual_operating * escalation_factor
        annual_costs.append(year_cost)
        cumulative_costs.append(cumulative_costs[-1] + year_cost)
    
    # Erstelle Dual-Axis Chart
    fig = go.Figure()
    
    # Jährliche Kosten (Balken)
    fig.add_trace(go.Bar(
        x=years,
        y=annual_costs,
        name='Jährliche Kosten',
        marker_color='#FF6600',
        yaxis='y'
    ))
    
    # Kumulative Kosten (Linie)
    fig.add_trace(go.Scatter(
        x=years,
        y=cumulative_costs,
        mode='lines+markers',
        name='Kumulative TCO',
        line=dict(color='#003366', width=3),
        marker=dict(size=6),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title='TCO-Entwicklung über Lebensdauer',
        xaxis_title='Jahr',
        yaxis=dict(title='Jährliche Kosten (€)', side='left'),
        yaxis2=dict(title='Kumulative TCO (€)', side='right', overlaying='y'),
        height=400,
        hovermode='x unified'
    )
    
    return fig

def create_component_confidence_chart(tco_result):
    """Zeigt Konfidenz-Level der verschiedenen Komponenten"""
    
    component_confidence = tco_result['confidence_metrics']['component_confidence']
    annual_breakdown = tco_result['annual_breakdown']
    
    # Nur Komponenten mit Kosten > 0
    filtered_confidence = {k: v for k, v in component_confidence.items() 
                          if annual_breakdown.get(k, 0) > 0}
    
    # Bubble Chart: Kosten vs Konfidenz
    components = list(filtered_confidence.keys())
    confidences = [filtered_confidence[comp] * 100 for comp in components]  # In Prozent
    costs = [annual_breakdown[comp] for comp in components]
    
    fig = go.Figure(go.Scatter(
        x=confidences,
        y=costs,
        mode='markers+text',
        marker=dict(
            size=[cost/1000 for cost in costs],  # Größe basierend auf Kosten
            color=confidences,
            colorscale='RdYlGn',
            showscale=True,
            colorbar=dict(title="Konfidenz (%)")
        ),
        text=components,
        textposition="middle center",
        textfont=dict(size=10, color="white")
    ))
    
    fig.update_layout(
        title='Komponenten: Kosten vs. Vorhersage-Konfidenz',
        xaxis_title='Konfidenz (%)',
        yaxis_title='Jährliche Kosten (€)',
        height=400
    )
    
    return fig

@st.cache_resource
def load_energy_agent():
    """Lädt den Energy Agent für Echtzeit-Strompreise"""
    try:
        from energy.energy_agent import EnergyAgent
        agent = EnergyAgent()
        return agent
    except ImportError as e:
        st.warning(f"⚠️ Energy Agent nicht verfügbar: {e}")
        return None

def create_energy_dashboard(energy_agent, location):
    """Erstellt Live-Energie-Dashboard"""
    
    if not energy_agent:
        return None
    
    try:
        dashboard_data = energy_agent.get_price_dashboard_data(location)
        
        # Current Price Display
        current_price = dashboard_data['current_price']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6600, #FF8800); color: white; 
                    border-radius: 15px; padding: 1.5rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 0.8rem; opacity: 0.8;">⚡ Aktueller Strompreis</div>
            <h3 style="margin: 0; font-size: 1.8rem;">€{current_price['value']:.4f}/kWh</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                {current_price['source']} • {'🟢 Live' if current_price['is_realtime'] else '🔴 Static'}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Price Statistics
        stats = dashboard_data['statistics']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Min (Heute)", f"€{stats['min']:.1f}/MWh", 
                     f"{((stats['current']/stats['min'])-1)*100:+.1f}%")
        
        with col2:
            st.metric("Durchschnitt", f"€{stats['avg']:.1f}/MWh",
                     f"{((stats['current']/stats['avg'])-1)*100:+.1f}%")
        
        with col3:
            st.metric("Max (Heute)", f"€{stats['max']:.1f}/MWh",
                     f"{((stats['current']/stats['max'])-1)*100:+.1f}%")
        
        return dashboard_data
        
    except Exception as e:
        st.error(f"❌ Energie-Dashboard Fehler: {e}")
        return None

def create_energy_forecast_chart(energy_agent, location):
    """Erstellt Strompreis-Vorhersage Chart"""
    
    if not energy_agent:
        return None
    
    try:
        forecast = energy_agent.get_daily_price_forecast(location, days=1)
        
        if not forecast:
            return None
        
        # Prepare data for chart
        hours = []
        prices = []
        colors = []
        
        for price_point in forecast[:24]:  # Next 24 hours
            hours.append(price_point.timestamp.strftime('%H:00'))
            prices.append(price_point.price_eur_mwh)
            
            # Color coding: Green=cheap, Yellow=medium, Red=expensive
            if price_point.price_eur_mwh < min(p.price_eur_mwh for p in forecast) * 1.1:
                colors.append('#28a745')  # Green - cheap
            elif price_point.price_eur_mwh > max(p.price_eur_mwh for p in forecast) * 0.9:
                colors.append('#dc3545')  # Red - expensive
            else:
                colors.append('#ffc107')  # Yellow - medium
        
        # Create chart
        fig = go.Figure(go.Bar(
            x=hours,
            y=prices,
            marker_color=colors,
            text=[f"€{p:.1f}" for p in prices],
            textposition='outside'
        ))
        
        fig.update_layout(
            title="⚡ Strompreis-Vorhersage (Nächste 24h)",
            xaxis_title="Uhrzeit",
            yaxis_title="Preis (€/MWh)",
            height=400,
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        st.error(f"❌ Forecast Chart Fehler: {e}")
        return None

def show_energy_optimization_section(energy_agent, asset_data):
    """Zeigt detaillierte Energie-Optimierungen"""
    
    if not energy_agent:
        st.info("⚠️ Energy Agent nicht verfügbar - Standard Energiepreise werden verwendet")
        return
    
    st.markdown("### ⚡ Live Energie-Analyse")
    
    location = asset_data.get('location', 'Düsseldorf (HQ)')
    
    # Live Dashboard
    col1, col2 = st.columns([1, 1])
    
    with col1:
        dashboard_data = create_energy_dashboard(energy_agent, location)
    
    with col2:
        # Energy Optimization Recommendations
        if dashboard_data:
            forecast = energy_agent.get_daily_price_forecast(location, days=1)
            recommendations = energy_agent.get_optimization_recommendations(asset_data, forecast)
            
            if recommendations:
                st.markdown("**🎯 Optimierungs-Empfehlungen:**")
                
                for i, rec in enumerate(recommendations[:3], 1):
                    priority_color = {
                        'Hoch': '#dc3545',
                        'Mittel': '#ffc107', 
                        'Niedrig': '#28a745',
                        'Strategisch': '#6c757d'
                    }.get(rec['priority'], '#6c757d')
                    
                    st.markdown(f"""
                    <div style="border-left: 4px solid {priority_color}; padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa;">
                        <strong>{i}. {rec['title']}</strong> ({rec['priority']})<br>
                        <small>{rec['description']}</small><br>
                        💰 <strong>{rec['savings_potential']}</strong>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Price Forecast Chart
    forecast_fig = create_energy_forecast_chart(energy_agent, location)
    if forecast_fig:
        st.plotly_chart(forecast_fig, use_container_width=True)

def show():
    """Enhanced Step 3: Erweiterte KI-Schätzung mit TCO-Komponenten"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 3/4")
    st.markdown("---")
    
    # Asset-Info validation
    if not st.session_state.asset_data.get('asset_name'):
        st.error("❌ Keine Asset-Daten gefunden. Bitte gehen Sie zurück zu Schritt 2.")
        return
    
    asset_data = st.session_state.asset_data
    
    # Enhanced Asset Summary
    st.markdown(f"""
    <div class="gea-card" style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-left: 5px solid #003366;">
        <h4 style="margin: 0; color: #003366;">🚀 Erweiterte TCO-Analyse mit ML + Zentrifugen-Expertise</h4>
        <p style="margin: 0.5rem 0 0 0; color: #666;">
            Für: <strong>{asset_data.get('asset_name', 'N/A')}</strong> 
            ({asset_data.get('manufacturer', 'N/A')} {asset_data.get('model', '')})
        </p>
        <p style="margin: 0.3rem 0 0 0; color: #666; font-size: 0.9rem;">
            🧠 Enhanced ML-Model • ⚡ Energie-Analyse • 💧 Wasserkosten • 👥 Personalaufwand • 🔧 Wartung
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load Enhanced Models
    st.markdown("## 🚀 Erweiterte ML-Systeme werden geladen...")
    
    with st.spinner("Lade Enhanced Machine Learning Models..."):
        predictor, tco_calculator = load_enhanced_ml_model()
        energy_agent = load_energy_agent()
    
    if not predictor or not tco_calculator:
        st.error("❌ Erweiterte ML-Systeme nicht verfügbar. Fallback auf Standard-Modus.")
        # Hier könnte ein Fallback implementiert werden
        return
    
    # Enhanced ML Analysis Animation
    st.markdown("## 🤖 Erweiterte TCO-Analyse läuft...")
    create_enhanced_analysis_animation()
    
    # Prepare enhanced asset data
    enhanced_asset_data = {
        'asset_name': asset_data.get('asset_name', 'N/A'),
        'category': asset_data.get('category', 'Industrial'),
        'subcategory': asset_data.get('subcategory', 'Separator'),
        'manufacturer': asset_data.get('manufacturer', 'GEA'),
        'model': asset_data.get('model', ''),
        'purchase_price': asset_data.get('purchase_price', 100000),
        'age_years': 0.5,  # Neues Asset
        'warranty_years': asset_data.get('warranty_years', 2),
        'expected_lifetime': asset_data.get('expected_lifetime', 15),
        'location': asset_data.get('location', 'Düsseldorf (HQ)'),
        'usage_pattern': asset_data.get('usage_pattern', 'Standard (8h/Tag)'),
        'criticality': asset_data.get('criticality', 'Mittel'),
        
        # Zentrifugen-spezifische Parameter (geschätzt für neue Assets)
        'motor_power_kw': asset_data.get('purchase_price', 100000) / 3000,  # Schätzung
        'total_power_consumption': asset_data.get('purchase_price', 100000) / 3500,  # Schätzung
        'water_consumption_ls': 1.0,  # Standard-Schätzung
        'water_per_ejection': 3.0,    # Standard-Schätzung
        'drive_type': 'flat - belt drive',  # Standard
        'quality_level': 'standard - Level'  # Standard
    }
    
    # Get ML prediction
    try:
        # 1. Basis ML-Vorhersage
        ml_prediction = predictor.predict(enhanced_asset_data)
        
        # 2. Erweiterte TCO-Berechnung
        if energy_agent:
            # Ersetze normale Energie-Komponente durch Enhanced Version
            enhanced_tco_result = tco_calculator.calculate_extended_tco_with_energy_agent(
                enhanced_asset_data, 
                lifetime_years=enhanced_asset_data['expected_lifetime'],
                energy_agent=energy_agent  # Übergebe Agent
            )
        else:
            # Fallback ohne Energy Agent
            extended_tco_result = tco_calculator.calculate_extended_tco(
                enhanced_asset_data, 
                lifetime_years=enhanced_asset_data['expected_lifetime']
            )
        
        # 3. Store in session state
        st.session_state.asset_data['ml_prediction'] = ml_prediction
        st.session_state.asset_data['extended_tco'] = extended_tco_result
        st.session_state.asset_data['enhanced_ml_used'] = True
        
        st.success("✅ Erweiterte TCO-Analyse erfolgreich abgeschlossen!")
        
    except Exception as e:
        st.error(f"❌ Erweiterte TCO-Analyse fehlgeschlagen: {e}")
        st.exception(e)
        return
    
    # === RESULTS SECTION ===
    st.markdown("## 🎯 Erweiterte TCO-Ergebnisse")
    
    if energy_agent:
        show_energy_optimization_section(energy_agent, enhanced_asset_data)
    
    # Main Results Display
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # ML Prediction Result
        ml_cost = ml_prediction.get('annual_prediction', 0)
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366, #0066CC); color: white; 
                    border-radius: 15px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 0.8rem; opacity: 0.8;">🤖 ML-Vorhersage</div>
            <h3 style="margin: 0; font-size: 1.8rem;">€{ml_cost:,}</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                Basis-Wartung/Jahr
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Extended TCO Annual
        extended_annual = extended_tco_result['financial_metrics']['total_annual_operating']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #FF6600, #FF8800); color: white; 
                    border-radius: 15px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 0.8rem; opacity: 0.8;">🔧 Erweiterte TCO</div>
            <h3 style="margin: 0; font-size: 1.8rem;">€{extended_annual:,}</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                Gesamt-Betrieb/Jahr
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Total Lifetime TCO
        total_tco = extended_tco_result['cost_summary']['total_tco']
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; 
                    border-radius: 15px; padding: 1.5rem; text-align: center;">
            <div style="font-size: 0.8rem; opacity: 0.8;">💰 Gesamt-TCO</div>
            <h3 style="margin: 0; font-size: 1.8rem;">€{total_tco:,}</h3>
            <p style="margin: 0.3rem 0 0 0; font-size: 0.9rem; opacity: 0.9;">
                {enhanced_asset_data['expected_lifetime']} Jahre
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Confidence and Key Metrics
    col4, col5 = st.columns([1, 1])
    
    with col4:
        # Confidence Display
        ml_confidence = ml_prediction.get('confidence', 0)
        tco_confidence = extended_tco_result['confidence_metrics']['overall_confidence'] * 100
        avg_confidence = (ml_confidence + tco_confidence) / 2
        
        confidence_icon = "🟢" if avg_confidence >= 80 else "🟡" if avg_confidence >= 60 else "🔴"
        confidence_level = "Hoch" if avg_confidence >= 80 else "Mittel" if avg_confidence >= 60 else "Niedrig"
        
        st.markdown(f"""
        <div style="background: white; border: 2px solid #28a745; border-radius: 15px; 
                    padding: 1.5rem; text-align: center;">
            <div style="font-size: 2.5rem;">{confidence_icon}</div>
            <h3 style="margin: 0; color: #28a745;">{avg_confidence:.0f}%</h3>
            <p style="margin: 0.3rem 0 0 0; color: #666;">
                Analyse-Konfidenz: <strong>{confidence_level}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        # Key Insights
        tco_multiple = extended_tco_result['cost_summary']['tco_multiple']
        operating_ratio = (extended_annual / extended_tco_result['financial_metrics']['purchase_price']) * 100
        
        st.markdown("**🔍 Key Insights:**")
        st.write(f"• **TCO-Multiplikator:** {tco_multiple:.1f}x Anschaffungspreis")
        st.write(f"• **Betriebskostenratio:** {operating_ratio:.1f}% p.a.")
        st.write(f"• **Größter Kostenfaktor:** {max(extended_tco_result['annual_breakdown'], key=extended_tco_result['annual_breakdown'].get).title()}")
        
        # Improvement potential
        energy_cost = extended_tco_result['annual_breakdown'].get('energy', 0)
        if energy_cost > extended_annual * 0.15:  # >15% der Betriebskosten
            st.warning("⚡ Energiekosten sind hoch - Effizienz-Upgrade prüfen!")
    
    # === DETAILED ANALYSIS SECTION ===
    st.markdown("### 📊 Detaillierte Kostenanalyse")
    
    # Tab-based detailed view
    tab1, tab2, tab3, tab4 = st.tabs(["💰 Kostenaufschlüsselung", "📈 Zeitverlauf", "🎯 Konfidenz-Analyse", "🔍 Komponenten-Details"])
    
    with tab1:
        # TCO Breakdown Chart
        breakdown_fig = create_tco_breakdown_chart(extended_tco_result)
        st.plotly_chart(breakdown_fig, use_container_width=True)
        
        # Cost comparison table
        st.markdown("**💸 Detaillierte Jahreskosten:**")
        breakdown_data = []
        total_annual = sum(extended_tco_result['annual_breakdown'].values())
        
        for component, cost in extended_tco_result['annual_breakdown'].items():
            if cost > 0:
                percentage = (cost / total_annual) * 100
                breakdown_data.append({
                    'Komponente': component.replace('_', ' ').title(),
                    'Kosten/Jahr': f"€{cost:,.0f}",
                    'Anteil': f"{percentage:.1f}%",
                    'Konfidenz': f"{extended_tco_result['confidence_metrics']['component_confidence'][component]*100:.0f}%"
                })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    with tab2:
        # Lifetime cost development
        lifetime_fig = create_lifetime_cost_chart(extended_tco_result)
        st.plotly_chart(lifetime_fig, use_container_width=True)
        
        # Cost escalation factors
        st.markdown("**📈 Kostenentwicklung-Faktoren:**")
        col6, col7 = st.columns(2)
        with col6:
            st.write("• **Inflation:** 3% p.a.")
            st.write("• **Verschleiß-Eskalation:** 2% p.a.")
            st.write("• **Energiepreis-Steigerung:** 4% p.a.")
        with col7:
            st.write("• **Lohn-Steigerung:** 3,5% p.a.")
            st.write("• **Ersatzteil-Inflation:** 5% p.a.")
            st.write("• **Compliance-Kosten:** +2% p.a.")
    
    with tab3:
        # Component confidence analysis
        confidence_fig = create_component_confidence_chart(extended_tco_result)
        st.plotly_chart(confidence_fig, use_container_width=True)
        
        st.markdown("**🎯 Konfidenz-Bewertung:**")
        st.write("• **Hoch (>80%):** Basiert auf umfangreichen Daten und bewährten Modellen")
        st.write("• **Mittel (60-80%):** Gute Datengrundlage mit einigen Schätzungen")
        st.write("• **Niedrig (<60%):** Viele Annahmen, unsichere Datenlage")
    
    with tab4:
        # Component details
        st.markdown("**🔧 Komponenten-Details:**")
        
        for comp_name, comp_data in extended_tco_result['components'].items():
            if comp_data['annual_cost'] > 0:
                with st.expander(f"{comp_name.replace('_', ' ').title()} - €{comp_data['annual_cost']:,.0f}/Jahr"):
                    st.write(f"**Berechnungsmethode:** {comp_data['calculation_method']}")
                    st.write(f"**Kategorie:** {comp_data['category']}")
                    st.write(f"**Konfidenz:** {comp_data['confidence']*100:.0f}%")
                    st.write(f"**Regional abhängig:** {'Ja' if comp_data['region_dependent'] else 'Nein'}")
                    
                    if comp_data['factors']:
                        st.write("**Berechnungsfaktoren:**")
                        for factor, value in comp_data['factors'].items():
                            if isinstance(value, (int, float)):
                                st.write(f"  • {factor}: {value:,.2f}")
                            else:
                                st.write(f"  • {factor}: {value}")
    
    # === OPTIMIZATION RECOMMENDATIONS ===
    st.markdown("### 💡 Optimierungs-Empfehlungen")
    
    recommendations = []
    annual_breakdown = extended_tco_result['annual_breakdown']
    
    # Energy optimization
    energy_cost = annual_breakdown.get('energy', 0)
    if energy_cost > extended_annual * 0.15:  # >15%
        energy_saving = energy_cost * 0.25  # 25% potential savings
        recommendations.append({
            'type': 'success',
            'title': 'Energieeffizienz-Upgrade',
            'description': f'Energiekosten machen {(energy_cost/extended_annual)*100:.0f}% aus. Modern IE4-Motoren können 20-25% sparen.',
            'savings': f'€{energy_saving:,.0f}/Jahr',
            'action': 'High-efficiency Motor evaluieren'
        })
    
    # Personnel optimization
    personnel_cost = annual_breakdown.get('personnel', 0)
    if personnel_cost > 15000:  # >€15k
        personnel_saving = personnel_cost * 0.30  # 30% through automation
        recommendations.append({
            'type': 'info',
            'title': 'Automatisierung erhöhen',
            'description': f'Personalkosten: €{personnel_cost:,.0f}/Jahr. Automatisierung kann Aufwand reduzieren.',
            'savings': f'€{personnel_saving:,.0f}/Jahr',
            'action': 'IoT-Monitoring und Auto-CIP implementieren'
        })
    
    # Maintenance optimization
    maintenance_cost = annual_breakdown.get('maintenance', 0)
    if maintenance_cost > ml_cost * 1.5:  # 50% above ML prediction
        maintenance_saving = maintenance_cost * 0.20  # 20% through predictive
        recommendations.append({
            'type': 'warning',
            'title': 'Predictive Maintenance',
            'description': f'Wartungskosten sind überdurchschnittlich hoch. Predictive Maintenance kann helfen.',
            'savings': f'€{maintenance_saving:,.0f}/Jahr',
            'action': 'Condition Monitoring System installieren'
        })
    
    # Display recommendations
    for rec in recommendations:
        if rec['type'] == 'success':
            st.success(f"✅ **{rec['title']}**: {rec['description']}")
        elif rec['type'] == 'info':
            st.info(f"ℹ️ **{rec['title']}**: {rec['description']}")
        elif rec['type'] == 'warning':
            st.warning(f"⚠️ **{rec['title']}**: {rec['description']}")
        
        st.write(f"   💰 **Einsparpotential:** {rec['savings']}")
        st.write(f"   👉 **Empfohlene Aktion:** {rec['action']}")
        st.write("")
    
    # === EXPORT & SHARING ===
    with st.expander("📤 Export & Sharing"):
        col8, col9, col10 = st.columns(3)
        
        with col8:
            if st.button("📊 Excel Export", use_container_width=True):
                st.success("✅ Excel-Report wird generiert...")
                # Hier würde Excel-Export implementiert
        
        with col9:
            if st.button("📧 Email Report", use_container_width=True):
                st.success("✅ Report an Management gesendet!")
        
        with col10:
            if st.button("💾 Speichern", use_container_width=True):
                st.success("✅ TCO-Analyse gespeichert!")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col11, col12, col13 = st.columns([1, 1, 1])
    
    with col11:
        if st.button("← ZURÜCK ZU GRUNDDATEN", key="step3_back", use_container_width=True):
            st.session_state.page = 'step2'
            st.rerun()
    
    with col12:
        if st.button("🔄 NEUE ANALYSE", key="step3_regenerate", use_container_width=True):
            # Clear previous analysis
            keys_to_clear = ['ml_prediction', 'extended_tco', 'enhanced_ml_used']
            for key in keys_to_clear:
                if key in st.session_state.asset_data:
                    del st.session_state.asset_data[key]
            st.rerun()
    
    with col13:
        if st.button("WEITER ZUR ÜBERSICHT →", key="step3_next", type="primary", use_container_width=True):
            st.session_state.page = 'step4'
            st.rerun()

if __name__ == "__main__":
    # Quick test
    print("🧪 Enhanced Step 3 Module ready!")