import streamlit as st

def apply_gea_styling():
    """Wendet authentisches GEA Corporate Design 2022 auf Streamlit an"""
    
    st.markdown("""
    <style>
    /* GEA 2022 Brand Refresh - Authentische Farbpalette */
    :root {
        --gea-ultramarine: #003875;     /* Hauptfarbe: Ultramarinblau */
        --gea-blue-primary: #0052A3;    /* Primäres Blau */
        --gea-blue-light: #1976D2;      /* Helles Blau */
        --gea-blue-accent: #42A5F5;     /* Akzent Blau */
        --gea-header-start: #1976D2;    /* Heller Startton */
        --gea-header-end: #42A5F5;      /* Noch heller Endton */
        --gea-blue-pale: #E3F2FD;       /* Sehr helles Blau */
        --gea-navy: #1A365D;            /* Dunkles Navy */
        --gea-steel: #455A64;           /* Stahl-Blau */
        --gea-slate: #607D8B;           /* Schiefer-Blau */
        --gea-powder: #CFD8DC;          /* Puderton */
        --gea-white: #FFFFFF;
        --gea-light-gray: #F5F7FA;
        --gea-medium-gray: #E2E8F0;
        --gea-text-dark: #2D3748;
        --gea-text-light: #718096;
    }
    
    /* Global Styling */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    
    /* GEA Header mit Logo-Integration */
    .gea-header {
        background: linear-gradient(135deg, var(--gea-header-start), var(--gea-header-end));
        color: var(--gea-white);
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        position: relative;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 56, 117, 0.3);
    }
    
    .gea-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="20" cy="20" r="2" fill="rgba(255,255,255,0.1)"/><circle cx="60" cy="60" r="1.5" fill="rgba(255,255,255,0.1)"/><circle cx="80" cy="30" r="1" fill="rgba(255,255,255,0.1)"/></svg>');
        opacity: 0.3;
    }
    
    .gea-header h1 {
        margin: 0;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -0.5px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .gea-header p {
        margin: 0.8rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    /* GEA Logo Integration */
    .gea-logo-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1rem;
    }
    
    .gea-logo-text {
        font-family: 'GEA Sans', 'Helvetica Neue', Arial, sans-serif;
        font-size: 4rem;
        font-weight: 900;
        color: var(--gea-white);
        letter-spacing: -2px;
        text-shadow: 0 3px 6px rgba(0,0,0,0.4);
        position: relative;
    }
    
    .gea-logo-text::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--gea-white), transparent);
        border-radius: 2px;
    }
    
    /* Enhanced Button Styling - GEA Blue Variants */
    .stButton > button {
        background: linear-gradient(135deg, var(--gea-blue-primary), var(--gea-blue-light));
        color: var(--gea-white);
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 82, 163, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-blue-primary));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 56, 117, 0.4);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
        box-shadow: 0 3px 8px rgba(0, 56, 117, 0.3);
    }
    
    /* Primary Action Button */
    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-navy));
        box-shadow: 0 6px 16px rgba(0, 56, 117, 0.4);
        font-weight: 700;
        font-size: 1rem;
    }
    
    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: linear-gradient(135deg, var(--gea-navy), var(--gea-ultramarine));
        box-shadow: 0 8px 24px rgba(26, 54, 93, 0.5);
    }
    
    /* GEA Cards/Containers */
    .gea-card {
        background: var(--gea-white);
        border: 2px solid var(--gea-medium-gray);
        border-radius: 12px;
        padding: 1.8rem;
        margin: 1.2rem 0;
        box-shadow: 0 4px 16px rgba(0, 82, 163, 0.08);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .gea-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, var(--gea-blue-primary), var(--gea-blue-light));
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .gea-card:hover {
        border-color: var(--gea-blue-light);
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(0, 82, 163, 0.15);
    }
    
    .gea-card:hover::before {
        opacity: 1;
    }
    
    /* Asset Selection Cards */
    .asset-card {
        background: linear-gradient(135deg, var(--gea-light-gray), var(--gea-white));
        border: 2px solid var(--gea-medium-gray);
        border-radius: 16px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin: 1rem 0;
        min-height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    
    .asset-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(25, 118, 210, 0.1), transparent);
        transition: left 0.5s ease;
    }
    
    .asset-card:hover {
        border-color: var(--gea-blue-primary);
        background: linear-gradient(135deg, var(--gea-blue-pale), var(--gea-white));
        transform: scale(1.03);
        box-shadow: 0 12px 40px rgba(0, 82, 163, 0.15);
    }
    
    .asset-card:hover::before {
        left: 100%;
    }
    
    .asset-card.selected {
        border-color: var(--gea-ultramarine);
        background: linear-gradient(135deg, var(--gea-blue-pale), var(--gea-white));
        box-shadow: 0 8px 32px rgba(0, 56, 117, 0.2);
    }
    
    /* Metrics/KPI Cards - GEA Blue Variants */
    .metric-card {
        background: linear-gradient(135deg, var(--gea-ultramarine), var(--gea-blue-primary));
        color: var(--gea-white);
        border-radius: 12px;
        padding: 1.8rem 1.2rem;
        text-align: center;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(0, 56, 117, 0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 10px 30px rgba(0, 56, 117, 0.4);
    }
    
    .metric-card-secondary {
        background: linear-gradient(135deg, var(--gea-steel), var(--gea-slate));
    }
    
    .metric-card-accent {
        background: linear-gradient(135deg, var(--gea-blue-light), var(--gea-blue-accent));
    }
    
    .metric-value {
        font-size: 2.2rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin: 0.5rem 0 0 0;
        font-weight: 400;
    }
    
    /* Confidence Indicators - Blue Theme */
    .confidence-high { 
        color: var(--gea-blue-primary); 
        font-weight: 700; 
        text-shadow: 0 1px 2px rgba(0,82,163,0.3);
    }
    .confidence-medium { 
        color: var(--gea-steel); 
        font-weight: 600; 
    }
    .confidence-low { 
        color: var(--gea-slate); 
        font-weight: 500; 
    }
    
    /* Progress Indicators */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--gea-blue-primary), var(--gea-blue-light));
        border-radius: 4px;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--gea-light-gray), var(--gea-white));
        border-right: 1px solid var(--gea-medium-gray);
    }
    
    /* Navigation State Indicators */
    .nav-active {
        color: var(--gea-ultramarine);
        font-weight: 700;
    }
    
    .nav-completed {
        color: var(--gea-blue-primary);
        font-weight: 600;
    }
    
    .nav-pending {
        color: var(--gea-text-light);
        font-weight: 400;
    }
    
    /* Success/Info/Warning Messages - GEA Themed */
    .stAlert > div {
        border-radius: 8px;
        border-left-width: 4px;
    }
    
    .stSuccess > div {
        background-color: rgba(25, 118, 210, 0.1);
        border-left-color: var(--gea-blue-primary);
    }
    
    .stInfo > div {
        background-color: rgba(66, 165, 245, 0.1);
        border-left-color: var(--gea-blue-accent);
    }
    
    .stWarning > div {
        background-color: rgba(96, 125, 139, 0.1);
        border-left-color: var(--gea-slate);
    }
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid var(--gea-medium-gray);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > div {
        border: 2px solid var(--gea-medium-gray);
        border-radius: 6px;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus {
        border-color: var(--gea-blue-primary);
        box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
    }
    
    /* Charts and Visualizations */
    .plotly-graph-div {
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 82, 163, 0.1);
    }
    
    /* Footer */
    .gea-footer {
        background: linear-gradient(135deg, var(--gea-light-gray), var(--gea-white));
        color: var(--gea-text-light);
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--gea-medium-gray);
        border-radius: 8px 8px 0 0;
    }
    
    .gea-footer a {
        color: var(--gea-blue-primary);
        text-decoration: none;
        font-weight: 600;
        transition: color 0.3s ease;
    }
    
    .gea-footer a:hover {
        color: var(--gea-ultramarine);
    }
    
    /* Equipment Type Icons */
    .equipment-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 2px 4px rgba(0, 82, 163, 0.3));
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .gea-header h1 {
            font-size: 2rem;
        }
        
        .gea-header p {
            font-size: 1rem;
        }
        
        .gea-logo-text {
            font-size: 2.5rem;
        }
        
        .asset-card {
            min-height: 180px;
            padding: 2rem 1rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
        }
    }
    
    /* Animation Classes */
    @keyframes gea-fade-in {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .gea-animate {
        animation: gea-fade-in 0.6s ease-out;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {display: none;}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--gea-light-gray);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--gea-blue-primary), var(--gea-blue-light));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, var(--gea-ultramarine), var(--gea-blue-primary));
    }
    </style>
    """, unsafe_allow_html=True)

