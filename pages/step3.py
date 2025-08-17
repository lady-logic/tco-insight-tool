import streamlit as st
import time
import random
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

def calculate_ai_prediction(asset_data):
    """Simuliert KI-Vorhersage basierend auf Asset-Daten"""
    
    # Base maintenance rates by category/subcategory
    base_rates = {
        # IT-Equipment
        "Server": 0.18, "Laptop": 0.12, "Workstation": 0.15, "Netzwerk": 0.10,
        # Industrial
        "Separator": 0.14, "Homogenizer": 0.16, "Pump": 0.12, "Pasteurizer": 0.13,
        # Software  
        "ERP": 0.20, "CAD": 0.18, "Office": 0.15, "Analyse": 0.16,
        # Other
        "PKW": 0.08, "LKW": 0.12, "HVAC": 0.10, "Security": 0.08
    }
    
    # Manufacturer reliability factors
    manufacturer_factors = {
        # Premium brands
        "Dell": 1.05, "Siemens": 1.15, "GEA": 1.10, "SAP": 1.20,
        # Standard brands  
        "HP": 1.00, "Lenovo": 0.95, "Alfa Laval": 1.00, "Microsoft": 1.00,
        # Budget options
        "Generic": 0.85, "No-Name": 0.80
    }
    
    # Location factors (based on environment, support availability)
    location_factors = {
        "Düsseldorf (HQ)": 0.95,    # Best support
        "Oelde": 1.00,              # Production site
        "Berlin": 1.05,             # Remote office
        "Shanghai": 1.15,           # International
        "Andere": 1.20              # Unknown/difficult
    }
    
    # Criticality factors
    criticality_factors = {
        "Niedrig": 0.80,    # Basic maintenance
        "Mittel": 1.00,     # Standard
        "Hoch": 1.30,       # Premium support
        "Kritisch": 1.60    # 24/7 support
    }
    
    # Usage pattern factors
    usage_factors = {
        "Standard (8h/Tag)": 1.00,
        "Extended (12h/Tag)": 1.25,
        "24/7 Betrieb": 1.80,
        "Gelegentlich": 0.70
    }
    
    # Get factors
    subcategory = asset_data.get('subcategory', 'Server')
    manufacturer = asset_data.get('manufacturer', 'Standard')
    location = asset_data.get('location', 'Düsseldorf (HQ)')
    criticality = asset_data.get('criticality', 'Mittel')
    usage = asset_data.get('usage_pattern', 'Standard (8h/Tag)')
    price = asset_data.get('purchase_price', 10000)
    
    # Calculate base annual maintenance
    base_rate = base_rates.get(subcategory, 0.15)
    mfg_factor = manufacturer_factors.get(manufacturer, 1.0)
    loc_factor = location_factors.get(location, 1.0)
    crit_factor = criticality_factors.get(criticality, 1.0)
    usage_factor = usage_factors.get(usage, 1.0)
    
    # Age factor (newer = less maintenance first years)
    purchase_date = asset_data.get('purchase_date', datetime.now().date())
    age_years = (datetime.now().date() - purchase_date).days / 365
    age_factor = max(0.7, 1.0 + (age_years * 0.1))  # 10% increase per year
    
    # Calculate prediction
    annual_maintenance = (price * base_rate * mfg_factor * loc_factor * 
                         crit_factor * usage_factor * age_factor)
    
    # Add realistic variance
    variance = random.uniform(0.85, 1.15)  # ±15% variance
    final_prediction = annual_maintenance * variance
    
    # Calculate confidence based on data completeness
    confidence_factors = {
        'manufacturer': 0.15 if manufacturer != 'Bitte wählen...' else 0,
        'model': 0.10 if asset_data.get('model', '') else 0,
        'usage_pattern': 0.15,
        'criticality': 0.10,
        'location': 0.10,
        'warranty': 0.05 if asset_data.get('warranty_years', 0) > 0 else 0
    }
    
    base_confidence = 0.35  # Minimum confidence
    total_confidence = base_confidence + sum(confidence_factors.values())
    confidence_variance = random.uniform(0.95, 1.05)
    final_confidence = min(0.95, total_confidence * confidence_variance)
    
    # Determine confidence level and color
    if final_confidence >= 0.85:
        confidence_level = "Sehr Hoch"
        confidence_color = "success"
        confidence_icon = "🟢"
    elif final_confidence >= 0.70:
        confidence_level = "Hoch" 
        confidence_color = "success"
        confidence_icon = "🟢"
    elif final_confidence >= 0.55:
        confidence_level = "Mittel"
        confidence_color = "warning"
        confidence_icon = "🟡"
    else:
        confidence_level = "Niedrig"
        confidence_color = "error"
        confidence_icon = "🔴"
    
    return {
        'annual_prediction': round(final_prediction),
        'confidence': round(final_confidence * 100),
        'confidence_level': confidence_level,
        'confidence_color': confidence_color,
        'confidence_icon': confidence_icon,
        'range_min': round(final_prediction * 0.75),
        'range_max': round(final_prediction * 1.25),
        'factors_used': {
            'base_rate': f"{base_rate*100:.1f}%",
            'manufacturer': f"{mfg_factor:.2f}x",
            'location': f"{loc_factor:.2f}x", 
            'criticality': f"{crit_factor:.2f}x",
            'usage': f"{usage_factor:.2f}x",
            'age': f"{age_factor:.2f}x"
        }
    }

