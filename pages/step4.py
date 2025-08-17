import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json

def calculate_total_tco(asset_data):
    """Berechnet komplette TCO basierend auf allen Daten"""
    
    purchase_price = asset_data.get('purchase_price', 0)
    lifetime_years = asset_data.get('expected_lifetime', 5)
    
    # Use AI prediction or manual override
    if 'manual_override' in asset_data:
        annual_maintenance = asset_data['manual_override']
    else:
        ai_prediction = asset_data.get('ai_prediction', {})
        annual_maintenance = ai_prediction.get('annual_prediction', purchase_price * 0.15)
    
    # Calculate escalating maintenance costs
    total_maintenance = 0
    maintenance_by_year = []
    
    for year in range(1, lifetime_years + 1):
        # 5% escalation per year + wear factor
        escalation = 1 + (year * 0.05)
        wear_factor = 1 + (year * 0.02)  # Components wear out
        yearly_cost = annual_maintenance * escalation * wear_factor
        
        total_maintenance += yearly_cost
        maintenance_by_year.append({
            'year': year,
            'cost': yearly_cost,
            'cumulative': total_maintenance
        })
    
    # Additional TCO components
    warranty_years = asset_data.get('warranty_years', 1)
    criticality = asset_data.get('criticality', 'Mittel')
    
    # Extended warranty costs (after initial warranty expires)
    extended_warranty = 0
    if lifetime_years > warranty_years:
        extended_years = lifetime_years - warranty_years
        extended_warranty = purchase_price * 0.08 * extended_years  # 8% per year
    
    # Downtime costs (based on criticality)
    downtime_multipliers = {
        'Niedrig': 0.02, 'Mittel': 0.05, 'Hoch': 0.10, 'Kritisch': 0.20
    }
    estimated_downtime_cost = purchase_price * downtime_multipliers.get(criticality, 0.05)
    
    # Training/Setup costs (one-time)
    training_costs = purchase_price * 0.03  # 3% of purchase price
    
    # End-of-life disposal costs
    disposal_costs = purchase_price * 0.02  # 2% for disposal/recycling
    
    # Energy costs (rough estimate for powered equipment)
    category = asset_data.get('category', '')
    if category in ['IT-Equipment', 'Industrial']:
        annual_energy = purchase_price * 0.05  # 5% of purchase price annually
        total_energy = annual_energy * lifetime_years
    else:
        total_energy = 0
    
    # Total TCO calculation
    total_tco = (purchase_price + total_maintenance + extended_warranty + 
                 estimated_downtime_cost + training_costs + disposal_costs + total_energy)
    
    return {
        'purchase_price': purchase_price,
        'total_maintenance': total_maintenance,
        'extended_warranty': extended_warranty,
        'downtime_cost': estimated_downtime_cost,
        'training_costs': training_costs,
        'energy_costs': total_energy,
        'disposal_costs': disposal_costs,
        'total_tco': total_tco,
        'maintenance_by_year': maintenance_by_year,
        'annual_average': total_tco / lifetime_years,
        'lifetime_years': lifetime_years
    }

