import streamlit as st

def apply_gea_styling():
    """Wendet GEA Corporate Design auf Streamlit an"""
    
    st.markdown("""
    <style>
    /* GEA Farbschema */
    :root {
        --gea-blue: #003366;
        --gea-orange: #FF6600;
        --gea-light-blue: #0066CC;
        --gea-gray: #F5F5F5;
        --gea-dark-gray: #666666;
    }
    
    /* Header Styling */
    .gea-header {
        background: linear-gradient(135deg, var(--gea-blue), var(--gea-light-blue));
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .gea-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .gea-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: var(--gea-orange);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #E55A00;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Primary Button (für wichtige Aktionen) */
    .gea-primary-btn {
        background: linear-gradient(135deg, var(--gea-orange), #FF8800) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        margin: 1rem 0 !important;
    }
    
    /* Cards/Boxes */
    .gea-card {
        background: white;
        border: 2px solid var(--gea-gray);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .gea-card:hover {
        border-color: var(--gea-orange);
        transform: translateY(-3px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    /* Asset-Type Selection Cards */
    .asset-card {
        background: linear-gradient(135deg, #F8F9FA, white);
        border: 2px solid #E9ECEF;
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 1rem;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    
    .asset-card:hover {
        border-color: var(--gea-orange);
        background: linear-gradient(135deg, #FFF8F0, white);
        transform: scale(1.05);
    }
    
    .asset-card.selected {
        border-color: var(--gea-blue);
        background: linear-gradient(135deg, #F0F8FF, white);
    }
    
    /* Progress Steps */
    .step-indicator {
        background: var(--gea-gray);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    /* Metrics/KPI Cards */
    .metric-card {
        background: linear-gradient(135deg, var(--gea-blue), var(--gea-light-blue));
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.8;
        margin: 0;
    }
    
    /* Confidence Indicator */
    .confidence-high { color: #28A745; font-weight: 600; }
    .confidence-medium { color: #FFC107; font-weight: 600; }
    .confidence-low { color: #DC3545; font-weight: 600; }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background-color: var(--gea-gray);
    }
    
    /* Hide Streamlit Menu */
    #MainMenu {visibility: hidden;}
    .stDeployButton {visibility: hidden;}