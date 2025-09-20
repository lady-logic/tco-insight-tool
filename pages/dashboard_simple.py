import streamlit as st
import pandas as pd
import re

# Import GEA Styling
try:
    from styles.gea_style import apply_gea_styling, create_gea_logo_header, GEA_COLORS
    STYLING_AVAILABLE = True
except ImportError:
    STYLING_AVAILABLE = False

# Standorte mit Energy Agent + feste Preise
STANDORTE = {
    'Düsseldorf (HQ)': {
        'strom': 'ENERGY_AGENT',  # Echte API
        'wasser': 0.0025,         # €/Liter
        'land': 'Deutschland',
        'info': '🟢 Live Strompreise'
    },
    'Kopenhagen': {
        'strom': 'ENERGY_AGENT',  # Echte API  
        'wasser': 0.0035,         # €/Liter
        'land': 'Dänemark',
        'info': '🟢 Live Strompreise'
    },
    'Mailand': {
        'strom': 'ENERGY_AGENT',  # Echte API
        'wasser': 0.002,          # €/Liter
        'land': 'Italien',
        'info': '🟢 Live Strompreise'
    },
    'Lyon': {
        'strom': 'ENERGY_AGENT',  # Echte API
        'wasser': 0.0022,         # €/Liter
        'land': 'Frankreich',
        'info': '🟢 Live Strompreise'
    },
    'Berlin': {
        'strom': 'ENERGY_AGENT',  # Echte API
        'wasser': 0.0028,         # €/Liter
        'land': 'Deutschland',
        'info': '🟢 Live Strompreise'
    },
    'Shanghai': {
        'strom': 0.08,            # €/kWh fest
        'wasser': 0.0008,         # €/Liter
        'land': 'China',
        'info': '🟡 Feste Preise'
    },
    'Chicago': {
        'strom': 0.12,            # €/kWh fest
        'wasser': 0.0015,         # €/Liter
        'land': 'USA',
        'info': '🟡 Feste Preise'
    }
}