def create_gea_logo_header(title: str, subtitle: str = ""):
    """Erstellt einen GEA-branded Header mit Logo-Styling"""
    
    logo_html = f"""
    <div class="gea-header gea-animate">
        <div class="gea-logo-container">
            <div class="gea-logo-text">GEA</div>
        </div>
        <h1>{title}</h1>
        {f'<p>{subtitle}</p>' if subtitle else ''}
    </div>
    """
    
    return logo_html

def create_metric_card(value: str, label: str, variant: str = "primary") -> str:
    """Erstellt eine GEA-styled Metric Card"""
    
    card_class = {
        "primary": "metric-card",
        "secondary": "metric-card metric-card-secondary", 
        "accent": "metric-card metric-card-accent"
    }.get(variant, "metric-card")
    
    return f"""
    <div class="{card_class}">
        <div class="metric-value">{value}</div>
        <div class="metric-label">{label}</div>
    </div>
    """

def create_equipment_card(icon: str, title: str, description: str, selected: bool = False) -> str:
    """Erstellt eine Equipment-Auswahl-Karte im GEA Design"""
    
    selected_class = " selected" if selected else ""
    
    return f"""
    <div class="asset-card{selected_class}">
        <div class="equipment-icon">{icon}</div>
        <h3 style="margin: 0.5rem 0; color: var(--gea-ultramarine); font-weight: 700;">{title}</h3>
        <p style="margin: 0; color: var(--gea-text-light); font-size: 0.9rem; line-height: 1.4;">{description}</p>
    </div>
    """

