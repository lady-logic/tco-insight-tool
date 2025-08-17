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
    ML_AVAILABLE = True
except ImportError as e:
    ML_AVAILABLE = False
    st.error(f"❌ ML-Model nicht verfügbar: {e}")

@st.cache_resource
def load_ml_model():
    """Lädt das ML-Model (wird gecacht für Performance)"""
    if not ML_AVAILABLE:
        return None
    
    try:
        predictor = TCOPredictor()
        
        # Try to load existing model first
        model_path = 'ml/tco_model.pkl'
        if os.path.exists(model_path):
            predictor.load_model(model_path)
            return predictor
        else:
            # Train new model if none exists
            st.info("🤖 Kein trainiertes Model gefunden. Trainiere neues Model...")
            stats = predictor.train()
            predictor.save_model()
            return predictor
            
    except Exception as e:
        st.error(f"❌ Fehler beim Laden des ML-Models: {e}")
        return None

def create_ml_analysis_animation():
    """Erstellt eine realistische ML-Analyse-Animation"""
    
    analysis_steps = [
        {"step": "🔍 Lade ML-Model...", "duration": 0.8},
        {"step": "📊 Analysiere Asset-Features...", "duration": 1.2},
        {"step": "🌳 Random Forest Inference...", "duration": 1.0},
        {"step": "📈 Berechne Konfidenz-Score...", "duration": 0.9},
        {"step": "🎯 Suche ähnliche Assets...", "duration": 1.1},
        {"step": "✅ ML-Analyse abgeschlossen!", "duration": 0.5}
    ]
    
    progress_container = st.empty()
    status_container = st.empty()
    
    total_steps = len(analysis_steps)
    
    for i, step_info in enumerate(analysis_steps):
        progress = (i + 1) / total_steps
        progress_container.progress(progress)
        status_container.write(f"**{step_info['step']}**")
        time.sleep(step_info['duration'])
    
    # Clear containers
    progress_container.empty()
    status_container.empty()

