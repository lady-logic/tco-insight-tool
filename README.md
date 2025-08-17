# TCO Insight Tool

AI-powered Total Cost of Ownership calculator for enterprise assets using machine learning.

## Features

- **4-Step Asset Wizard** - Intuitive asset creation process
- **Machine Learning Predictions** - Random Forest model trained on 500+ assets
- **Smart Cost Analysis** - Automatic maintenance cost estimation with confidence scoring
- **Interactive Dashboards** - Charts, metrics, and TCO breakdowns
- **Similar Assets Finder** - Benchmark comparisons from training data
- **Professional UI** - Clean, responsive business interface

## Tech Stack

- **Python 3.10+** - Core language
- **Streamlit** - Web framework
- **Scikit-learn** - Machine learning (Random Forest)
- **Pandas** - Data processing
- **Plotly** - Interactive charts

## ML Model Performance

- **R² Score:** ~0.73 (73% variance explained)
- **Mean Absolute Error:** ~€5,300
- **Features:** 13 engineered asset properties
- **Training Data:** 400+ realistic assets

## Usage

1. **Dashboard** - View asset overview and metrics
2. **Add Asset** - Enter asset details through 4-step wizard
3. **AI Analysis** - Get ML-powered cost predictions
4. **TCO Report** - Review complete cost breakdown and recommendations

## Quick Start

```bash
# Clone and setup
git clone https://github.com/yourusername/tco-insight-tool.git
cd tco-insight-tool

# Install dependencies
pip install streamlit plotly pandas scikit-learn joblib

# Generate training data and train ML model
python data/generate_training_data.py
python ml/tco_predictor.py

# Run application
streamlit run app.py