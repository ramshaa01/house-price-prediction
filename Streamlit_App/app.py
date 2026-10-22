import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set Page Config
st.set_page_config(
    page_title="Ames House Price Prediction System",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Relative Paths using pathlib for OS-agnostic compatibility (Windows, Linux, macOS)
APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
MODEL_PATH = BASE_DIR / "Model" / "best_house_price_model.pkl"
PREPROCESSOR_PATH = BASE_DIR / "Model" / "preprocessor_pipeline.pkl"
METADATA_PATH = BASE_DIR / "Model" / "model_metadata.json"
CLEANED_DATA_PATH = BASE_DIR / "Dataset" / "cleaned_house_data.csv"
CSS_PATH = APP_DIR / "style.css"
IMAGES_DIR = BASE_DIR / "Images"

# Load CSS
if CSS_PATH.exists():
    with open(CSS_PATH, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load Artifacts
@st.cache_resource
def load_models_and_data():
    model = joblib.load(MODEL_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    with open(METADATA_PATH, "r", encoding="utf-8") as f:
        metadata = json.load(f)
    df = pd.read_csv(CLEANED_DATA_PATH)
    return model, preprocessor, metadata, df

try:
    model, preprocessor, metadata, df_cleaned = load_models_and_data()
    best_model_name = metadata.get("best_model", "Ridge Regression")
    model_metrics = metadata.get("model_metrics", {}).get(best_model_name, {})
    r2_score = model_metrics.get("R2_Score", 0.9003)
    mae_score = model_metrics.get("MAE", 16280)
except Exception as e:
    st.error(f"Error loading model artifacts: {e}")
    st.stop()

# Header
st.markdown("""
<div class="main-header">
    <h1>🏠 Ames Residential House Price Predictor</h1>
    <p>Machine Learning Capstone Project • End-to-End Property Valuation System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar: Property Attributes
st.sidebar.header("🏡 Property Specifications")

# Numerical inputs
gr_liv_area = st.sidebar.slider("Above Ground Living Area (Sq Ft)", 400, 3800, 1600, step=25)
total_bsmt_sf = st.sidebar.slider("Basement Area (Sq Ft)", 0, 3000, 900, step=25)
year_built = st.sidebar.slider("Year Built", 1900, 2010, 2002, step=1)
bedrooms = st.sidebar.slider("Bedrooms Above Ground", 1, 6, 3, step=1)
full_bath = st.sidebar.slider("Full Bathrooms", 1, 4, 2, step=1)
half_bath = st.sidebar.slider("Half Bathrooms", 0, 2, 1, step=1)

# Categorical & Condition inputs
neighborhood_list = sorted(df_cleaned['Neighborhood'].unique())
default_hood_idx = neighborhood_list.index('CollgCr') if 'CollgCr' in neighborhood_list else 0
neighborhood = st.sidebar.selectbox("Neighborhood / Location", neighborhood_list, index=default_hood_idx)

overall_qual = st.sidebar.slider("Overall Quality Rating (1: Very Poor, 10: Excellent)", 1, 10, 7)
overall_cond = st.sidebar.slider("Overall Condition Rating (1: Very Poor, 10: Excellent)", 1, 10, 5)

# Amenities toggles
st.sidebar.subheader("✨ Amenities & Upgrades")
has_garage = st.sidebar.toggle("Garage Available", value=True)
garage_cars = st.sidebar.slider("Garage Car Capacity", 0, 4, 2) if has_garage else 0
has_pool = st.sidebar.toggle("Swimming Pool", value=False)
is_remodeled = st.sidebar.toggle("Remodeled / Renovated Property", value=True)

# Derive engineered features
property_age = 2010 - year_built
total_living_area = gr_liv_area + total_bsmt_sf
total_bathrooms = full_bath + (0.5 * half_bath)

# Predict Function
def predict_price(area_val, total_area, baths, beds, age, cars, qual, cond, pool, garage, remod, hood):
    input_data = pd.DataFrame([{
        'GrLivArea': area_val,
        'Total_Living_Area': total_area,
        'Total_Bathrooms': baths,
        'BedroomAbvGr': beds,
        'Property_Age': age,
        'GarageCars': cars,
        'OverallQual': qual,
        'OverallCond': cond,
        'Has_Pool': 1 if pool else 0,
        'Has_Garage': 1 if garage else 0,
        'Is_Remodeled': 1 if remod else 0,
        'Neighborhood': hood
    }])
    X_trans = preprocessor.transform(input_data)
    pred_log = model.predict(X_trans)
    return float(np.expm1(pred_log)[0])

pred_price = predict_price(
    gr_liv_area, total_living_area, total_bathrooms, bedrooms,
    property_age, garage_cars, overall_qual, overall_cond,
    has_pool, has_garage, is_remodeled, neighborhood
)

lower_bound = max(0, pred_price - mae_score)
upper_bound = pred_price + mae_score

# Main Dashboard Layout
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Estimated Market Valuation</div>
        <div class="metric-value">${pred_price:,.0f}</div>
        <div class="metric-sub">Expected Valuation Range (± 1 MAE): <b>${lower_bound:,.0f} - ${upper_bound:,.0f}</b></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🔍 Real-Time Property Summary")
    sum_col1, sum_col2, sum_col3 = st.columns(3)
    sum_col1.metric("Total Living Space", f"{total_living_area:,} sq ft", f"{gr_liv_area} above ground")
    sum_col2.metric("Bathrooms / Beds", f"{total_bathrooms} Baths", f"{bedrooms} Bedrooms")
    sum_col3.metric("Property Age", f"{property_age} Years", f"Built {year_built}")

    # What-If Analysis Section
    st.markdown("---")
    st.subheader("💡 'What-If' Scenario Analysis")
    st.write("Evaluate how specific improvements impact property market valuation:")

    col_w1, col_w2 = st.columns(2)

    # What if bedroom added
    price_extra_bed = predict_price(
        gr_liv_area + 200, total_living_area + 200, total_bathrooms, bedrooms + 1,
        property_age, garage_cars, overall_qual, overall_cond,
        has_pool, has_garage, is_remodeled, neighborhood
    )
    bed_delta = price_extra_bed - pred_price
    col_w1.metric(
        label="Add 1 Bedroom (+200 sq ft)",
        value=f"${price_extra_bed:,.0f}",
        delta=f"+${bed_delta:,.0f}" if bed_delta >= 0 else f"-${abs(bed_delta):,.0f}"
    )

    # What if remodeled
    price_remodeled = predict_price(
        gr_liv_area, total_living_area, total_bathrooms, bedrooms,
        property_age, garage_cars, min(10, overall_qual + 1), overall_cond,
        has_pool, has_garage, 1, neighborhood
    )
    remod_delta = price_remodeled - pred_price
    col_w2.metric(
        label="Full Remodel (+1 Quality Rating)",
        value=f"${price_remodeled:,.0f}",
        delta=f"+${remod_delta:,.0f}"
    )

with col2:
    st.subheader("📊 Model Performance & Confidence")
    st.info(f"""
    **Active Production Model:** {best_model_name}  
    **Test Accuracy ($R^2$ Score):** **{r2_score:.2%}**  
    **Mean Absolute Error (MAE):** **${mae_score:,.2f}**  
    **Dataset Size:** 1,456 Ames residential properties
    """)

    # Top drivers info
    st.markdown("""
    **Top Value Drivers Identified:**
    1. **Overall Quality Rating** (Materials & Finish)
    2. **Total Living Area** (Above Ground + Basement)
    3. **Garage Capacity**
    4. **Total Bathrooms**
    5. **Property Age / Renovation Recency**
    """)

# Tabs for EDA Mini-Dashboard
st.markdown("---")
st.subheader("📈 Interactive Exploratory Data Analysis & Diagnostics")
tab1, tab2, tab3 = st.tabs(["Price Distribution", "Correlation Heatmap", "Feature Importance"])

with tab1:
    fig_hist, ax_hist = plt.subplots(figsize=(10, 4.5))
    sns.histplot(df_cleaned['SalePrice'], kde=True, color='#2563eb', ax=ax_hist)
    ax_hist.axvline(pred_price, color='#ef4444', linestyle='--', linewidth=2.5, label=f"Current Prediction: ${pred_price:,.0f}")
    ax_hist.set_title("Sale Price Distribution in Ames Market with Current Prediction", fontsize=12, fontweight='bold')
    ax_hist.set_xlabel("Sale Price ($)")
    ax_hist.legend()
    plt.tight_layout()
    st.pyplot(fig_hist)

with tab2:
    numeric_cols = df_cleaned.select_dtypes(include=[np.number])
    top_cols = numeric_cols.corr()['SalePrice'].abs().sort_values(ascending=False).head(10).index
    fig_corr, ax_corr = plt.subplots(figsize=(9, 6))
    sns.heatmap(numeric_cols[top_cols].corr(), annot=True, fmt=".2f", cmap="Blues", ax=ax_corr)
    ax_corr.set_title("Top 10 Feature Correlations with Sale Price", fontsize=12, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig_corr)

with tab3:
    feat_img_path = IMAGES_DIR / "feature_importance.png"
    if feat_img_path.exists():
        st.image(str(feat_img_path), caption="XGBoost & Tree Ensemble Feature Importances", use_container_width=True)
    else:
        st.write("Feature importance graphic not found.")
