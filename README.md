# Ames House Price Prediction System

An end-to-end Machine Learning Capstone Project developed for the Artificial Intelligence & Machine Learning (AIML) Summer Internship Program.

The system automates residential property valuations using the Ames Housing benchmark dataset, achieving **90.03% test $R^2$ accuracy** across multi-family regression architectures, complete with an interactive Streamlit web dashboard.

---

## 🌐 Live Demo
Access the live interactive property valuation dashboard deployed on Streamlit Community Cloud:
👉 **[Live Streamlit App (Placeholder Link - Deploying)](https://house-price-prediction.streamlit.app)**

---

## 📁 Project Directory Structure

```text
House_Price_Prediction/
│
├── Dataset/
│   ├── raw_house_data.csv             # Raw Ames Housing dataset (1,460 records, 81 columns)
│   └── cleaned_house_data.csv         # Cleaned & feature-engineered dataset
│
├── Notebook/
│   └── house_price_prediction_eda_modeling.ipynb # Fully executed Jupyter notebook (Phases 1-7)
│
├── Model/
│   ├── best_house_price_model.pkl     # Exported winning model (Ridge Regression)
│   ├── preprocessor_pipeline.pkl      # Sklearn ColumnTransformer & Scaling pipeline
│   └── model_metadata.json            # Model parameters, cross-validation & test metrics
│
├── Streamlit_App/
│   ├── app.py                         # Production Streamlit application
│   ├── style.css                      # Custom visual styling & responsive cards
│   └── requirements.txt               # App-specific dependencies
│
├── Documentation/
│   ├── Project_Report.md              # Detailed Capstone Project Report
│   └── Presentation_Summary.md        # Slide-by-slide executive presentation notes
│
├── Images/                            # High-resolution plots for presentations
│   ├── price_distribution_before_after_log.png
│   ├── scatter_area_vs_price.png
│   ├── boxplot_neighborhood_vs_price.png
│   ├── boxplot_quality_vs_price.png
│   ├── correlation_heatmap_top15.png
│   ├── actual_vs_predicted.png
│   ├── residuals_plot.png
│   ├── feature_importance.png
│   └── streamlit_app_screenshot.png
│
├── requirements.txt                   # Complete project dependencies (pinned versions)
├── .gitignore                         # Standard Python/Jupyter ignore rules
└── README.md                          # Quick start documentation
```

---

## 🚀 Quick Start Guide

### 1. Installation
Clone the repository and install dependencies:

```bash
git clone https://github.com/ramshaa01/house-price-prediction.git
cd house-price-prediction
pip install -r requirements.txt
```

### 2. Launch the Streamlit Web Application
To run the interactive house price prediction web interface:

```bash
streamlit run Streamlit_App/app.py
```

Once running, navigate to `http://localhost:8501` in any web browser.

### 3. Launch the Jupyter Notebook
To inspect the step-by-step notebook with interactive visualizations and analysis:

```bash
jupyter notebook Notebook/house_price_prediction_eda_modeling.ipynb
```

---

## 📊 Model Performance Benchmark

Evaluated on a held-out 20% test split (original USD price scale):

| Model Architecture | MAE ($) | RMSE ($) | $R^2$ Score | 5-Fold CV $R^2$ |
| :--- | :---: | :---: | :---: | :---: |
| **Ridge Regression (Best)** | **$16,280.23** | **$22,871.54** | **0.9003** | **0.8918** |
| **XGBoost Regressor** | **$15,999.01** | **$22,919.00** | **0.8999** | **0.8916** |
| **Random Forest** | $17,309.61 | $25,384.09 | 0.8772 | 0.8730 |
| **Decision Tree** | $22,916.82 | $32,449.46 | 0.7994 | 0.7834 |

---

## 🏆 Top 5 Predictive Value Drivers
1. **Overall Quality Rating (`OverallQual`)** — 39.40%
2. **Total Combined Living Area (`Total_Living_Area`)** — 17.89%
3. **Garage Car Capacity (`GarageCars`)** — 5.55%
4. **Presence of Garage (`Has_Garage`)** — 5.43%
5. **Total Bathrooms (`Total_Bathrooms`)** — 4.63%
