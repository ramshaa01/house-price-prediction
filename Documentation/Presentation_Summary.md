# Capstone Presentation Summary: Ames House Price Prediction

Use these slide-by-slide talking points for project presentation and demo reviews.

---

### Slide 1: Title & Executive Summary
- **Title:** Intelligent House Price Prediction System
- **Presenter:** AIML Capstone Project Team
- **Core Mission:** Eliminate pricing opacity in residential real estate through an automated, end-to-end Machine Learning valuation system.
- **Key Result:** Achieved **90.03% test $R^2$** accuracy with an average absolute error of only **$16,280** on real market transactions.

---

### Slide 2: Problem Statement & Objectives
- **Business Need:** Property appraisals are often subjective, inconsistent, and slow. Buyers and lenders need transparent valuations based on verifiable physical attributes.
- **Key Objectives:**
  - Build an end-to-end automated pipeline executing all 8 stages of the ML lifecycle.
  - Engineer domain-specific indicators (living area combinations, age, bathroom ratios).
  - Benchmark multiple machine learning families (Regularized Linear, Decision Trees, Bagging, Gradient Boosting).
  - Deploy an interactive Streamlit application with "What-If" scenario planning.

---

### Slide 3: Dataset & Data Architecture
- **Source:** Ames Housing Dataset (1,460 benchmark sales across 81 attributes).
- **Target Variable:** `SalePrice` in USD.
- **Preprocessing Pipeline:**
  - Outlier filtering: Removed anomalous records with $> 4,000$ sq ft living area (1,456 final records).
  - Imputation: Median for continuous missing values; categorical constants for missing amenity flags.
  - Log Transformation: Applied $\ln(1 + \text{SalePrice})$ to normalize target skewness.
  - Modular `ColumnTransformer`: Standard scaling for continuous features; one-hot encoding for neighborhoods.

---

### Slide 4: Exploratory Data Analysis Key Insights
- **Price Skewness:** Raw prices were heavily right-skewed; logarithmic transform converted them to a near-perfect normal distribution.
- **Primary Correlations:**
  - Overall Material Quality Rating has the highest correlation ($r = 0.79$).
  - Above ground living area shows a strong linear positive relationship ($r = 0.71$).
  - Large price variance observed across geographic neighborhoods (e.g., Northridge vs Old Town).

---

### Slide 5: Feature Engineering
- Domain features engineered:
  - `Property_Age = 2010 - YearBuilt`
  - `Total_Living_Area = Above_Ground_Area + Basement_Area`
  - `Total_Bathrooms = FullBath + 0.5*HalfBath + BsmtFullBath + 0.5*BsmtHalfBath`
  - Binary indicators: `Has_Pool`, `Has_Garage`, `Is_Remodeled`

---

### Slide 6: Model Benchmarking & Results
*Evaluated on held-out 20% test split on the original USD price scale:*

| Model | MAE ($) | RMSE ($) | Test $R^2$ | 5-Fold CV $R^2$ |
| :--- | :---: | :---: | :---: | :---: |
| **Ridge Regression (Winner)** | **$16,280** | **$22,871** | **0.9003** | **0.8918** |
| **XGBoost Regressor** | **$15,999** | **$22,919** | **0.8999** | **0.8916** |
| **Random Forest** | $17,309 | $25,384 | 0.8772 | 0.8730 |
| **Decision Tree** | $22,916 | $32,449 | 0.7994 | 0.7834 |

- Target exceeded: Both Ridge Regression and XGBoost scored $\approx 90\%$, well above the $0.85$ requirement.

---

### Slide 7: Top 5 Feature Importances
1. **Overall Material & Finish Quality (39.4%)**
2. **Total Combined Living Area (17.9%)**
3. **Garage Car Capacity (5.6%)**
4. **Presence of Garage (5.4%)**
5. **Total Bathrooms (4.6%)**

---

### Slide 8: Deployment & Live Streamlit Demo
- **Interactive UI:** Dynamic sliders for square footage, construction year, and room count.
- **Confidence Intervals:** Instant range estimate ($\pm 1$ MAE) around predicted valuation.
- **"What-If" Analysis:** Real-time ROI simulation showing the value impact of adding a bedroom or completing a renovation.
- **Embedded EDA Dashboards:** In-app price distributions and correlation heatmaps.

---

### Slide 9: Conclusion & Next Steps
- Successfully established an institutional-grade automated property valuation pipeline.
- Future enhancements: Integrate automated spatial maps, interest rate curves, and computer vision models for photo-based condition scoring.
