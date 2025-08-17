import streamlit as st
from datetime import datetime, date
import re

def get_manufacturers_by_category():
    """Hersteller-Listen je nach Asset-Kategorie"""
    return {
        "IT-Equipment": ["Dell", "HP", "Lenovo", "Apple", "Microsoft", "Cisco", "IBM"],
        "Industrial": ["GEA", "Alfa Laval", "Siemens", "ABB", "Schneider Electric", "Endress+Hauser"],
        "Software": ["SAP", "Microsoft", "Autodesk", "Oracle", "Adobe", "Salesforce"],
        "Vehicles": ["Mercedes", "BMW", "VW", "Ford", "MAN", "Still"],
        "Facilities": ["Siemens", "Bosch", "Honeywell", "Johnson Controls", "KONE"]
    }

def get_locations():
    """GEA Standorte weltweit"""
    return [
        "Düsseldorf (HQ)", "Oelde", "Berlin", "Hamburg", "München",
        "Kopenhagen", "Mailand", "Lyon", "Shanghai", "Singapur", 
        "Chicago", "São Paulo", "Andere"
    ]

def get_cost_centers():
    """Typische Kostenstellen"""
    return [
        "IT-01 (IT Infrastructure)", "IT-02 (Software & Licenses)",
        "PRD-A (Production Line A)", "PRD-B (Production Line B)", 
        "R&D-01 (Research & Development)", "ADM-01 (Administration)",
        "LOG-01 (Logistics)", "QA-01 (Quality Assurance)", "Andere"
    ]

def validate_form_data(data):
    """Validiert die Formulardaten"""
    errors = []
    
    # Asset-Name validieren
    if not data.get('asset_name', '').strip():
        errors.append("Asset-Name ist erforderlich")
    elif len(data['asset_name'].strip()) < 3:
        errors.append("Asset-Name muss mindestens 3 Zeichen haben")
    
    # Anschaffungskosten validieren
    if not data.get('purchase_price'):
        errors.append("Anschaffungskosten sind erforderlich")
    elif data['purchase_price'] <= 0:
        errors.append("Anschaffungskosten müssen größer als 0 sein")
    elif data['purchase_price'] > 10000000:  # 10 Mio Cap
        errors.append("Anschaffungskosten scheinen unrealistisch hoch")
    
    # Datum validieren
    if data.get('purchase_date'):
        if data['purchase_date'] > date.today():
            errors.append("Anschaffungsdatum kann nicht in der Zukunft liegen")
        elif data['purchase_date'].year < 1990:
            errors.append("Anschaffungsdatum scheint unrealistisch alt")
    
    return errors

