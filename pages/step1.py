import streamlit as st

def get_mock_categories():
    """Asset-Kategorien direkt hier"""
    return {
        "IT-Equipment": {
            "icon": "💻",
            "description": "Server, Laptops, Netzwerk",
            "subcategories": ["Server", "Laptop", "Workstation", "Netzwerk"]
        },
        "Industrial": {
            "icon": "🏭", 
            "description": "Maschinen & Anlagen",
            "subcategories": ["Separator", "Homogenizer", "Pump", "Pasteurizer"]
        },
        "Software": {
            "icon": "💾",
            "description": "Lizenzen & SaaS",
            "subcategories": ["ERP", "CAD", "Office", "Analyse"]
        }
    }

def show():
    """Asset-Typ Auswahl - Schritt 1"""
    
    # Header
    st.markdown("### ← Zurück &nbsp;&nbsp;&nbsp; NEUES ASSET HINZUFÜGEN &nbsp;&nbsp;&nbsp; Schritt 1/4")
    st.markdown("---")
    
    st.markdown("## Welchen Asset-Typ möchten Sie hinzufügen?")
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Asset-Kategorien holen
    categories = get_mock_categories()
    
    # Grid Layout für Asset-Karten
    cols = st.columns(3)
    
    for idx, (category_key, category_info) in enumerate(categories.items()):
        col_idx = idx % 3
        
        with cols[col_idx]:
            # Asset-Karte
            st.markdown(f"""
            <div style="text-align: center; padding: 2rem; background: #f8f9fa; border: 2px solid #e9ecef; border-radius: 10px; margin: 1rem 0;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">{category_info['icon']}</div>
                <h3 style="margin: 0.5rem 0; color: #003366;">{category_key}</h3>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">{category_info['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Button unter der Karte
            if st.button(
                "AUSWÄHLEN", 
                key=f"select_{category_key}",
                use_container_width=True
            ):
                st.session_state.asset_data['category'] = category_key
                st.session_state.asset_data['subcategories'] = category_info['subcategories']
                st.rerun()
    
    # Zeige ausgewählte Kategorie
    if 'category' in st.session_state.asset_data:
        selected_category = st.session_state.asset_data['category']
        category_info = categories[selected_category]
        
        st.success(f"✅ Ausgewählt: **{selected_category}**")
        
        # Subcategory-Auswahl
        subcategory = st.selectbox(
            "Spezifischer Asset-Typ:",
            category_info['subcategories'],
            key="subcategory_select"
        )
        st.session_state.asset_data['subcategory'] = subcategory
    
    # Navigation
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("← ZURÜCK", key="step1_back"):
            st.session_state.page = 'dashboard'
            st.rerun()
    
    with col3:
        if 'category' in st.session_state.asset_data:
            if st.button("WEITER →", key="step1_next", type="primary"):
                st.session_state.page = 'step2'
                st.rerun()
        else:
            st.button("WEITER →", disabled=True)