def generate_recommendations(asset_data, tco_data):
    """Generiert actionable Empfehlungen"""
    
    recommendations = []
    
    # Cost optimization recommendations
    maintenance_ratio = tco_data['total_maintenance'] / tco_data['purchase_price']
    if maintenance_ratio > 1.0:  # Maintenance > Purchase price
        recommendations.append({
            'type': 'warning',
            'title': 'Hohe Wartungskosten erkannt',
            'description': f'Wartungskosten ({maintenance_ratio:.1%}) übersteigen Anschaffungskosten. Prüfen Sie Leasing-Optionen.',
            'action': 'Leasing-Vergleich durchführen'
        })
    
    # Warranty recommendations
    warranty_years = asset_data.get('warranty_years', 1)
    lifetime = asset_data.get('expected_lifetime', 5)
    if warranty_years < lifetime * 0.6:  # Less than 60% coverage
        recommendations.append({
            'type': 'info',
            'title': 'Garantie-Verlängerung empfohlen',
            'description': f'Nur {warranty_years} Jahre Garantie bei {lifetime} Jahren Nutzung. Verlängerung könnte sich lohnen.',
            'action': 'Extended Warranty prüfen'
        })
    
    # Energy efficiency recommendations
    category = asset_data.get('category', '')
    if category in ['IT-Equipment', 'Industrial'] and tco_data['energy_costs'] > 0:
        recommendations.append({
            'type': 'success',
            'title': 'Energieeffizienz optimieren',
            'description': f'Energiekosten: €{tco_data["energy_costs"]:,.0f}. Moderne Geräte können 20-30% sparen.',
            'action': 'Energy Star Modelle vergleichen'
        })
    
    # Predictive maintenance recommendation
    if asset_data.get('criticality') in ['Hoch', 'Kritisch']:
        recommendations.append({
            'type': 'info',
            'title': 'Predictive Maintenance implementieren',
            'description': 'Bei kritischen Assets kann IoT-Monitoring Ausfälle um 40% reduzieren.',
            'action': 'IoT-Sensoren evaluieren'
        })
    
    return recommendations

def export_to_json(asset_data, tco_data):
    """Exportiert alle Daten als JSON für weitere Verarbeitung"""
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'asset_info': {
            'name': asset_data.get('asset_name', ''),
            'category': asset_data.get('category', ''),
            'subcategory': asset_data.get('subcategory', ''),
            'manufacturer': asset_data.get('manufacturer', ''),
            'model': asset_data.get('model', ''),
            'purchase_price': asset_data.get('purchase_price', 0),
            'purchase_date': str(asset_data.get('purchase_date', '')),
            'location': asset_data.get('location', ''),
            'cost_center': asset_data.get('cost_center', '')
        },
        'tco_analysis': tco_data,
        'ai_prediction': asset_data.get('ai_prediction', {}),
        'similar_assets': asset_data.get('similar_assets', [])
    }
    
    return json.dumps(export_data, indent=2, default=str)

