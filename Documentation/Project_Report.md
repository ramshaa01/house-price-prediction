# Ames House Price Prediction System: Comprehensive Capstone Project Report

**Program:** Artificial Intelligence and Machine Learning (AIML) Summer Internship Program  
**Project:** Capstone Project - House Price Prediction System  
**Status:** Completed & Demo-Ready  

---

## 1. Executive Summary & Problem Understanding
Residential real estate valuation is a multi-dimensional challenge influenced by structural square footage, location demographics, building quality, property age, and optional amenities. Traditional appraisal practices frequently rely on human heuristics, introducing subjectivity and pricing opacity.

The primary objective of this project is to construct an end-to-end Machine Learning pipeline that reliably predicts house prices with high accuracy ($R^2 \ge 0.85$). The system encompasses the complete 8-phase ML lifecycle, from problem formulation, data cleaning, and feature engineering to multi-model benchmarking and interactive deployment via Streamlit.

---

## 2. Dataset Selection & Inspection (Phase 1 & 2)
The model was trained on the benchmark **Ames Housing Dataset** (Kaggle / OpenML `house_prices`):
- **Raw Observations:** 1,460 residential properties
- **Attributes:** 81 structural and spatial features
- **Target Variable:** `SalePrice` (Continuous numeric variable in USD)

Key attributes analyzed:
- `GrLivArea`: Above grade (ground) living area square feet.
- `TotalBsmtSF`: Total square feet of basement area.
- `YearBuilt`: Original construction date.
- `YearRemodAdd`: Remodel date.
- `OverallQual`: Overall material and finish rating (1–10 scale).
- `OverallCond`: Overall condition rating (1–10 scale).
- `Neighborhood`: Physical location within Ames city limits.
- `FullBath` & `HalfBath`: Bathroom configurations.
- `GarageCars`: Size of garage in car capacity.
- `PoolArea`: Pool area in square feet.

---

## 3. Data Preprocessing & Pipeline Architecture (Phase 3)
1. **Outlier Filtering:**
   - Properties exceeding 4,000 sq ft in `GrLivArea` were identified as abnormal outliers as documented by Dean De Cock (Ames assessor) and removed to prevent skewing linear weights. Cleaned sample size: **1,456 records**.
2. **Missing Value Imputation:**
   - Quantitative features: Imputed using **median** to safeguard against skewness.
   - Categorical features: Imputed with constant label `"Missing"` / `"None"`.
3. **Target Normalization:**
   - `SalePrice` displays substantial right-skewness. A logarithmic transformation $y' = \ln(1 + \text{SalePrice})$ was applied prior to training, ensuring that residuals conform to homoscedasticity assumptions.
4. **Encoding & Scaling:**
   - Packaged inside an integrated `scikit-learn` `ColumnTransformer` pipeline:
     - Numerical features: `StandardScaler` (zero mean, unit variance).
     - Categorical features: `OneHotEncoder(handle_unknown='ignore')`.
   - **Verification Assertion:** Strict validation confirmed **0 null values** across transformed matrices.

---

## 4. Exploratory Data Analysis Insights (Phase 4)
- **Target Distribution:** Log-transformation converted the raw right-skewed distribution into an approximately Gaussian bell curve, stabilizing regression variance.
- **Living Area vs. Price:** A strong positive linear relationship exists between living area and sale price, with distinct separation across overall quality tiers.
- **Neighborhood Variance:** Substantial geographic price disparities exist, with premium neighborhoods like *Northridge Heights (NridgHt)*, *Stone Brook (StoneBr)*, and *Somerset (Somerst)* commanding significant premiums over *Edwards* or *Old Town*.
- **Top Linear Correlations:**
  1. `OverallQual` ($r = 0.79$)
  2. `GrLivArea` ($r = 0.71$)
  3. `GarageCars` ($r = 0.64$)
  4. `TotalBsmtSF` ($r = 0.61$)
  5. `FullBath` ($r = 0.56$)

All corresponding figures have been rendered to high-resolution PNGs in the `Images/` folder.

---