def get_similar_assets(asset_data):
    """Findet ähnliche Assets für Benchmark"""
    
    # Mock similar assets based on category
    subcategory = asset_data.get('subcategory', 'Server')
    manufacturer = asset_data.get('manufacturer', 'Dell')
    price = asset_data.get('purchase_price', 10000)
    
    similar_assets = []
    
    if subcategory == "Server":
        similar_assets = [
            {"name": "SRV-DUS-003", "manufacturer": "Dell", "model": "PowerEdge R730", 
             "price": 7800, "maintenance": 1560, "location": "München", "age": "2 Jahre"},
            {"name": "SRV-BER-012", "manufacturer": "HP", "model": "ProLiant DL380", 
             "price": 8200, "maintenance": 1640, "location": "Berlin", "age": "1 Jahr"},
            {"name": "SRV-HH-007", "manufacturer": "Dell", "model": "PowerEdge R740", 
             "price": 9100, "maintenance": 1820, "location": "Hamburg", "age": "3 Jahre"}
        ]
    elif subcategory == "Separator":
        similar_assets = [
            {"name": "SEP-A15", "manufacturer": "GEA", "model": "WSP 4000",
             "price": 98000, "maintenance": 14700, "location": "Oelde", "age": "2 Jahre"},
            {"name": "SEP-B08", "manufacturer": "Alfa Laval", "model": "WSPX 5500",
             "price": 115000, "maintenance": 17250, "location": "Kopenhagen", "age": "1 Jahr"},
            {"name": "SEP-C12", "manufacturer": "GEA", "model": "WSP 5200", 
             "price": 108000, "maintenance": 16200, "location": "Düsseldorf", "age": "4 Jahre"}
        ]
    else:
        # Generic similar assets
        base_price = price
        for i in range(3):
            price_var = base_price * random.uniform(0.8, 1.2)
            maintenance_var = price_var * random.uniform(0.12, 0.18)
            similar_assets.append({
                "name": f"{subcategory}-{random.randint(100,999)}", 
                "manufacturer": random.choice([manufacturer, "Andere"]),
                "model": f"Model {chr(65+i)}",
                "price": round(price_var),
                "maintenance": round(maintenance_var),
                "location": random.choice(["Düsseldorf", "Berlin", "München"]),
                "age": f"{random.randint(1,5)} Jahre"
            })
    
    return similar_assets