def show():
    """Step 4: Finale TCO-Übersicht und Asset-Speicherung"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 4/4")
    st.markdown("---")
    
    # Validate we have all necessary data
    if not st.session_state.asset_data.get('asset_name') or not st.session_state.asset_data.get('ai_prediction'):
        st.error("❌ Unvollständige Daten. Bitte durchlaufen Sie alle vorherigen Schritte.")
        return
    
    asset_data = st.session_state.asset_data
    tco_data = calculate_total_tco(asset_data)
    
    # Success Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; 
                border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
        <h1 style="margin: 0; font-size: 2.5rem;">🎉 TCO-Analyse abgeschlossen!</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Für Asset: <strong>{asset_data.get('asset_name', 'N/A')}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary - The Money Shot
    st.markdown("## 💰 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div style="background: #003366; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">€{tco_data['total_tco']:,.0f}</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Gesamt-TCO ({tco_data['lifetime_years']} Jahre)</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: #FF6600; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">€{tco_data['annual_average']:,.0f}</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Durchschnitt/Jahr</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        ownership_multiplier = tco_data['total_tco'] / tco_data['purchase_price']
        st.markdown(f"""
        <div style="background: #0066CC; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">{ownership_multiplier:.1f}x</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Anschaffungspreis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        ai_confidence = asset_data.get('ai_prediction', {}).get('confidence', 0)
        st.markdown(f"""
        <div style="background: #28a745; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">{ai_confidence}%</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">KI-Konfidenz</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed TCO Breakdown
    st.markdown("## 📊 TCO-Kostenaufschlüsselung")
    
    col5, col6 = st.columns([1, 1])
    
    with col5:
        # Pie Chart für TCO Components
        tco_components = {
            'Anschaffung': tco_data['purchase_price'],
            'Wartung': tco_data['total_maintenance'],
            'Garantie-Verlängerung': tco_data['extended_warranty'],
            'Ausfallzeiten': tco_data['downtime_cost'],
            'Training': tco_data['training_costs'],
            'Energie': tco_data['energy_costs'],
            'Entsorgung': tco_data['disposal_costs']
        }
        
        # Remove zero components
        tco_components = {k: v for k, v in tco_components.items() if v > 0}
        
        fig_pie = px.pie(
            values=list(tco_components.values()),
            names=list(tco_components.keys()),
            title="TCO-Komponenten",
            color_discrete_sequence=['#003366', '#FF6600', '#0066CC', '#28a745', '#ffc107', '#dc3545', '#6c757d']
        )
        fig_pie.update_layout(height=400)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col6:
        # Cost breakdown table
        st.markdown("**💸 Detaillierte Kostenaufstellung:**")
        
        breakdown_data = []
        for component, cost in tco_components.items():
            percentage = (cost / tco_data['total_tco']) * 100
            breakdown_data.append({
                'Kategorie': component,
                'Kosten': f"€{cost:,.0f}",
                'Anteil': f"{percentage:.1f}%"
            })
        
        breakdown_df = pd.DataFrame(breakdown_data)
        st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
        
        # Key insights
        st.markdown("**🔍 Key Insights:**")
        maintenance_pct = (tco_data['total_maintenance'] / tco_data['total_tco']) * 100
        
        if maintenance_pct > 60:
            st.warning(f"⚠️ Wartung macht {maintenance_pct:.0f}% der TCO aus")
        elif maintenance_pct > 40:
            st.info(f"ℹ️ Wartung macht {maintenance_pct:.0f}% der TCO aus")
        else:
            st.success(f"✅ Wartung macht nur {maintenance_pct:.0f}% der TCO aus")
    
    # Timeline Chart
    st.markdown("### 📈 TCO-Entwicklung über Lebensdauer")
    
    # Prepare timeline data
    timeline_data = []
    cumulative_cost = tco_data['purchase_price']  # Start with purchase
    
    timeline_data.append({
        'Jahr': 0,
        'Jährliche Kosten': tco_data['purchase_price'],
        'Kumulative TCO': cumulative_cost,
        'Typ': 'Anschaffung'
    })
    
    for year_data in tco_data['maintenance_by_year']:
        year = year_data['year']
        annual_cost = year_data['cost']
        cumulative_cost += annual_cost
        
        timeline_data.append({
            'Jahr': year,
            'Jährliche Kosten': annual_cost,
            'Kumulative TCO': cumulative_cost,
            'Typ': 'Wartung'
        })
    
    timeline_df = pd.DataFrame(timeline_data)
    
    # Create dual-axis chart
    fig_timeline = go.Figure()
    
    # Annual costs (bars)
    fig_timeline.add_trace(go.Bar(
        x=timeline_df['Jahr'],
        y=timeline_df['Jährliche Kosten'],
        name='Jährliche Kosten',
        marker_color=['#003366' if t == 'Anschaffung' else '#FF6600' for t in timeline_df['Typ']],
        yaxis='y'
    ))
    
    # Cumulative TCO (line)
    fig_timeline.add_trace(go.Scatter(
        x=timeline_df['Jahr'],
        y=timeline_df['Kumulative TCO'],
        mode='lines+markers',
        name='Kumulative TCO',
        line=dict(color='#28a745', width=3),
        yaxis='y2'
    ))
    
    fig_timeline.update_layout(
        title='TCO-Entwicklung: Jährliche Kosten vs. Kumulative TCO',
        xaxis_title='Jahr',
        yaxis=dict(title='Jährliche Kosten (€)', side='left'),
        yaxis2=dict(title='Kumulative TCO (€)', side='right', overlaying='y'),
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Recommendations Section
    st.markdown("## 💡 Empfehlungen & Next Steps")
    
    recommendations = generate_recommendations(asset_data, tco_data)
    
    for rec in recommendations:
        if rec['type'] == 'warning':
            st.warning(f"⚠️ **{rec['title']}**: {rec['description']}")
            st.write(f"   👉 **Empfohlene Aktion:** {rec['action']}")
        elif rec['type'] == 'info':
            st.info(f"ℹ️ **{rec['title']}**: {rec['description']}")
            st.write(f"   👉 **Empfohlene Aktion:** {rec['action']}")
        elif rec['type'] == 'success':
            st.success(f"✅ **{rec['title']}**: {rec['description']}")
            st.write(f"   👉 **Empfohlene Aktion:** {rec['action']}")
    
    # Asset Summary Card
    st.markdown("## 📋 Asset-Zusammenfassung")
    
    col7, col8 = st.columns([1, 1])
    
    with col7:
        st.markdown("**🏷️ Asset-Details:**")
        st.write(f"• **Name:** {asset_data.get('asset_name', 'N/A')}")
        st.write(f"• **Typ:** {asset_data.get('category', 'N/A')} → {asset_data.get('subcategory', 'N/A')}")
        st.write(f"• **Hersteller:** {asset_data.get('manufacturer', 'N/A')}")
        if asset_data.get('model'):
            st.write(f"• **Modell:** {asset_data.get('model')}")
        st.write(f"• **Standort:** {asset_data.get('location', 'N/A')}")
        st.write(f"• **Kostenstelle:** {asset_data.get('cost_center', 'N/A')}")
    
    with col8:
        st.markdown("**💰 Finanz-Details:**")
        st.write(f"• **Anschaffung:** €{asset_data.get('purchase_price', 0):,.2f}")
        st.write(f"• **Anschaffungsdatum:** {asset_data.get('purchase_date', 'N/A')}")
        st.write(f"• **Nutzungsdauer:** {asset_data.get('expected_lifetime', 5)} Jahre")
        st.write(f"• **Kritikalität:** {asset_data.get('criticality', 'Mittel')}")
        if 'manual_override' in asset_data:
            st.write(f"• **Angepasste Wartung:** €{asset_data['manual_override']:,.0f}/Jahr")
        st.write(f"• **Gesamt-TCO:** €{tco_data['total_tco']:,.0f}")
    
    # Export & Actions
    st.markdown("## 📤 Export & Aktionen")
    
    col9, col10, col11 = st.columns(3)
    
    with col9:
        # JSON Export
        if st.button("📄 JSON Export", use_container_width=True):
            json_data = export_to_json(asset_data, tco_data)
            st.download_button(
                label="💾 JSON herunterladen",
                data=json_data,
                file_name=f"TCO_Analysis_{asset_data.get('asset_name', 'Asset')}_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with col10:
        # Email Report (simulated)
        if st.button("📧 Report versenden", use_container_width=True):
            st.success("✅ TCO-Report wurde an das Management-Team gesendet!")
            st.balloons()
    
    with col11:
        # Add to monitoring
        if st.button("📊 Monitoring aktivieren", use_container_width=True):
            st.success("✅ Asset wurde zum TCO-Monitoring hinzugefügt!")
    
    # Final Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col12, col13, col14 = st.columns([1, 1, 1])
    
    with col12:
        if st.button("← ZURÜCK ZUR KI-ANALYSE", key="step4_back", use_container_width=True):
            st.session_state.page = 'step3'
            st.rerun()
    
    with col13:
        if st.button("🔄 NEUES ASSET STARTEN", key="step4_new", use_container_width=True):
            st.session_state.asset_data = {}  # Reset everything
            st.session_state.page = 'step1'
            st.rerun()
    
    with col14:
        if st.button("🏠 ZURÜCK ZUM DASHBOARD", key="step4_home", type="primary", use_container_width=True):
            # Asset zu "gespeicherten Assets" hinzufügen (simulation)
            st.session_state.page = 'dashboard'
            st.success("✅ Asset erfolgreich gespeichert!")
            st.balloons()
            time.sleep(2)  # Brief celebration
            st.rerun()