def apply_custom_gea_header_styling():
    """Wendet GEA Styling mit hellem Header für blaues Logo an"""
    st.markdown("""
    <style>
    /* GEA Header mit hellem Hintergrund für blaues Logo */
    .gea-header-custom {
        background: linear-gradient(135deg, #F5F7FA, #E2E8F0);
        color: #003875;
        padding: 2rem 2.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        display: flex;
        align-items: center;
        box-shadow: 0 8px 32px rgba(0, 82, 163, 0.15);
        position: relative;
        overflow: hidden;
        border: 2px solid #E2E8F0;
    }
    
    .gea-header-custom::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(0, 82, 163, 0.05)"/><circle cx="60" cy="60" r="1.5" fill="rgba(0, 82, 163, 0.05)"/><circle cx="80" cy="30" r="1" fill="rgba(0, 82, 163, 0.05)"/></svg>');
        opacity: 0.4;
    }
    
    .gea-header-content {
        display: flex;
        align-items: center;
        width: 100%;
        position: relative;
        z-index: 1;
    }
    
    .gea-logo {
        width: 120px;
        height: auto;
        margin-right: 2rem;
        /* Kein Filter - zeige blaues Logo */
    }
    
    .gea-header-text h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        color: #003875;
        line-height: 1.1;
    }
    
    .gea-header-text p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        color: #455A64;
        font-weight: 400;
    }
    
    /* Responsive Design für Header */
    @media (max-width: 768px) {
        .gea-header-custom {
            flex-direction: column;
            text-align: center;
            padding: 1.5rem;
        }
        
        .gea-logo {
            margin-right: 0;
            margin-bottom: 1rem;
            width: 100px;
        }
        
        .gea-header-text h1 {
            font-size: 2rem;
        }
        
        .gea-header-text p {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def create_custom_gea_header():
    """Erstellt den GEA Header mit Logo auf hellem Hintergrund"""
    
    header_html = """
    <div class="gea-header-custom">
        <div class="gea-header-content">
            <svg viewBox="0 0 85 27" fill="#0303B8" xmlns="http://www.w3.org/2000/svg" class="gea-logo">
                <path d="M71.761 0.731346H65.3369L61.0542 9.29883L65.8193 9.29983L68.5661 3.8121L79.8574 26.4338H84.6225L71.761 0.731346Z"></path>
                <path d="M69.62 11.4436L13.9448 11.4416L11.8034 15.7253H20.3689V22.1509H12.777C8.08278 22.1509 4.26368 18.3246 4.26368 13.5865C4.26368 8.84841 8.08278 5.01489 12.777 5.01489H22.5022V0.729073L12.777 0.729074C5.73173 0.729074 0 6.49694 0 13.5865C0 20.6761 5.73173 26.4347 12.777 26.4347H24.6516V15.7253H31.0756V26.4347H48.2064L50.3478 22.1509H35.3583V15.7253H57.8157L52.4891 26.4347H57.2519L62.606 15.7253H71.7613L69.62 11.4436Z"></path>
                <path d="M35.3584 5.01396L50.3476 5.01504V0.731292L31.0732 0.728142L31.0736 9.29977H35.3584V5.01396Z"></path>
            </svg>
            <div class="gea-header-text">
                <h1>TCO Analyse Tool</h1>
                <p>Intelligente Kostenschätzung für GEA Zentrifugen</p>
            </div>
        </div>
    </div>
    """
    
    st.markdown(header_html, unsafe_allow_html=True)

def get_energy_agent():
    """Lädt Energy Agent falls verfügbar"""
    try:
        from energy.energy_agent import EnergyAgent
        return EnergyAgent()
    except ImportError:
        return None

def get_electricity_price(standort, energy_agent=None):
    """Holt Strompreis für Standort"""
    standort_config = STANDORTE.get(standort, STANDORTE['Düsseldorf (HQ)'])
    
    if standort_config['strom'] == 'ENERGY_AGENT' and energy_agent:
        try:
            price, source, is_realtime = energy_agent.get_current_electricity_price(standort)
            return price, f"Live: {source}", is_realtime
        except:
            # Fallback zu festen Preisen
            fallback_prices = {'Düsseldorf (HQ)': 0.28, 'Kopenhagen': 0.32, 'Mailand': 0.25, 'Lyon': 0.24, 'Berlin': 0.27}
            return fallback_prices.get(standort, 0.28), "Fallback", False
    else:
        # Feste Preise
        return standort_config['strom'], "Fest", False

def load_excel_data(uploaded_file=None):
    """Lädt Excel-Daten - Upload oder Fallback"""
    try:
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file, sheet_name='Ausgewählte LISTE - Final')
            st.success("✅ Ihre Excel-Datei wurde geladen")
        else:
            # Fallback auf vorhandene Datei
            df = pd.read_excel('HinterlandHack _ FinaleListe.xlsx', sheet_name='Ausgewählte LISTE - Final')
            st.info("📁 Standard Excel-Datei wird verwendet")
        
        return df
    except Exception as e:
        st.error(f"❌ Fehler beim Laden: {e}")
        return None

def estimate_dmr_from_model(model_name):
    """Schätzt DMR aus Modellname"""
    if pd.isna(model_name):
        return 500
    
    # Extrahiere Zahlen aus Modellname
    numbers = re.findall(r'\d+', str(model_name))
    if numbers:
        first_number = int(numbers[0])
        # GFA 200 → DMR 200, etc.
        if first_number < 1000:  # Sinnvolle DMR-Werte
            return first_number
    
    return 500  # Fallback

def estimate_dmr_from_capacity(capacity_max):
    """Schätzt DMR aus Kapazität falls Modellname nicht funktioniert"""
    if pd.isna(capacity_max):
        return 500
    
    if capacity_max < 5000:
        return 300   # Kleine Zentrifuge
    elif capacity_max < 20000:
        return 500   # Mittlere Zentrifuge  
    else:
        return 800   # Große Zentrifuge

def calculate_service_cost(dmr):
    """Berechnet Service-Kosten basierend auf DMR"""
    if dmr < 400:
        return 10000
    elif dmr <= 700:
        return 15000
    else:
        return 20000

def calculate_simple_tco(row, standort='Düsseldorf (HQ)', betriebsstunden_woche=40, nutzungsdauer_jahre=15, energy_agent=None):
    """TCO-Berechnung mit Diskontierung (5%) - Jahr für Jahr"""
    purchase_price = row.get('Listprice', 0)  # Spalte K
    
    # DMR schätzen
    dmr = estimate_dmr_from_model(row.get('SEP_SQLLangtyp'))
    if dmr == 500:  # Fallback verwendet
        dmr = estimate_dmr_from_capacity(row.get('SEP_CapacityMaxInp'))
    
    # SERVICE-KOSTEN: Alle 8000h ODER 24 Monate (was zuerst kommt)
    service_cost_per_service = calculate_service_cost(dmr)
    
    # Berechne Service-Zyklen
    gesamt_betriebsstunden = betriebsstunden_woche * 52 * nutzungsdauer_jahre
    service_zyklen_stunden = max(1, int(gesamt_betriebsstunden / 8000))  # Alle 8000h
    service_zyklen_zeit = max(1, int(nutzungsdauer_jahre / 2))           # Alle 24 Monate
    service_zyklen_gesamt = max(service_zyklen_stunden, service_zyklen_zeit)
    
    # ENERGIE-KOSTEN (jährlich)
    power_consumption_spalte_z = row.get('power consumption TOTAL [kW]', 20)
    electricity_price, price_source, is_realtime = get_electricity_price(standort, energy_agent)
    annual_energy_kwh = power_consumption_spalte_z * betriebsstunden_woche * 52
    annual_energy_cost = annual_energy_kwh * electricity_price
    
    # WASSER-KOSTEN (jährlich)
    water_consumption_spalte_p = row.get('SEP_SQLOpWaterls', 1.0)  # L/s
    water_price = STANDORTE[standort]['wasser']
    annual_water_liters = water_consumption_spalte_p * 60 * (betriebsstunden_woche * 60) * 52
    annual_water_cost = annual_water_liters * water_price
    
    # SERVICE-KOSTEN (jährlich verteilt)
    annual_service_cost = (service_cost_per_service * service_zyklen_gesamt) / nutzungsdauer_jahre
    
    # DISKONTIERUNG - Jahr für Jahr
    discount_rate = 0.05  # 5% Diskontsatz
    
    # Anschaffung (Jahr 0, nicht diskontiert)
    discounted_tco = purchase_price
    
    # Jährliche Betriebskosten Jahr für Jahr diskontieren
    total_undiscounted_operating = 0
    total_discounted_operating = 0
    
    for year in range(1, nutzungsdauer_jahre + 1):
        # Jährliche Betriebskosten
        yearly_operating = annual_energy_cost + annual_water_cost + annual_service_cost
        total_undiscounted_operating += yearly_operating
        
        # Diskontierung für dieses Jahr
        discount_factor = (1 + discount_rate) ** year
        discounted_yearly = yearly_operating / discount_factor
        total_discounted_operating += discounted_yearly
    
    # Gesamt-TCO (diskontiert)
    discounted_tco += total_discounted_operating
    
    # Undiskontierte TCO zum Vergleich
    undiscounted_tco = purchase_price + total_undiscounted_operating
    
    return {
        'purchase_price': purchase_price,
        'annual_service_cost': annual_service_cost,
        'annual_energy_cost': annual_energy_cost,
        'annual_water_cost': annual_water_cost,
        'total_service_cost': service_cost_per_service * service_zyklen_gesamt,
        'total_energy_cost': annual_energy_cost * nutzungsdauer_jahre,
        'total_water_cost': annual_water_cost * nutzungsdauer_jahre,
        'total_tco': discounted_tco,  # DISKONTIERTE TCO als Hauptwert
        'undiscounted_tco': undiscounted_tco,  # Zum Vergleich
        'total_discounted_operating': total_discounted_operating,
        'total_undiscounted_operating': total_undiscounted_operating,
        'discount_rate': discount_rate,
        'dmr': dmr,
        'service_cost_per_service': service_cost_per_service,
        'service_zyklen_gesamt': service_zyklen_gesamt,
        'annual_energy_kwh': annual_energy_kwh,
        'annual_water_liters': annual_water_liters,
        'electricity_price': electricity_price,
        'price_source': price_source,
        'is_realtime': is_realtime,
        'betriebsstunden_woche': betriebsstunden_woche,
        'nutzungsdauer_jahre': nutzungsdauer_jahre,
        'gesamt_betriebsstunden': gesamt_betriebsstunden
    }

def show():
    """Reduziertes Dashboard mit Maschinen-Vergleich"""
    
    # GEA Styling anwenden (falls verfügbar)
    if STYLING_AVAILABLE:
        apply_gea_styling()
    
    # Custom Header Styling
    apply_custom_gea_header_styling()
    
    # GEA Header mit Logo auf hellem Hintergrund
    create_custom_gea_header()
    
    # Excel Upload
    st.markdown("## 📁 Excel-Datei")
    uploaded_file = st.file_uploader(
        "Excel-Datei hochladen (optional)", 
        type=['xlsx'], 
        help="Wenn keine Datei hochgeladen wird, wird die Standard-Datei verwendet"
    )
    
    # Daten laden
    df = load_excel_data(uploaded_file)
    if df is None:
        st.stop()
    
    # Session State für DataFrame speichern
    st.session_state['df'] = df
    
    # Energy Agent laden
    energy_agent = get_energy_agent()
    if energy_agent:
        st.success("⚡ Energy Agent aktiv - Live Strompreise verfügbar")
    else:
        st.warning("⚠️ Energy Agent nicht verfügbar - verwende feste Strompreise")
    
    st.markdown("---")
    
    # Auswahl 1: Application
    st.markdown("## 🔧 Maschinen-Auswahl")
    
    applications = df['Application'].dropna().unique()
    selected_application = st.selectbox(
        "1. Application auswählen:",
        options=['Bitte wählen...'] + list(applications),
        key="app_select"
    )
    
    if selected_application != 'Bitte wählen...':
        # Filter DataFrame
        filtered_df = df[df['Application'] == selected_application]
        
        # Auswahl 2: Sub Application
        sub_applications = filtered_df['Sub Application'].dropna().unique()
        selected_sub_application = st.selectbox(
            "2. Sub Application auswählen:",
            options=['Bitte wählen...'] + list(sub_applications),
            key="sub_app_select"
        )
        
        if selected_sub_application != 'Bitte wählen...':
            # Filter weiter - ALLE Maschinen anzeigen
            filtered_df2 = filtered_df[filtered_df['Sub Application'] == selected_sub_application]
            
            if len(filtered_df2) > 0:
                st.markdown("---")
                st.markdown("## 🏭 Maschinen-Vergleich")
                st.markdown(f"**{selected_application} → {selected_sub_application}**")
                
                # Erweiterte Optionen für Standort + Betriebsstunden + Nutzungsdauer
                with st.expander("⚙️ Erweiterte Optionen"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        standort = st.selectbox(
                            "🌍 Standort der Maschine:",
                            options=list(STANDORTE.keys()),
                            index=0,  # Düsseldorf als Default
                            key="standort_select"
                        )
                        
                        # Standort-Info anzeigen
                        standort_info = STANDORTE[standort]
                        st.info(f"📍 **{standort}** ({standort_info['land']}) - {standort_info['info']}")
                    
                    with col2:
                        betriebsstunden_woche = st.number_input(
                            "⏰ Betriebsstunden pro Woche:",
                            min_value=1,
                            max_value=168,  # 24h × 7 Tage
                            value=40,       # Standard 40h/Woche
                            step=1,
                            key="hours_select",
                            help="Anzahl Stunden pro Woche, die die Maschine läuft"
                        )
                        
                        # Zusätzliche Info
                        jahresstunden = betriebsstunden_woche * 52
                        st.write(f"💡 **{jahresstunden:,} Stunden/Jahr** ({betriebsstunden_woche}h/Woche × 52 Wochen)")
                        
                        # Nutzungskategorie anzeigen
                        if betriebsstunden_woche <= 20:
                            nutzung = "🟢 Geringe Nutzung"
                        elif betriebsstunden_woche <= 40:
                            nutzung = "🟡 Standard Nutzung"
                        elif betriebsstunden_woche <= 80:
                            nutzung = "🟠 Intensive Nutzung"
                        else:
                            nutzung = "🔴 24/7 Betrieb"
                        
                        st.write(f"📊 {nutzung}")
                    
                    with col3:
                        nutzungsdauer_jahre = st.number_input(
                            "📅 Nutzungsdauer (Jahre):",
                            min_value=1,
                            max_value=30,
                            value=15,       # Standard 15 Jahre
                            step=1,
                            key="lifetime_select",
                            help="Geplante Nutzungsdauer der Maschine"
                        )
                        
                        # Zusätzliche Info über Nutzungsdauer
                        gesamt_betriebsstunden = jahresstunden * nutzungsdauer_jahre
                        st.write(f"💡 **{gesamt_betriebsstunden:,} Gesamt-Stunden** ({nutzungsdauer_jahre} Jahre)")
                        
                        # Service-Zyklen berechnen
                        service_zyklen = max(1, int(gesamt_betriebsstunden / 8000))  # Alle 8000h
                        service_zyklen_zeit = max(1, int(nutzungsdauer_jahre / 2))   # Alle 24 Monate
                        service_zyklen_gesamt = max(service_zyklen, service_zyklen_zeit)
                        
                        st.write(f"🔧 **{service_zyklen_gesamt} Services** (alle 8000h oder 24 Monate)")
                        
                        # Nutzungskategorie nach Dauer
                        if nutzungsdauer_jahre <= 5:
                            dauer_kategorie = "🔵 Kurzzeitnutzung"
                        elif nutzungsdauer_jahre <= 10:
                            dauer_kategorie = "🟡 Standard-Nutzung"
                        elif nutzungsdauer_jahre <= 20:
                            dauer_kategorie = "🟠 Langzeit-Nutzung"
                        else:
                            dauer_kategorie = "🔴 Sehr langfristig"
                        
                        st.write(f"📈 {dauer_kategorie}")
                
                # TCO für alle Maschinen berechnen
                comparison_data = []
                
                for idx, machine_row in filtered_df2.iterrows():
                    model = machine_row.get('SEP_SQLLangtyp', 'N/A')
                    if pd.notna(model):
                        tco_result = calculate_simple_tco(machine_row, standort, betriebsstunden_woche, nutzungsdauer_jahre, energy_agent)
                        
                        comparison_data.append({
                            'Modell': model,
                            'Anschaffung': f"€{tco_result['purchase_price']:,.0f}",
                            'TCO': f"€{tco_result['total_tco']:,.0f}",
                            'TCO/Jahr': f"€{tco_result['total_tco']/nutzungsdauer_jahre:,.0f}",
                            'Energie/Jahr': f"€{tco_result['annual_energy_cost']:,.0f}",
                            'Wasser/Jahr': f"€{tco_result['annual_water_cost']:,.0f}",
                            'Services': f"{tco_result['service_zyklen_gesamt']}×",
                            'kWh/Jahr': f"{tco_result['annual_energy_kwh']:,.0f}",
                            'DMR': f"{tco_result['dmr']} mm",
                            # Rohdaten für Sortierung
                            '_tco_raw': tco_result['total_tco'],
                            '_purchase_raw': tco_result['purchase_price'],
                            '_machine_row': machine_row  # Für What-if Analyse
                        })
                
                if comparison_data:
                    # Sortiere nach TCO
                    comparison_data.sort(key=lambda x: x['_tco_raw'])
                    
                    # Erstelle DataFrame für Anzeige (ohne Rohdaten)
                    display_columns = ['Modell', 'Anschaffung', 'TCO', 'TCO/Jahr', 'Energie/Jahr', 'Wasser/Jahr', 'Services', 'kWh/Jahr', 'DMR']
                    display_data = [{k: v for k, v in row.items() if k in display_columns} for row in comparison_data]
                    
                    comparison_df = pd.DataFrame(display_data)
                    
                    # Highlight beste Option
                    st.markdown("### 🏆 TCO-Ranking")
                    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
                    
                    # Beste Option hervorheben
                    best_machine = comparison_data[0]
                    st.success(f"🥇 **Beste TCO-Option:** {best_machine['Modell']} mit {best_machine['TCO']} über {nutzungsdauer_jahre} Jahre")
                    
                    # Berechnungs-Info anzeigen
                    st.markdown("### 📋 Berechnungsgrundlage")
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        sample_tco = calculate_simple_tco(filtered_df2.iloc[0], standort, betriebsstunden_woche, nutzungsdauer_jahre, energy_agent)
                        st.write("**⚡ Energiekosten-Berechnung:**")
                        st.write(f"• Spalte Z (Power): {filtered_df2.iloc[0].get('power consumption TOTAL [kW]', 'N/A')} kW")
                        st.write(f"• Betriebsstunden: {betriebsstunden_woche}h/Woche × {nutzungsdauer_jahre} Jahre")
                        st.write(f"• Strompreis: €{sample_tco['electricity_price']:.4f}/kWh")
                        st.write(f"• Jahresverbrauch: {sample_tco['annual_energy_kwh']:,.0f} kWh")
                        st.write(f"• Gesamt-Betriebsstunden: {sample_tco['gesamt_betriebsstunden']:,.0f}h")
                    
                    with col4:
                        st.write("**💧 Wasserkosten-Berechnung:**")
                        st.write(f"• Spalte P (Water): {filtered_df2.iloc[0].get('SEP_SQLOpWaterls', 'N/A')} L/s")
                        st.write(f"• Betriebsstunden: {betriebsstunden_woche}h/Woche × {nutzungsdauer_jahre} Jahre")
                        st.write(f"• Wasserpreis: €{STANDORTE[standort]['wasser']:.4f}/L")
                        st.write(f"• Jahresverbrauch: {sample_tco['annual_water_liters']:,.0f} L")
                        st.write(f"• Service-Zyklen: {sample_tco['service_zyklen_gesamt']}× (alle 8000h oder 24 Monate)")
                    
                    # What-if Analyse Sektion - Beste Maschine verwenden
                    st.markdown("### 🔮 What-if Analyse")
                    st.markdown("**Wie ändert sich die TCO wenn...?**")
                    
                    # Beste Maschine als Referenz verwenden
                    beste_maschine_data = best_machine['_machine_row']  # Beste Maschine aus Ranking
                    beste_tco = calculate_simple_tco(beste_maschine_data, standort, betriebsstunden_woche, nutzungsdauer_jahre, energy_agent)
                    
                    st.info(f"🎯 **Referenz:** {best_machine['Modell']} - Beste TCO: €{beste_tco['total_tco']:,.0f}")
                    
                    # What-if Buttons in Spalten
                    what_if_col1, what_if_col2, what_if_col3 = st.columns(3)
                    
                    with what_if_col1:
                        st.markdown("**⚡ Energiepreise:**")
                        
                        if st.button("📈 Strom +20%", key="strom_plus", help="Strompreis um 20% erhöhen"):
                            # Simuliere höheren Strompreis
                            new_electricity_price = beste_tco['electricity_price'] * 1.2
                            what_if_energy_cost = beste_tco['annual_energy_kwh'] * new_electricity_price * nutzungsdauer_jahre
                            what_if_tco = (beste_tco['total_tco'] - beste_tco['total_energy_cost'] + what_if_energy_cost)
                            differenz = what_if_tco - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            
                            if differenz > 0:
                                st.error(f"📈 **+€{differenz:,.0f}** (+{prozent:.1f}%)")
                                st.write(f"Neue TCO: €{what_if_tco:,.0f}")
                            
                        if st.button("📉 Strom -15%", key="strom_minus", help="Strompreis um 15% senken"):
                            new_electricity_price = beste_tco['electricity_price'] * 0.85
                            what_if_energy_cost = beste_tco['annual_energy_kwh'] * new_electricity_price * nutzungsdauer_jahre
                            what_if_tco = (beste_tco['total_tco'] - beste_tco['total_energy_cost'] + what_if_energy_cost)
                            differenz = what_if_tco - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            
                            if differenz < 0:
                                st.success(f"📉 **{differenz:,.0f}€** ({prozent:.1f}%)")
                                st.write(f"Neue TCO: €{what_if_tco:,.0f}")
                    
                    with what_if_col2:
                        st.markdown("**⏰ Betriebszeiten:**")
                        
                        if st.button("⬆️ +50% Stunden", key="hours_plus", help="50% mehr Betriebsstunden"):
                            new_hours = betriebsstunden_woche * 1.5
                            what_if_tco_result = calculate_simple_tco(beste_maschine_data, standort, new_hours, nutzungsdauer_jahre, energy_agent)
                            differenz = what_if_tco_result['total_tco'] - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            
                            st.error(f"⬆️ **+€{differenz:,.0f}** (+{prozent:.1f}%)")
                            st.write(f"Von {betriebsstunden_woche}h → {new_hours:.0f}h/Woche")
                            st.write(f"Neue TCO: €{what_if_tco_result['total_tco']:,.0f}")
                        
                        if st.button("⬇️ -25% Stunden", key="hours_minus", help="25% weniger Betriebsstunden"):
                            new_hours = betriebsstunden_woche * 0.75
                            what_if_tco_result = calculate_simple_tco(beste_maschine_data, standort, new_hours, nutzungsdauer_jahre, energy_agent)
                            differenz = what_if_tco_result['total_tco'] - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            
                            st.success(f"⬇️ **{differenz:,.0f}€** ({prozent:.1f}%)")
                            st.write(f"Von {betriebsstunden_woche}h → {new_hours:.0f}h/Woche")
                            st.write(f"Neue TCO: €{what_if_tco_result['total_tco']:,.0f}")
                    
                    with what_if_col3:
                        st.markdown("**📅 Nutzungsdauer:**")
                        
                        if st.button("📈 +5 Jahre", key="years_plus", help="5 Jahre längere Nutzung"):
                            new_years = nutzungsdauer_jahre + 5
                            what_if_tco_result = calculate_simple_tco(beste_maschine_data, standort, betriebsstunden_woche, new_years, energy_agent)
                            differenz = what_if_tco_result['total_tco'] - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            tco_per_year_old = beste_tco['total_tco'] / nutzungsdauer_jahre
                            tco_per_year_new = what_if_tco_result['total_tco'] / new_years
                            
                            st.error(f"📈 **+€{differenz:,.0f}** (+{prozent:.1f}%)")
                            st.write(f"Von {nutzungsdauer_jahre} → {new_years} Jahre")
                            st.success(f"💡 TCO/Jahr: €{tco_per_year_new:,.0f} (vs. €{tco_per_year_old:,.0f})")
                        
                        if st.button("📉 -5 Jahre", key="years_minus", help="5 Jahre kürzere Nutzung"):
                            new_years = max(1, nutzungsdauer_jahre - 5)
                            what_if_tco_result = calculate_simple_tco(beste_maschine_data, standort, betriebsstunden_woche, new_years, energy_agent)
                            differenz = what_if_tco_result['total_tco'] - beste_tco['total_tco']
                            prozent = (differenz / beste_tco['total_tco']) * 100
                            tco_per_year_old = beste_tco['total_tco'] / nutzungsdauer_jahre
                            tco_per_year_new = what_if_tco_result['total_tco'] / new_years
                            
                            st.success(f"📉 **{differenz:,.0f}€** ({prozent:.1f}%)")
                            st.write(f"Von {nutzungsdauer_jahre} → {new_years} Jahre")
                            st.error(f"⚠️ TCO/Jahr: €{tco_per_year_new:,.0f} (vs. €{tco_per_year_old:,.0f})")
                        
                        # Reset Button
                        if st.button("🔄 Reset", key="reset_whatif", help="Zurück zu Original-Parametern"):
                            st.info("🔄 Parameter zurückgesetzt")
                    
                    # Key Insights
                    st.markdown("---")
                    st.markdown("### 💡 Key Insights")
                    col_insight1, col_insight2 = st.columns(2)
                    
                    with col_insight1:
                        # Größter Kostentreiber
                        cost_factors = {
                            'Anschaffung': beste_tco['purchase_price'],
                            'Energie': beste_tco['total_energy_cost'],
                            'Service': beste_tco['total_service_cost'],
                            'Wasser': beste_tco['total_water_cost']
                        }
                        biggest_factor = max(cost_factors, key=cost_factors.get)
                        biggest_value = cost_factors[biggest_factor]
                        biggest_percent = (biggest_value / beste_tco['total_tco']) * 100
                        
                        st.write(f"🎯 **Größter Kostenfaktor:** {biggest_factor}")
                        st.write(f"   €{biggest_value:,.0f} ({biggest_percent:.1f}% der TCO)")
                    
                    with col_insight2:
                        # Optimierungspotential
                        energy_ratio = (beste_tco['total_energy_cost'] / beste_tco['total_tco']) * 100
                        if energy_ratio > 20:
                            st.write("⚡ **Energieoptimierung lohnt sich!**")
                            st.write(f"   {energy_ratio:.1f}% der TCO sind Energiekosten")
                        else:
                            st.write("💡 **Fokus auf andere Faktoren**")
                            st.write(f"   Energieanteil nur {energy_ratio:.1f}%")
                
                else:
                    st.warning("⚠️ Keine Maschinen gefunden für diese Kombination")
            else:
                st.warning("⚠️ Keine Daten für diese Sub Application gefunden")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        © 2025 GEA Group | TCO Insight Tool | Engineering for a better world
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    show()