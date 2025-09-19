import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import json
import time

def calculate_total_tco(asset_data):
    """Berechnet komplette TCO basierend auf allen Daten - FIXED VERSION"""
    
    # FIXED: Prüfe auf enhanced_ml_used und verwende extended_tco falls verfügbar
    if asset_data.get('enhanced_ml_used') and 'extended_tco' in asset_data:
        # Verwende die bereits berechnete erweiterte TCO
        extended_tco = asset_data['extended_tco']
        return {
            'purchase_price': extended_tco['financial_metrics']['purchase_price'],
            'total_maintenance': extended_tco['escalated_costs'].get('maintenance', 0),
            'extended_warranty': 0,  # Bereits in anderen Komponenten enthalten
            'downtime_cost': 0,      # Bereits in Monitoring enthalten
            'training_costs': extended_tco['financial_metrics']['training_cost'],
            'energy_costs': extended_tco['escalated_costs'].get('energy', 0),
            'disposal_costs': extended_tco['financial_metrics']['disposal_cost'],
            'total_tco': extended_tco['cost_summary']['total_tco'],
            'maintenance_by_year': [],  # Vereinfacht für erweiterte TCO
            'annual_average': extended_tco['cost_summary']['annual_average'],
            'lifetime_years': extended_tco['financial_metrics']['lifetime_years'],
            # Zusätzliche erweiterte Komponenten
            'water_costs': extended_tco['escalated_costs'].get('water', 0),
            'personnel_costs': extended_tco['escalated_costs'].get('personnel', 0),
            'monitoring_costs': extended_tco['escalated_costs'].get('monitoring', 0),
            'compliance_costs': extended_tco['escalated_costs'].get('compliance', 0),
            'insurance_costs': extended_tco['escalated_costs'].get('insurance', 0),
            'spare_parts_costs': extended_tco['escalated_costs'].get('spare_parts', 0),
            'cleaning_costs': extended_tco['escalated_costs'].get('cleaning', 0)
        }
    
    # FALLBACK: Traditionelle TCO-Berechnung falls extended_tco nicht verfügbar
    purchase_price = asset_data.get('purchase_price', 0)
    lifetime_years = asset_data.get('expected_lifetime', 5)
    
    # Use AI prediction or manual override
    if 'manual_override' in asset_data:
        annual_maintenance = asset_data['manual_override']
    else:
        # FIXED: Prüfe verschiedene Prediction-Quellen
        ai_prediction = asset_data.get('ai_prediction') or asset_data.get('ml_prediction', {})
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
    """Generiert actionable Empfehlungen - ENHANCED VERSION"""
    
    recommendations = []
    
    # Prüfe ob erweiterte TCO-Daten verfügbar sind
    if asset_data.get('enhanced_ml_used') and 'extended_tco' in asset_data:
        extended_tco = asset_data['extended_tco']
        annual_breakdown = extended_tco['annual_breakdown']
        total_annual = sum(annual_breakdown.values())
        
        # Energiekosten-Optimierung
        energy_cost = annual_breakdown.get('energy', 0)
        if energy_cost > total_annual * 0.10:  # >10% der Betriebskosten
            recommendations.append({
                'type': 'success',
                'title': 'Energieeffizienz-Upgrade',
                'description': f'Energiekosten: €{energy_cost:,.0f}/Jahr ({(energy_cost/total_annual)*100:.1f}% der Betriebskosten). IE4-Motoren können 15-25% sparen.',
                'action': 'High-efficiency Motor evaluieren'
            })
        
        # Personalkosten-Optimierung
        personnel_cost = annual_breakdown.get('personnel', 0)
        if personnel_cost > 10000:  # >€10k
            recommendations.append({
                'type': 'info',
                'title': 'Automatisierung erhöhen',
                'description': f'Personalkosten: €{personnel_cost:,.0f}/Jahr. IoT-Monitoring kann Aufwand um 20-30% reduzieren.',
                'action': 'Condition Monitoring System implementieren'
            })
        
        # Wartungskosten-Optimierung
        maintenance_cost = annual_breakdown.get('maintenance', 0)
        spare_parts_cost = annual_breakdown.get('spare_parts', 0)
        if (maintenance_cost + spare_parts_cost) > total_annual * 0.20:  # >20%
            recommendations.append({
                'type': 'warning',
                'title': 'Predictive Maintenance',
                'description': f'Wartungs- und Ersatzteilkosten: €{maintenance_cost + spare_parts_cost:,.0f}/Jahr. Predictive Maintenance kann 15-20% sparen.',
                'action': 'Vibrations- und Temperatur-Monitoring installieren'
            })
        
        # Compliance-Optimierung
        compliance_cost = annual_breakdown.get('compliance', 0)
        if compliance_cost > 2000:  # >€2k
            recommendations.append({
                'type': 'info',
                'title': 'Compliance-Effizienz',
                'description': f'Compliance-Kosten: €{compliance_cost:,.0f}/Jahr. Digitale Dokumentation kann Aufwand reduzieren.',
                'action': 'Digitales Compliance-Management System'
            })
        
    else:
        # Fallback auf traditionelle Empfehlungen
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
        'ai_prediction': asset_data.get('ai_prediction') or asset_data.get('ml_prediction', {}),
        'extended_tco': asset_data.get('extended_tco', {}),
        'similar_assets': asset_data.get('similar_assets', []),
        'enhanced_ml_used': asset_data.get('enhanced_ml_used', False)
    }
    
    return json.dumps(export_data, indent=2, default=str)