## 5. Domain Feature Engineering (Phase 5)
Domain-specific variables were engineered to capture composite real-estate drivers:
- **`Property_Age`:** `2010 - YearBuilt` (quantifies structural depreciation).
- **`Total_Living_Area`:** `GrLivArea + TotalBsmtSF` (comprehensive usable square footage).
- **`Total_Bathrooms`:** `FullBath + 0.5*HalfBath + BsmtFullBath + 0.5*BsmtHalfBath`.
- **`Has_Pool`:** Binary indicator (`PoolArea > 0`).
- **`Has_Garage`:** Binary indicator (`GarageCars > 0`).
- **`Is_Remodeled`:** Binary flag (`YearRemodAdd > YearBuilt`).

---

## 6. Model Training & Cross-Validation (Phase 6)
Four distinct machine learning architectures were trained on an 80/20 train-test split (`random_state=42`) with 5-fold cross-validation:
1. **Ridge Regression:** Regularized L2 linear model ($\alpha = 10.0$).
2. **Decision Tree Regressor:** Single tree baseline (`max_depth=6`, `min_samples_split=10`).
3. **Random Forest Regressor:** Bagging ensemble (`n_estimators=150`, `max_depth=12`).
4. **XGBoost Regressor:** Gradient boosted decision trees (`n_estimators=200`, `learning_rate=0.05`, `max_depth=4`, `subsample=0.8`).

---

## 7. Model Evaluation & Comparison (Phase 7)
All evaluation metrics were calculated on the **original dollar price scale** (via inverse log-transformation $\hat{y} = \exp(\hat{y}') - 1$):

| Model Architecture | MAE ($) | MSE ($) | RMSE ($) | $R^2$ Score | Adjusted $R^2$ | 5-Fold CV $R^2$ (Mean ± Std) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ridge Regression** | **$16,280.23** | **$5.231 \times 10^8$** | **$22,871.54** | **0.9003** | **0.8863** | **0.8918 ± 0.0148** |
| **XGBoost Regressor** | **$15,999.01** | **$5.253 \times 10^8$** | **$22,919.00** | **0.8999** | **0.8858** | **0.8916 ± 0.0265** |
| **Random Forest** | $17,309.61 | $6.444 \times 10^8$ | $25,384.09$ | 0.8772 | 0.8599 | 0.8730 ± 0.0269 |
| **Decision Tree** | $22,916.82 | $1.053 \times 10^9$ | $32,449.46$ | 0.7994 | 0.7711 | 0.7834 ± 0.0264 |

### Key Evaluation Findings:
- **Winning Model:** **Ridge Regression** achieved the highest test $R^2$ of **90.03%** and highest cross-validation stability, closely matched by **XGBoost** ($R^2 = 89.99\%$, lowest MAE of $\$15,999$).
- Both top models surpassed the benchmark target ($R^2 \ge 0.85$).
- Ridge Regression and Preprocessor Pipeline were exported to `Model/best_house_price_model.pkl` and `Model/preprocessor_pipeline.pkl`.

### Top 5 Value Drivers (Feature Importance):
1. **`OverallQual`** (39.40%)
2. **`Total_Living_Area`** (17.89%)
3. **`GarageCars`** (5.55%)
4. **`Has_Garage`** (5.43%)
5. **`Total_Bathrooms`** (4.63%)

---

## 8. Web Application Deployment (Phase 8)
An interactive web application was deployed using **Streamlit**:
- **Sidebar Controls:** Sliders for square footage, basement area, bedrooms, bathrooms, construction year; dropdowns for neighborhoods; toggles for garage, remodel status, and pool.
- **Instant Valuation:** Computes point estimate and dynamic confidence interval ($\pm 1 \text{ MAE}$).
- **"What-If" Analysis:** Instant counterfactual evaluation (e.g., adding a bedroom or executing a remodel).
- **Embedded EDA Dashboard:** Live correlation heatmaps and price distribution graphs.

---

## 9. Limitations & Future Scope
- **Geographic Scope:** Trained strictly on Ames, Iowa data. Transferring to metropolitan markets requires localized retraining.
- **Future Scope:** Incorporating macro-economic indicators (interest rates, inflation) and satellite imagery embeddings.