def create_gea_footer() -> str:
    """Erstellt einen GEA-branded Footer"""
    
    return """
    <div class="gea-footer">
        <p>© 2025 GEA Group Aktiengesellschaft | TCO Insight Tool | 
        <a href="#" target="_blank">Engineering for a better world</a></p>
    </div>
    """

# Color Palette für externe Verwendung
GEA_COLORS = {
    'ultramarine': '#003875',      # Hauptfarbe
    'blue_primary': '#0052A3',     # Primäres Blau  
    'blue_light': '#1976D2',       # Helles Blau
    'blue_accent': '#42A5F5',      # Akzent Blau
    'blue_pale': '#E3F2FD',        # Sehr helles Blau
    'navy': '#1A365D',             # Dunkles Navy
    'steel': '#455A64',            # Stahl-Blau
    'slate': '#607D8B',            # Schiefer-Blau
    'powder': '#CFD8DC',           # Puderton
    'white': '#FFFFFF',
    'light_gray': '#F5F7FA',
    'medium_gray': '#E2E8F0'
}

if __name__ == "__main__":
    # Test der Styling-Funktionen
    print("🎨 GEA Corporate Design 2022 Style Module ready!")
    print("📊 Verfügbare Funktionen:")
    print("  • apply_gea_styling()")
    print("  • create_gea_logo_header()")
    print("  • create_metric_card()")
    print("  • create_equipment_card()")
    print("  • create_gea_footer()")
    print(f"🎯 {len(GEA_COLORS)} GEA-Farben definiert")