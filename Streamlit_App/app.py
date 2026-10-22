import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

st.set_page_config(
    page_title="House Price Prediction",
    page_icon="🏠",
    layout="wide"
)

# Paths relative to file
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "California_Model" / "house_price_model.pkl"
DATA_PATH = BASE_DIR / "California_Model" / "housing.csv"

# Load Model and Data
@st.cache_resource
def load_artifacts():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    df = pd.read_csv(DATA_PATH)
    return model, df

model, df = load_artifacts()

# Custom CSS matching clean UI
st.markdown("""
<style>
    .main-title {
        font-family: Arial, sans-serif;
        color: #1e3c72;
        font-size: 2.2rem;
        font-weight: bold;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #555;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .result-card {
        background: #f8f9fa;
        border-left: 5px solid #28a745;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }
    .result-val {
        font-size: 2.2rem;
        font-weight: bold;
        color: #28a745;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">House Price Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">A Machine Learning Approach to Estimating Real Estate Value (California Housing Benchmark)</div>', unsafe_allow_html=True)

col_input, col_out = st.columns([1.1, 1])

with col_input:
    st.subheader("Input Property Features")
    
    col1, col2 = st.columns(2)
    with col1:
        longitude = st.number_input("Longitude", value=-122.23, format="%.4f")
        latitude = st.number_input("Latitude", value=37.88, format="%.4f")
        housing_median_age = st.number_input("Age (Housing Median Age)", min_value=1.0, max_value=52.0, value=41.0, step=1.0)
        total_rooms = st.number_input("Rooms (Total Rooms)", min_value=1.0, value=880.0, step=10.0)
        total_bedrooms = st.number_input("Bedrooms (Total Bedrooms)", min_value=1.0, value=129.0, step=5.0)
    
    with col2:
        population = st.number_input("Population", min_value=1.0, value=322.0, step=10.0)
        households = st.number_input("Households", min_value=1.0, value=126.0, step=5.0)
        median_income = st.number_input("Median Income (in $10,000s)", min_value=0.5, max_value=15.0, value=8.3252, format="%.4f")
        ocean_proximity = st.selectbox(
            "Ocean Proximity",
            ["<1H OCEAN", "INLAND", "NEAR BAY", "NEAR OCEAN", "ISLAND"],
            index=2
        )
        
    predict_clicked = st.button("Predict House Price", use_container_width=True)

with col_out:
    st.subheader("Prediction Result")
    
    # Compute prediction
    input_df = pd.DataFrame([{
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }])
    
    pred_val = model.predict(input_df)[0]
    
    st.markdown(f"""
    <div class="result-card">
        <div style="font-size: 1rem; color: #555;">Estimated Median House Value:</div>
        <div class="result-val">${pred_val:,.2f}</div>
        <div style="color: #666; font-size: 0.9rem; margin-top: 5px;">Model: <b>XGBoost Regressor (Test R² = 0.821, RMSE = $48,496)</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Model Benchmark Comparison (Test Set)")
    metrics_summary = pd.DataFrame({
        "Model": ["Linear Regression", "Random Forest", "XGBoost (Active)"],
        "RMSE ($)": ["~72,688", "~49,455", "48,496.32"],
        "MAE ($)": ["~51,000", "~32,900", "32,452.53"],
        "R² Score": ["~0.612", "~0.817", "0.821"]
    })
    st.dataframe(metrics_summary, use_container_width=True, hide_index=True)

st.markdown("---")
tab1, tab2 = st.tabs(["Target Distribution & Price Cap", "Correlation with Income"])

with tab1:
    fig1, ax1 = plt.subplots(figsize=(8, 3.5))
    sns.histplot(df['median_house_value'], bins=50, kde=True, color='#1f77b4', ax=ax1)
    ax1.axvline(pred_val, color='red', linestyle='--', label=f'Current Prediction: ${pred_val:,.0f}')
    ax1.set_title("Distribution of Median House Value (with $500,001 artificial cap)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Median House Value ($)")
    ax1.legend()
    plt.tight_layout()
    st.pyplot(fig1)

with tab2:
    fig2, ax2 = plt.subplots(figsize=(8, 3.5))
    sample_df = df.sample(1000, random_state=42)
    sns.scatterplot(data=sample_df, x='median_income', y='median_house_value', alpha=0.5, color='#2ca02c', ax=ax2)
    ax2.set_title("Median Income vs. Median House Value (Correlation r = 0.688)", fontsize=11, fontweight='bold')
    ax2.set_xlabel("Median Income (Tens of Thousands $)")
    ax2.set_ylabel("House Value ($)")
    plt.tight_layout()
    st.pyplot(fig2)