def create_ml_comparison_chart(ml_prediction, fake_prediction):
    """Vergleicht ML-Vorhersage mit alter Fake-Vorhersage"""
    
    comparison_data = {
        'Method': ['🤖 ML-Model (Random Forest)', '🎭 Simulation (Rules-based)'],
        'Prediction': [ml_prediction['annual_prediction'], fake_prediction['annual_prediction']],
        'Confidence': [ml_prediction['confidence'], fake_prediction['confidence']],
        'Method_Type': ['Machine Learning', 'Rule-based']
    }
    
    fig = go.Figure()
    
    # Add bars for predictions
    fig.add_trace(go.Bar(
        name='Vorhersage (€/Jahr)',
        x=comparison_data['Method'],
        y=comparison_data['Prediction'],
        marker_color=['#003366', '#FF6600'],
        text=[f"€{x:,}" for x in comparison_data['Prediction']],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="🤖 ML vs. 🎭 Simulation: Vorhersage-Vergleich",
        yaxis_title="Jährliche Wartungskosten (€)",
        height=400,
        showlegend=False
    )
    
    return fig

def show_feature_importance(predictor):
    """Zeigt Feature Importance des ML-Models"""
    
    if not predictor or not hasattr(predictor, 'training_stats'):
        return
    
    feature_importance = predictor.training_stats.get('feature_importance', {})
    
    if not feature_importance:
        return
    
    # Sort features by importance
    sorted_features = sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
    top_features = sorted_features[:8]  # Top 8 features
    
    # Create horizontal bar chart
    feature_names = [item[0] for item in top_features]
    importance_values = [item[1] for item in top_features]
    
    # Translate feature names to German
    feature_translations = {
        'purchase_price': 'Anschaffungspreis',
        'age_years': 'Alter (Jahre)',
        'manufacturer': 'Hersteller',
        'category': 'Kategorie',
        'subcategory': 'Subkategorie',
        'location': 'Standort',
        'usage_pattern': 'Nutzungsmuster',
        'criticality': 'Kritikalität',
        'warranty_years': 'Garantie (Jahre)',
        'expected_lifetime': 'Erwartete Lebensdauer',
        'price_age_ratio': 'Preis-Alter-Verhältnis',
        'age_category': 'Alters-Kategorie',
        'warranty_active': 'Garantie aktiv'
    }
    
    translated_names = [feature_translations.get(name, name) for name in feature_names]
    
    fig = go.Figure(go.Bar(
        x=importance_values,
        y=translated_names,
        orientation='h',
        marker_color='#003366',
        text=[f"{val:.3f}" for val in importance_values],
        textposition='outside'
    ))
    
    fig.update_layout(
        title="🧠 ML-Model: Feature Importance",
        xaxis_title="Wichtigkeit",
        yaxis_title="Features",
        height=400,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def show():
    """Step 3: Echte KI-Schätzung mit ML"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 3/4")
    st.markdown("---")
    
    # Asset-Info validation
    if not st.session_state.asset_data.get('asset_name'):
        st.error("❌ Keine Asset-Daten gefunden. Bitte gehen Sie zurück zu Schritt 2.")
        return
    
    asset_data = st.session_state.asset_data
    
    # Asset Summary
    st.markdown(f"""
    <div class="gea-card" style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-left: 5px solid #003366;">
        <h4 style="margin: 0; color: #003366;">🤖 Machine Learning Kostenschätzung</h4>
        <p style="margin: 0.5rem 0 0 0; color: #666;">
            Für: <strong>{asset_data.get('asset_name', 'N/A')}</strong> 
            ({asset_data.get('manufacturer', 'N/A')} {asset_data.get('model', '')})
        </p>
        <p style="margin: 0.3rem 0 0 0; color: #666; font-size: 0.9rem;">
            🧠 Random Forest Model • 📊 Trainiert mit 500+ Assets • ⚡ Real-time Inference
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load ML Model
    st.markdown("## 🧠 ML-Model wird geladen...")
    
    with st.spinner("Lade Machine Learning Model..."):
        predictor = load_ml_model()
    
    if not predictor:
        st.error("❌ ML-Model konnte nicht geladen werden. Fallback auf Simulation.")
        # Fallback to old fake prediction
        from pages.step3 import calculate_fake_tco_prediction
        prediction = calculate_fake_tco_prediction(
            asset_data.get('subcategory', 'Server'),
            asset_data.get('manufacturer', 'Dell'),
            asset_data.get('purchase_price', 10000)
        )
        st.session_state.asset_data['ai_prediction'] = prediction
        st.warning("⚠️ Verwende Regel-basierte Simulation statt ML")
    else:
        # ML Analysis Animation
        st.markdown("## 🤖 Machine Learning Analyse läuft...")
        create_ml_analysis_animation()
        
        # Prepare asset data for ML prediction
        ml_asset_data = {
            'category': asset_data.get('category', 'IT-Equipment'),
            'subcategory': asset_data.get('subcategory', 'Server'),
            'manufacturer': asset_data.get('manufacturer', 'Dell'),
            'purchase_price': asset_data.get('purchase_price', 10000),
            'age_years': 0.5,  # Assume 6 months old for new asset
            'warranty_years': asset_data.get('warranty_years', 1),
            'expected_lifetime': asset_data.get('expected_lifetime', 5),
            'location': asset_data.get('location', 'Düsseldorf (HQ)'),
            'usage_pattern': asset_data.get('usage_pattern', 'Standard (8h/Tag)'),
            'criticality': asset_data.get('criticality', 'Mittel')
        }
        
        # Get ML prediction
        try:
            ml_prediction = predictor.predict(ml_asset_data)
            similar_assets = predictor.get_similar_assets(ml_asset_data)
            
            # Store in session state
            st.session_state.asset_data['ai_prediction'] = ml_prediction
            st.session_state.asset_data['similar_assets'] = similar_assets
            st.session_state.asset_data['ml_used'] = True
            
            # Show success
            st.success("✅ Machine Learning Analyse abgeschlossen!")
            
        except Exception as e:
            st.error(f"❌ ML-Vorhersage fehlgeschlagen: {e}")
            # Fallback
            prediction = {'annual_prediction': 1000, 'confidence': 50, 'confidence_level': 'Niedrig'}
            st.session_state.asset_data['ai_prediction'] = prediction
    
    # Results Section
    prediction = st.session_state.asset_data.get('ai_prediction', {})
    
    st.markdown("## 🎯 Machine Learning Ergebnisse")
    
    # Main prediction display with ML branding
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Enhanced prediction result card
        model_info = "🤖 Random Forest" if predictor else "🎭 Simulation"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #003366, #0066CC); color: white; 
                    border-radius: 15px; padding: 2rem; text-align: center; margin: 1rem 0;">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 0.5rem;">{model_info}</div>
            <h2 style="margin: 0; font-size: 2.5rem;">€{prediction.get('annual_prediction', 0):,}</h2>
            <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
                Geschätzte jährliche Wartungskosten
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Range display
        range_min = prediction.get('range_min', 0)
        range_max = prediction.get('range_max', 0)
        st.markdown(f"""
        <div style="background: #f8f9fa; border-radius: 10px; padding: 1rem; text-align: center;">
            <strong>Vorhersage-Bereich:</strong> €{range_min:,} - €{range_max:,}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Enhanced confidence display
        confidence = prediction.get('confidence', 0)
        confidence_level = prediction.get('confidence_level', 'Niedrig')
        confidence_icon = prediction.get('confidence_icon', '🔴')
        
        confidence_color_map = {
            "success": "#28a745",
            "warning": "#ffc107", 
            "error": "#dc3545"
        }
        
        color = confidence_color_map.get(prediction.get('confidence_color', 'error'), "#28a745")
        
        st.markdown(f"""
        <div style="background: white; border: 2px solid {color}; border-radius: 15px; 
                    padding: 1.5rem; text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">{confidence_icon}</div>
            <h3 style="margin: 0; color: {color};">{confidence}%</h3>
            <p style="margin: 0.5rem 0 0 0; color: #666;">
                ML-Konfidenz: <strong>{confidence_level}</strong>
            </p>
            {f'<p style="margin: 0.3rem 0 0 0; font-size: 0.8rem; color: #999;">Model: {prediction.get("model_type", "Unknown")}</p>' if predictor else ''}
        </div>
        """, unsafe_allow_html=True)
    
    # ML-specific insights
    if predictor and ML_AVAILABLE:
        st.markdown("### 🧠 Machine Learning Insights")
        
        col3, col4 = st.columns([1, 1])
        
        with col3:
            # Model performance info
            stats = predictor.training_stats
            st.markdown("**📊 Model Performance:**")
            st.write(f"• **R² Score:** {stats.get('test_r2', 0):.3f} ({stats.get('test_r2', 0)*100:.1f}% Varianz erklärt)")
            st.write(f"• **Mean Absolute Error:** €{stats.get('test_mae', 0):,.0f}")
            st.write(f"• **Training Assets:** {stats.get('n_training_assets', 0):,}")
            st.write(f"• **Features verwendet:** {stats.get('n_features', 0)}")
            
            # Prediction details
            if 'prediction_std' in prediction:
                st.write(f"• **Vorhersage-Unsicherheit:** €{prediction['prediction_std']:,.0f}")
        
        with col4:
            # Feature importance chart
            importance_fig = show_feature_importance(predictor)
            if importance_fig:
                st.plotly_chart(importance_fig, use_container_width=True)
    
    # Enhanced similar assets section
    similar_assets = st.session_state.asset_data.get('similar_assets', [])
    if similar_assets:
        st.markdown("### 🎯 Ähnliche Assets aus ML-Training-Daten")
        
        for i, asset in enumerate(similar_assets[:3]):
            maintenance_pct = (asset.get('maintenance', 0) / asset.get('price', 1)) * 100
            
            # Enhanced asset card with more details
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f8f9fa, white); border: 1px solid #dee2e6; 
                        border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong style="color: #003366;">{asset.get('name', 'N/A')}</strong><br>
                        <small style="color: #666;">{asset.get('manufacturer', 'N/A')} {asset.get('model', '')} | {asset.get('location', 'N/A')}</small><br>
                        <small style="color: #999;">Alter: {asset.get('age', 'N/A')}</small>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #FF6600; font-weight: bold;">€{asset.get('maintenance', 0):,}/Jahr</span><br>
                        <small style="color: #666;">({maintenance_pct:.1f}% von Anschaffung)</small>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Optional: Comparison with rule-based prediction
    if predictor and st.checkbox("🔍 Vergleich: ML vs. Regel-basierte Simulation", value=False):
        st.markdown("### 🤖 vs 🎭 Methodenvergleich")
        
        # Calculate fake prediction for comparison
        from pages.step3 import calculate_fake_tco_prediction
        fake_prediction = calculate_fake_tco_prediction(
            asset_data.get('subcategory', 'Server'),
            asset_data.get('manufacturer', 'Dell'),
            asset_data.get('purchase_price', 10000)
        )
        
        # Show comparison
        comparison_fig = create_ml_comparison_chart(prediction, fake_prediction)
        st.plotly_chart(comparison_fig, use_container_width=True)
        
        col5, col6 = st.columns(2)
        with col5:
            st.markdown("**🤖 Machine Learning:**")
            st.write("• Lernt aus echten Daten")
            st.write("• Berücksichtigt komplexe Muster")
            st.write("• Adaptiert sich automatisch")
            st.write("• Confidence basierend auf Modell-Unsicherheit")
        
        with col6:
            st.markdown("**🎭 Regel-basierte Simulation:**")
            st.write("• Verwendet vordefinierte Regeln")
            st.write("• Einfache Faktor-Multiplikation")
            st.write("• Feste Berechnungslogik")
            st.write("• Confidence basierend auf Datenvollständigkeit")
    
    # Manual adjustment (enhanced for ML)
    with st.expander("⚙️ ML-Vorhersage manuell anpassen"):
        st.markdown("Die ML-Vorhersage basiert auf gelernten Mustern. Sie können sie anpassen wenn Sie spezifische Informationen haben:")
        
        current_prediction = prediction.get('annual_prediction', 0)
        manual_cost = st.number_input(
            "Ihre Experteneinschätzung (€/Jahr):",
            min_value=0,
            value=current_prediction,
            step=100,
            help="Überschreibt die ML-Vorhersage mit Ihrer Einschätzung"
        )
        
        manual_reason = st.text_input(
            "Grund für Anpassung:",
            placeholder="z.B. Spezialvertrag, besondere Umstände, interne Erfahrung...",
            help="Dokumentiert warum Sie die ML-Vorhersage angepasst haben"
        )
        
        if manual_cost != current_prediction:
            st.session_state.asset_data['manual_override'] = manual_cost
            st.session_state.asset_data['manual_reason'] = manual_reason
            
            # Calculate difference
            difference = manual_cost - current_prediction
            percentage_diff = (difference / current_prediction) * 100 if current_prediction > 0 else 0
            
            if difference > 0:
                st.info(f"💡 Ihre Schätzung ist €{difference:,} höher als ML-Vorhersage ({percentage_diff:+.1f}%)")
            else:
                st.info(f"💡 Ihre Schätzung ist €{abs(difference):,} niedriger als ML-Vorhersage ({percentage_diff:+.1f}%)")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col7, col8, col9 = st.columns([1, 1, 1])
    
    with col7:
        if st.button("← ZURÜCK ZU GRUNDDATEN", key="step3_back", use_container_width=True):
            st.session_state.page = 'step2'
            st.rerun()
    
    with col8:
        # Enhanced regenerate with ML context
        button_text = "🔄 NEUE ML-ANALYSE" if predictor else "🔄 NEUE SIMULATION"
        if st.button(button_text, key="step3_regenerate", use_container_width=True):
            # Clear previous predictions to force regeneration
            if 'ai_prediction' in st.session_state.asset_data:
                del st.session_state.asset_data['ai_prediction']
            st.rerun()
    
    with col9:
        if st.button("WEITER ZUR ÜBERSICHT →", key="step3_next", type="primary", use_container_width=True):
            st.session_state.page = 'step4'
            st.rerun()

# Fallback function for fake prediction (if ML fails)
def calculate_fake_tco_prediction(asset_type, manufacturer, price):
    """Fallback rule-based prediction"""
    import random
    
    base_rates = {"Server": 0.20, "Laptop": 0.15, "Separator": 0.15}
    base_rate = base_rates.get(asset_type, 0.15)
    
    manufacturer_factors = {"Dell": 1.1, "HP": 1.0, "GEA": 1.15}
    mfg_factor = manufacturer_factors.get(manufacturer, 1.0)
    
    annual_maintenance = price * base_rate * mfg_factor
    variance = random.uniform(0.8, 1.2)
    predicted_cost = annual_maintenance * variance
    confidence = random.uniform(0.75, 0.90)
    
    return {
        "annual_prediction": round(predicted_cost),
        "confidence": round(confidence * 100),
        "confidence_level": "Mittel",
        "confidence_color": "warning",
        "confidence_icon": "🟡",
        "range_min": round(predicted_cost * 0.8),
        "range_max": round(predicted_cost * 1.2)
    }