def show():
    """Step 3: KI-Schätzung durchführen"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 3/4")
    st.markdown("---")
    
    # Asset-Info aus vorherigen Schritten
    if not st.session_state.asset_data.get('asset_name'):
        st.error("❌ Keine Asset-Daten gefunden. Bitte gehen Sie zurück zu Schritt 2.")
        return
    
    asset_data = st.session_state.asset_data
    
    # Asset Summary
    st.markdown(f"""
    <div class="gea-card" style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-left: 5px solid #28a745;">
        <h4 style="margin: 0; color: #003366;">🤖 KI-basierte Kostenschätzung</h4>
        <p style="margin: 0.5rem 0 0 0; color: #666;">
            Für: <strong>{asset_data.get('asset_name', 'N/A')}</strong> 
            ({asset_data.get('manufacturer', 'N/A')} {asset_data.get('model', '')})
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Processing Animation
    st.markdown("## 🧠 KI-Analyse läuft...")
    
    # Progress container
    progress_container = st.empty()
    status_container = st.empty()
    
    # Simulate AI processing with progress bar
    analysis_steps = [
        "🔍 Analysiere Asset-Eigenschaften...",
        "📊 Durchsuche historische Daten...", 
        "🎯 Finde ähnliche Assets...",
        "🧮 Berechne Wartungskosten...",
        "📈 Validiere Schätzung...",
        "✅ Analyse abgeschlossen!"
    ]
    
    # Animated progress
    for i, step in enumerate(analysis_steps):
        progress = (i + 1) / len(analysis_steps)
        progress_container.progress(progress)
        status_container.write(f"**{step}**")
        time.sleep(random.uniform(0.5, 1.5))  # Realistic delay
    
    # Clear progress indicators
    progress_container.empty()
    status_container.empty()
    
    # Generate AI prediction
    prediction = calculate_ai_prediction(asset_data)
    similar_assets = get_similar_assets(asset_data)
    
    # Store prediction in session state
    st.session_state.asset_data['ai_prediction'] = prediction
    st.session_state.asset_data['similar_assets'] = similar_assets
    
    # Results Section
    st.markdown("## 🎯 Ergebnisse der KI-Analyse")
    
    # Main prediction display
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Prediction result card
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366, #0066CC); color: white; 
                    border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <h2 style="margin: 0; font-size: 2.5rem;">€{prediction['annual_prediction']:,}</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Geschätzte jährliche Wartungskosten
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Range display
        st.markdown(f"""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 1rem; text-align: center;">
            <strong>Erwarteter Bereich:</strong> €{prediction['range_min']:,} - €{prediction['range_max']:,}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Confidence indicator
        confidence_color_map = {
            "success": "#28a745",
            "warning": "#ffc107", 
            "error": "#dc3545"
        }
        
        color = confidence_color_map.get(prediction['confidence_color'], "#28a745")
        
        st.markdown(f"""
        <div style="background: white; border: 2px solid {color}; border-radius: 15px; 
                    padding: 1.5rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{prediction['confidence_icon']}</div>
            <h3 style="margin: 0; color: {color};">{prediction['confidence']}%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">
                Konfidenz: <strong>{prediction['confidence_level']}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed breakdown
    st.markdown("### 📊 Detaillierte Analyse")
    
    col3, col4 = st.columns([1, 1])
    
    with col3:
        st.markdown("**🔧 Verwendete Faktoren:**")
        factors = prediction['factors_used']
        
        factor_descriptions = {
            'base_rate': 'Basis-Wartungssatz',
            'manufacturer': 'Hersteller-Faktor', 
            'location': 'Standort-Faktor',
            'criticality': 'Kritikalitäts-Faktor',
            'usage': 'Nutzungs-Faktor',
            'age': 'Alters-Faktor'
        }
        
        for key, value in factors.items():
            description = factor_descriptions.get(key, key)
            st.write(f"• **{description}:** {value}")
    
    with col4:
        st.markdown("**🎯 Ähnliche Assets (Referenz):**")
        
        for asset in similar_assets[:3]:  # Top 3
            maintenance_pct = (asset['maintenance'] / asset['price']) * 100
            st.markdown(f"""
            <div style="background: #f8f9fa; border-radius: 8px; padding: 0.8rem; margin: 0.5rem 0;">
                <strong>{asset['name']}</strong><br>
                <small>{asset['manufacturer']} {asset['model']} | {asset['location']}</small><br>
                <span style="color: #FF6600;">€{asset['maintenance']:,}/Jahr ({maintenance_pct:.1f}%)</span>
            </div>
            """, unsafe_allow_html=True)
    
    # TCO Preview Chart
    st.markdown("### 📈 TCO-Projektion (5 Jahre)")
    
    years = list(range(2025, 2030))
    annual_cost = prediction['annual_prediction']
    purchase_price = asset_data.get('purchase_price', 0)
    
    # Escalation factor (maintenance increases over time)
    costs_over_time = []
    for i, year in enumerate(years):
        escalation = 1 + (i * 0.05)  # 5% increase per year
        yearly_cost = annual_cost * escalation
        costs_over_time.append(yearly_cost)
    
    # Create chart
    fig = go.Figure()
    
    # Purchase cost (one-time)
    fig.add_trace(go.Bar(
        x=[years[0]], 
        y=[purchase_price],
        name='Anschaffungskosten',
        marker_color='#003366'
    ))
    
    # Annual maintenance costs
    fig.add_trace(go.Bar(
        x=years,
        y=costs_over_time,
        name='Jährliche Wartungskosten',
        marker_color='#FF6600'
    ))
    
    fig.update_layout(
        title="TCO-Entwicklung über 5 Jahre",
        xaxis_title="Jahr",
        yaxis_title="Kosten (€)",
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Manual adjustment option
    with st.expander("⚙️ Schätzung manuell anpassen"):
        st.markdown("Falls Sie andere Informationen haben, können Sie die KI-Schätzung anpassen:")
        
        manual_cost = st.number_input(
            "Ihre Schätzung (€/Jahr):",
            min_value=0,
            value=prediction['annual_prediction'],
            step=100
        )
        
        manual_reason = st.text_input(
            "Grund für Anpassung:",
            placeholder="z.B. Spezialvertrag, interne Erfahrung, etc."
        )
        
        if manual_cost != prediction['annual_prediction']:
            st.session_state.asset_data['manual_override'] = manual_cost
            st.session_state.asset_data['manual_reason'] = manual_reason
            st.info(f"💡 Angepasste Schätzung: €{manual_cost:,}/Jahr")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col5, col6, col7 = st.columns([1, 1, 1])
    
    with col5:
        if st.button("← ZURÜCK ZU GRUNDDATEN", key="step3_back", use_container_width=True):
            st.session_state.page = 'step2'
            st.rerun()
    
    with col6:
        # Regenerate prediction
        if st.button("🔄 NEUE ANALYSE", key="step3_regenerate", use_container_width=True):
            st.rerun()  # Will recalculate with new random factors
    
    with col7:
        if st.button("WEITER ZUR ÜBERSICHT →", key="step3_next", type="primary", use_container_width=True):
            st.session_state.page = 'step4'
            st.rerun()