def show():
    """Step 4: Finale TCO-Übersicht und Asset-Speicherung - FIXED VERSION"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 4/4")
    st.markdown("---")
    
    # FIXED: Verbesserte Datenvalidierung
    asset_data = st.session_state.asset_data
    
    # Prüfe Asset-Name
    if not asset_data.get('asset_name'):
        st.error("❌ Asset-Name fehlt. Bitte gehen Sie zurück zu Schritt 2.")
        return
    
    # FIXED: Prüfe auf verschiedene Prediction-Quellen
    has_prediction = (
        'ai_prediction' in asset_data or 
        'ml_prediction' in asset_data or 
        'extended_tco' in asset_data
    )
    
    if not has_prediction:
        st.error("❌ Keine KI-Vorhersage gefunden. Bitte gehen Sie zurück zu Schritt 3.")
        return
    
    # Debug-Informationen (optional anzeigen)
    with st.expander("🔍 Debug: Verfügbare Daten"):
        st.write("**Asset Data Keys:**", list(asset_data.keys()))
        if 'ai_prediction' in asset_data:
            st.write("✅ ai_prediction vorhanden")
        if 'ml_prediction' in asset_data:
            st.write("✅ ml_prediction vorhanden")
        if 'extended_tco' in asset_data:
            st.write("✅ extended_tco vorhanden")
        st.write("**Enhanced ML Used:**", asset_data.get('enhanced_ml_used', False))
    
    # TCO-Daten berechnen
    tco_data = calculate_total_tco(asset_data)
    
    # Success Header
    analysis_type = "Erweiterte TCO-Analyse" if asset_data.get('enhanced_ml_used') else "Standard TCO-Analyse"
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #28a745, #20c997); color: white; 
                border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
        <h1 style="margin: 0; font-size: 2.5rem;">🎉 {analysis_type} abgeschlossen!</h1>
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
        ownership_multiplier = tco_data['total_tco'] / tco_data['purchase_price'] if tco_data['purchase_price'] > 0 else 0
        st.markdown(f"""
        <div style="background: #0066CC; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">{ownership_multiplier:.1f}x</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Anschaffungspreis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # FIXED: Konfidenz aus verschiedenen Quellen
        confidence = 0
        if asset_data.get('enhanced_ml_used') and 'extended_tco' in asset_data:
            confidence = asset_data['extended_tco']['confidence_metrics']['overall_confidence'] * 100
        else:
            ai_prediction = asset_data.get('ai_prediction') or asset_data.get('ml_prediction', {})
            confidence = ai_prediction.get('confidence', 50)
        
        st.markdown(f"""
        <div style="background: #28a745; color: white; border-radius: 10px; padding: 1.5rem; text-align: center;">
            <h2 style="margin: 0; font-size: 2rem;">{confidence:.0f}%</h2>
            <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Analyse-Konfidenz</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced TCO Breakdown (if available)
    if asset_data.get('enhanced_ml_used') and 'extended_tco' in asset_data:
        st.markdown("## 📊 Erweiterte TCO-Aufschlüsselung")
        
        extended_tco = asset_data['extended_tco']
        annual_breakdown = extended_tco['annual_breakdown']
        
        # Filter out zero components
        filtered_breakdown = {k: v for k, v in annual_breakdown.items() if v > 0}
        
        col5, col6 = st.columns([2, 1])
        
        with col5:
            # Enhanced Pie Chart
            fig_pie = px.pie(
                values=list(filtered_breakdown.values()),
                names=[name.replace('_', ' ').title() for name in filtered_breakdown.keys()],
                title="Jährliche TCO-Komponenten",
                color_discrete_sequence=['#003366', '#FF6600', '#0066CC', '#28a745', '#ffc107', '#dc3545', '#6c757d', '#6f42c1', '#20c997']
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col6:
            st.markdown("**💸 Detaillierte Jahreskosten:**")
            
            # Enhanced breakdown table
            breakdown_data = []
            total_annual = sum(filtered_breakdown.values())
            
            for component, cost in sorted(filtered_breakdown.items(), key=lambda x: x[1], reverse=True):
                percentage = (cost / total_annual) * 100
                confidence = extended_tco['confidence_metrics']['component_confidence'][component]
                
                breakdown_data.append({
                    'Komponente': component.replace('_', ' ').title(),
                    'Kosten/Jahr': f"€{cost:,.0f}",
                    'Anteil': f"{percentage:.1f}%",
                    'Konfidenz': f"{confidence*100:.0f}%"
                })
            
            breakdown_df = pd.DataFrame(breakdown_data)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    else:
        # Standard TCO Breakdown
        st.markdown("## 📊 TCO-Kostenaufschlüsselung")
        
        col5, col6 = st.columns([1, 1])
        
        with col5:
            # Standard Pie Chart für TCO Components
            tco_components = {
                'Anschaffung': tco_data['purchase_price'],
                'Wartung': tco_data['total_maintenance'],
                'Energie': tco_data.get('energy_costs', 0),
                'Training': tco_data.get('training_costs', 0),
                'Entsorgung': tco_data.get('disposal_costs', 0)
            }
            
            # Remove zero components
            tco_components = {k: v for k, v in tco_components.items() if v > 0}
            
            fig_pie = px.pie(
                values=list(tco_components.values()),
                names=list(tco_components.keys()),
                title="TCO-Komponenten",
                color_discrete_sequence=['#003366', '#FF6600', '#0066CC', '#28a745', '#ffc107']
            )
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col6:
            # Cost breakdown table
            st.markdown("**💸 Kostenaufstellung:**")
            
            breakdown_data = []
            for component, cost in tco_components.items():
                if cost > 0:
                    percentage = (cost / tco_data['total_tco']) * 100
                    breakdown_data.append({
                        'Kategorie': component,
                        'Kosten': f"€{cost:,.0f}",
                        'Anteil': f"{percentage:.1f}%"
                    })
            
            breakdown_df = pd.DataFrame(breakdown_data)
            st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
    
    # Recommendations Section
    st.markdown("## 💡 Empfehlungen & Next Steps")
    
    recommendations = generate_recommendations(asset_data, tco_data)
    
    if recommendations:
        for rec in recommendations:
            if rec['type'] == 'warning':
                st.warning(f"⚠️ **{rec['title']}**: {rec['description']}")
            elif rec['type'] == 'info':
                st.info(f"ℹ️ **{rec['title']}**: {rec['description']}")
            elif rec['type'] == 'success':
                st.success(f"✅ **{rec['title']}**: {rec['description']}")
            
            st.write(f"   👉 **Empfohlene Aktion:** {rec['action']}")
    else:
        st.info("💡 **Optimale Konfiguration**: Ihre TCO-Werte liegen im erwarteten Bereich. Regelmäßige Wartung beibehalten.")
    
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
        
        # Analysis type info
        analysis_info = "Enhanced ML + TCO Components" if asset_data.get('enhanced_ml_used') else "Standard ML + Rules"
        st.write(f"• **Analyse-Typ:** {analysis_info}")
    
    with col8:
        st.markdown("**💰 Finanz-Details:**")
        st.write(f"• **Anschaffung:** €{asset_data.get('purchase_price', 0):,.2f}")
        st.write(f"• **Anschaffungsdatum:** {asset_data.get('purchase_date', 'N/A')}")
        st.write(f"• **Nutzungsdauer:** {asset_data.get('expected_lifetime', 5)} Jahre")
        st.write(f"• **Kritikalität:** {asset_data.get('criticality', 'Mittel')}")
        
        # Show prediction details
        if asset_data.get('enhanced_ml_used') and 'extended_tco' in asset_data:
            annual_operating = asset_data['extended_tco']['financial_metrics']['total_annual_operating']
            st.write(f"• **Jährliche Betriebskosten:** €{annual_operating:,.0f}")
        else:
            ai_prediction = asset_data.get('ai_prediction') or asset_data.get('ml_prediction', {})
            if 'manual_override' in asset_data:
                st.write(f"• **Angepasste Wartung:** €{asset_data['manual_override']:,.0f}/Jahr")
            elif ai_prediction:
                st.write(f"• **ML-Wartungsvorhersage:** €{ai_prediction.get('annual_prediction', 0):,.0f}/Jahr")
        
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
                file_name=f"TCO_Analysis_{asset_data.get('asset_name', 'Asset').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
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
        if st.button("← ZURÜCK ZUR ANALYSE", key="step4_back", use_container_width=True):
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
            time.sleep(1)  # Brief celebration
            st.rerun()

if __name__ == "__main__":
    print("🔧 Fixed Step 4 Module ready!")