def show():
    """Step 2: Grunddaten eingeben"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 2/4")
    st.markdown("---")
    
    # Asset-Info aus Step 1 anzeigen
    if 'category' in st.session_state.asset_data:
        selected_category = st.session_state.asset_data['category']
        selected_subcategory = st.session_state.asset_data.get('subcategory', '')
        
        # Info-Banner
        st.markdown(f"""
        <div class="gea-card" style="background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-left: 5px solid #FF6600;">
            <h4 style="margin: 0; color: #003366;">📋 Asset-Typ: {selected_category} → {selected_subcategory}</h4>
            <p style="margin: 0.5rem 0 0 0; color: #666;">Geben Sie nun die Grunddaten für das neue Asset ein</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ Kein Asset-Typ ausgewählt. Bitte gehen Sie zurück zu Schritt 1.")
        return
    
    st.markdown("## Grunddaten eingeben")
    
    # Zwei-Spalten Layout für bessere UX
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📝 Asset-Informationen")
        
        # Asset-Name (Required)
        asset_name = st.text_input(
            "Asset-Name *", 
            value=st.session_state.asset_data.get('asset_name', ''),
            placeholder=f"z.B. {selected_subcategory}-{selected_category[:3].upper()}-001",
            help="Eindeutiger Name für das Asset"
        )
        st.session_state.asset_data['asset_name'] = asset_name
        
        # Hersteller (Required)
        manufacturers = get_manufacturers_by_category()
        manufacturer_list = manufacturers.get(selected_category, ["Andere"])
        
        manufacturer = st.selectbox(
            "Hersteller *",
            ["Bitte wählen..."] + manufacturer_list,
            index=0 if 'manufacturer' not in st.session_state.asset_data 
                  else manufacturer_list.index(st.session_state.asset_data['manufacturer']) + 1
                  if st.session_state.asset_data['manufacturer'] in manufacturer_list else 0
        )
        
        if manufacturer != "Bitte wählen...":
            st.session_state.asset_data['manufacturer'] = manufacturer
        
        # Modell/Bezeichnung
        model = st.text_input(
            "Modell/Bezeichnung",
            value=st.session_state.asset_data.get('model', ''),
            placeholder="z.B. PowerEdge R740, ThinkPad X1, WSP 5000",
            help="Spezifische Modellbezeichnung (optional)"
        )
        st.session_state.asset_data['model'] = model
        
        # Seriennummer (optional)
        serial_number = st.text_input(
            "Seriennummer", 
            value=st.session_state.asset_data.get('serial_number', ''),
            placeholder="Optional für Tracking",
            help="Herstellerseitige Seriennummer"
        )
        st.session_state.asset_data['serial_number'] = serial_number
    
    with col2:
        st.markdown("### 💰 Kosten & Standort")
        
        # Anschaffungskosten (Required)
        purchase_price = st.number_input(
            "Anschaffungskosten (€) *",
            min_value=0.0,
            max_value=10000000.0,
            value=float(st.session_state.asset_data.get('purchase_price', 0)),
            step=100.0,
            format="%.2f",
            help="Gesamte Anschaffungskosten inkl. Setup"
        )
        st.session_state.asset_data['purchase_price'] = purchase_price
        
        # Anschaffungsdatum
        purchase_date = st.date_input(
            "Anschaffungsdatum",
            value=st.session_state.asset_data.get('purchase_date', date.today()),
            min_value=date(1990, 1, 1),
            max_value=date.today(),
            help="Datum der Anschaffung oder Inbetriebnahme"
        )
        st.session_state.asset_data['purchase_date'] = purchase_date
        
        # Standort
        location = st.selectbox(
            "Standort",
            get_locations(),
            index=get_locations().index(st.session_state.asset_data.get('location', 'Düsseldorf (HQ)'))
        )
        st.session_state.asset_data['location'] = location
        
        # Kostenstelle
        cost_center = st.selectbox(
            "Kostenstelle",
            get_cost_centers(),
            index=0 if 'cost_center' not in st.session_state.asset_data
                  else get_cost_centers().index(st.session_state.asset_data['cost_center'])
                  if st.session_state.asset_data['cost_center'] in get_cost_centers() else 0
        )
        st.session_state.asset_data['cost_center'] = cost_center
    
    # Erweiterte Optionen (Expander)
    with st.expander("🔧 Erweiterte Optionen"):
        col3, col4 = st.columns(2)
        
        with col3:
            # Nutzungsdauer
            expected_lifetime = st.slider(
                "Erwartete Nutzungsdauer (Jahre)",
                min_value=1, max_value=20,
                value=st.session_state.asset_data.get('expected_lifetime', 5),
                help="Geplante Nutzungsdauer für TCO-Berechnung"
            )
            st.session_state.asset_data['expected_lifetime'] = expected_lifetime
            
            # Criticality
            criticality = st.select_slider(
                "Kritikalität",
                options=["Niedrig", "Mittel", "Hoch", "Kritisch"],
                value=st.session_state.asset_data.get('criticality', "Mittel"),
                help="Ausfallkritikalität für das Business"
            )
            st.session_state.asset_data['criticality'] = criticality
        
        with col4:
            # Usage Pattern
            usage_pattern = st.selectbox(
                "Nutzungsmuster",
                ["Standard (8h/Tag)", "Extended (12h/Tag)", "24/7 Betrieb", "Gelegentlich"],
                index=0
            )
            st.session_state.asset_data['usage_pattern'] = usage_pattern
            
            # Warranty Info
            warranty_years = st.number_input(
                "Garantie/Gewährleistung (Jahre)",
                min_value=0.0, max_value=10.0,
                value=st.session_state.asset_data.get('warranty_years', 1.0),
                step=0.5,
                help="Herstellergarantie in Jahren"
            )
            st.session_state.asset_data['warranty_years'] = warranty_years
    
    # Notizen/Kommentare
    notes = st.text_area(
        "Notizen/Kommentare",
        value=st.session_state.asset_data.get('notes', ''),
        placeholder="Zusätzliche Informationen, Besonderheiten, etc.",
        height=100,
        help="Optionale Zusatzinformationen"
    )
    st.session_state.asset_data['notes'] = notes
    
    # Formular-Validierung
    form_data = {
        'asset_name': asset_name,
        'manufacturer': manufacturer if manufacturer != "Bitte wählen..." else '',
        'purchase_price': purchase_price,
        'purchase_date': purchase_date
    }
    
    validation_errors = validate_form_data(form_data)
    
    # Validation Feedback
    if validation_errors:
        st.error("❌ **Bitte korrigieren Sie folgende Fehler:**")
        for error in validation_errors:
            st.write(f"• {error}")
    else:
        st.success("✅ **Alle Pflichtfelder ausgefüllt!**")
    
    # Zusammenfassung anzeigen
    if not validation_errors:
        with st.expander("📋 Eingabe-Zusammenfassung", expanded=False):
            col5, col6 = st.columns(2)
            
            with col5:
                st.write("**Asset-Details:**")
                st.write(f"• Name: {asset_name}")
                st.write(f"• Typ: {selected_category} → {selected_subcategory}")
                st.write(f"• Hersteller: {manufacturer}")
                if model:
                    st.write(f"• Modell: {model}")
            
            with col6:
                st.write("**Kosten & Standort:**")
                st.write(f"• Anschaffung: €{purchase_price:,.2f}")
                st.write(f"• Datum: {purchase_date.strftime('%d.%m.%Y')}")
                st.write(f"• Standort: {location}")
                st.write(f"• Kostenstelle: {cost_center}")
    
    # Navigation
    st.markdown("<br><br>", unsafe_allow_html=True)
    col7, col8, col9 = st.columns([1, 1, 1])
    
    with col7:
        if st.button("← ZURÜCK ZU SCHRITT 1", key="step2_back", use_container_width=True):
            st.session_state.page = 'step1'
            st.rerun()
    
    with col8:
        # Reset Button
        if st.button("🔄 FORMULAR ZURÜCKSETZEN", key="step2_reset", use_container_width=True):
            # Nur Step 2 Daten löschen, Step 1 behalten
            keys_to_keep = ['category', 'subcategory', 'subcategories']
            filtered_data = {k: v for k, v in st.session_state.asset_data.items() if k in keys_to_keep}
            st.session_state.asset_data = filtered_data
            st.rerun()
    
    with col9:
        # Weiter-Button nur aktiv wenn alles valid
        if not validation_errors:
            if st.button("WEITER ZUR KI-SCHÄTZUNG →", key="step2_next", type="primary", use_container_width=True):
                st.session_state.page = 'step3'
                st.rerun()
        else:
            st.button("WEITER ZUR KI-SCHÄTZUNG →", key="step2_next_disabled", disabled=True, use_container_width=True)
            st.caption("⚠️ Bitte füllen Sie alle Pflichtfelder aus")