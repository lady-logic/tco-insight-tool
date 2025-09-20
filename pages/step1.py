import streamlit as st

def get_core_industrial_categories():
    """Nur die 3 wichtigsten GEA Equipment-Kategorien"""
    return {
        "Separator": {
            "icon": "🌀",
            "description": "Zentrifugen für Separation & Clarification",
            "subcategories": ["Disc Stack Separator", "Decanter", "Chamber Bowl", "Clarifier"],
            "typical_applications": ["Juice Clarification", "Oil Separation", "Protein Recovery", "Water Treatment"]
        },
        "Homogenizer": {
            "icon": "🔄", 
            "description": "Hochdruck-Homogenisatoren",
            "subcategories": ["Ariete", "Rannie", "Lab Homogenizer", "UHT Homogenizer"],
            "typical_applications": ["Dairy Processing", "Pharmaceutical", "Cosmetics", "Food & Beverage"]
        },
        "Pump": {
            "icon": "⚙️",
            "description": "Sanitär- & Industriepumpen",
            "subcategories": ["Centrifugal Pump", "Positive Displacement", "Hilge HYGIA", "Varipump"],
            "typical_applications": ["CIP Systems", "Product Transfer", "Circulation", "Dosing"]
        }
    }

def show():
    """Asset-Typ Auswahl - Schritt 1 (nur 3 Haupttypen)"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUE GEA ANLAGE HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 1/4")
    st.markdown("---")
    
    st.markdown("## Welche Art von GEA Anlage möchten Sie hinzufügen?")
    st.write("")  # Leerzeile ohne HTML
    
    # Info über die Fokussierung
    st.info("🎯 **Fokus auf Kern-Equipment:** Wir konzentrieren uns auf die 3 wichtigsten GEA Anlagentypen für maximale Präzision bei der TCO-Analyse.")
    
    # Asset-Kategorien holen (nur 3)
    categories = get_core_industrial_categories()
    
    # Einfache 3-spaltige Button-Layout
    cols = st.columns(3)
    
    for idx, (category_key, category_info) in enumerate(categories.items()):
        with cols[idx]:
            # Einfache Textbeschreibung
            st.markdown(f"### {category_info['icon']} {category_key}")
            st.write(category_info['description'])
            st.write(f"✓ {len(category_info['subcategories'])} Varianten verfügbar")
            
            # Button
            button_text = f"🏭 {category_key.upper()} AUSWÄHLEN"
            if st.button(button_text, key=f"select_{category_key}", use_container_width=True):
                st.session_state.asset_data['category'] = 'Industrial'
                st.session_state.asset_data['subcategory'] = category_key
                st.session_state.asset_data['equipment_variants'] = category_info['subcategories']
                st.session_state.asset_data['typical_applications'] = category_info['typical_applications']
                st.rerun()
    
    # Zeige ausgewählte Kategorie
    if 'subcategory' in st.session_state.asset_data:
        selected_equipment = st.session_state.asset_data['subcategory']
        equipment_info = categories[selected_equipment]
        
        st.success(f"✅ **{selected_equipment}** ausgewählt - {equipment_info['description']}")
        
        # Erweiterte Equipment-Konfiguration
        st.markdown("### 🔧 Equipment-Konfiguration")
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Equipment-Variante Auswahl
            st.markdown("**Spezifische Equipment-Variante:**")
            equipment_variant = st.selectbox(
                "Wählen Sie die spezifische Variante:",
                equipment_info['subcategories'],
                key="equipment_variant_select",
                help=f"Verschiedene {selected_equipment}-Typen für unterschiedliche Anwendungen"
            )
            st.session_state.asset_data['equipment_variant'] = equipment_variant
            
            # Anwendungsbereich
            st.markdown("**Hauptanwendung:**")
            application = st.selectbox(
                "Wählen Sie den Anwendungsbereich:",
                equipment_info['typical_applications'],
                key="application_select",
                help="Spezifischer Anwendungsbereich für präzisere TCO-Analyse"
            )
            st.session_state.asset_data['application'] = application
        
        with col2:
            # Equipment-spezifische Informationen anzeigen
            equipment_specs = get_equipment_specs(selected_equipment, equipment_variant)
            if equipment_specs:
                st.markdown("**📋 Typische Eigenschaften:**")
                
                # Einfache Darstellung ohne HTML
                for spec_key, spec_value in equipment_specs.items():
                    st.write(f"**{spec_key}:** {spec_value}")
            
            # Zusätzliche Auswahlhilfe
            st.markdown("**💡 Auswahlhilfe:**")
            selection_tips = get_selection_tips(selected_equipment)
            for tip in selection_tips:
                st.write(f"• {tip}")
    
    # Navigation
    st.write("")
    st.write("")
    col1, col2, col3 = st.columns([2, 2, 2])
    
    with col1:
        if st.button("← ZURÜCK ZUM DASHBOARD", key="step1_back", use_container_width=True):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col2:
        # Status-Anzeige
        if 'subcategory' in st.session_state.asset_data:
            selected_equipment = st.session_state.asset_data['subcategory']
            variant = st.session_state.asset_data.get('equipment_variant', 'N/A')
            st.info(f"🏭 **{selected_equipment}** | 🔧 {variant}")
        else:
            st.info("⏳ Bitte wählen Sie einen Equipment-Typ")
    
    with col3:
        # Weiter-Button nur aktiv wenn Equipment vollständig konfiguriert
        if ('subcategory' in st.session_state.asset_data and 
            'equipment_variant' in st.session_state.asset_data):
            if st.button("WEITER ZU GRUNDDATEN →", key="step1_next", type="primary", use_container_width=True):
                st.session_state.page = 'step2'
                st.rerun()
        else:
            st.button("WEITER ZU GRUNDDATEN →", disabled=True, use_container_width=True)
            if 'subcategory' not in st.session_state.asset_data:
                st.caption("⚠️ Equipment-Typ auswählen")
            else:
                st.caption("⚠️ Konfiguration vervollständigen")

def get_equipment_specs(equipment_type, variant):
    """Gibt detaillierte Spezifikationen für Equipment-Typen zurück"""
    
    specs_db = {
        "Separator": {
            "Disc Stack Separator": {
                "Kapazität": "1.000 - 50.000 L/h",
                "Anwendung": "Clarification, Purification",
                "Preisspanne": "€80.000 - €400.000",
                "Wartungsintervall": "2.000 - 4.000 h"
            },
            "Decanter": {
                "Kapazität": "500 - 20.000 L/h", 
                "Anwendung": "Dewatering, Classification",
                "Preisspanne": "€150.000 - €600.000",
                "Wartungsintervall": "3.000 - 6.000 h"
            },
            "Chamber Bowl": {
                "Kapazität": "100 - 2.000 L/h",
                "Anwendung": "High-purity separation",
                "Preisspanne": "€60.000 - €250.000",
                "Wartungsintervall": "1.500 - 3.000 h"
            },
            "Clarifier": {
                "Kapazität": "2.000 - 100.000 L/h",
                "Anwendung": "Juice clarification",
                "Preisspanne": "€100.000 - €500.000",
                "Wartungsintervall": "2.500 - 5.000 h"
            }
        },
        "Homogenizer": {
            "Ariete": {
                "Druck": "150 - 1.000 bar",
                "Anwendung": "Dairy, Pharma, Cosmetics", 
                "Preisspanne": "€80.000 - €300.000",
                "Wartungsintervall": "1.000 - 2.000 h"
            },
            "Rannie": {
                "Druck": "200 - 600 bar",
                "Anwendung": "Food, Beverage",
                "Preisspanne": "€60.000 - €200.000",
                "Wartungsintervall": "1.500 - 3.000 h"
            },
            "Lab Homogenizer": {
                "Druck": "100 - 500 bar",
                "Anwendung": "R&D, Small batches",
                "Preisspanne": "€20.000 - €80.000",
                "Wartungsintervall": "500 - 1.000 h"
            },
            "UHT Homogenizer": {
                "Druck": "200 - 800 bar",
                "Anwendung": "UHT treatment",
                "Preisspanne": "€100.000 - €400.000",
                "Wartungsintervall": "2.000 - 4.000 h"
            }
        },
        "Pump": {
            "Centrifugal Pump": {
                "Förderleistung": "1 - 500 m³/h",
                "Anwendung": "General purpose",
                "Preisspanne": "€5.000 - €50.000",
                "Wartungsintervall": "4.000 - 8.000 h"
            },
            "Positive Displacement": {
                "Förderleistung": "0.1 - 100 m³/h",
                "Anwendung": "Viscous products",
                "Preisspanne": "€8.000 - €80.000", 
                "Wartungsintervall": "2.000 - 4.000 h"
            },
            "Hilge HYGIA": {
                "Förderleistung": "5 - 200 m³/h",
                "Anwendung": "Hygienic applications",
                "Preisspanne": "€15.000 - €100.000",
                "Wartungsintervall": "3.000 - 6.000 h"
            },
            "Varipump": {
                "Förderleistung": "1 - 50 m³/h",
                "Anwendung": "Variable speed applications",
                "Preisspanne": "€10.000 - €60.000",
                "Wartungsintervall": "3.500 - 7.000 h"
            }
        }
    }
    
    return specs_db.get(equipment_type, {}).get(variant, {})

def get_selection_tips(equipment_type):
    """Gibt Auswahlhilfen für Equipment-Typen"""
    
    tips_db = {
        "Separator": [
            "Disc Stack für hohe Durchsätze",
            "Decanter für schwierige Trennungen",
            "Chamber Bowl für höchste Reinheit",
            "Clarifier für Lebensmittel-Anwendungen"
        ],
        "Homogenizer": [
            "Ariete für höchste Drücke",
            "Rannie für Standardanwendungen", 
            "Lab Homogenizer für F&E",
            "UHT für Sterilisations-Prozesse"
        ],
        "Pump": [
            "Centrifugal für niedrige Viskosität",
            "Positive Displacement für hohe Viskosität",
            "Hilge HYGIA für Pharma/Food",
            "Varipump für variable Anforderungen"
        ]
    }
    
    return tips_db.get(equipment_type, ["Kontaktieren Sie GEA für Beratung"])

if __name__ == "__main__":
    show()