# House Price Prediction System: Comprehensive Viva Defense Guide (California Housing Reference)

**Candidate:** Ramsha Fatima (Roll No.: 2300101530112)  
**Supervisor:** Mr. Arpit Dubey, Assistant Professor  
**Department:** Computer Science & Engineering, United College of Engineering & Research, Prayagraj  
**Affiliation:** Dr. A.P.J. Abdul Kalam Technical University (AKTU) & Innovation and Incubation Hub Foundation, MNNIT Allahabad  

---

## 1. Project Overview & Architecture

### Q1: What is the problem statement and objective of this project?
- **Problem Statement:** Real estate prices are governed by heterogeneous geographical coordinates, neighborhood demographics, and structural dimensions. Manual property appraisal is subjective, time-consuming, and prone to human cognitive bias.
- **Objective:** To construct an automated, end-to-end Machine Learning pipeline that predicts continuous median house prices across California census block groups using geographical location (`longitude`, `latitude`, `ocean_proximity`), demographic indicators (`population`, `households`, `median_income`), and physical room counts (`total_rooms`, `total_bedrooms`, `housing_median_age`).

### Q2: Describe the dataset used in this project.
- **Dataset:** California Housing Prices (`housing.csv`), sourced from the 1990 U.S. Census.
- **Total Records:** 20,640 block groups (districts).
- **Total Features:** 9 input predictors (8 numerical + 1 categorical: `ocean_proximity`).
- **Target Variable:** `median_house_value` (continuous numeric value in USD).

---

## 2. Data Preprocessing & Leakage Prevention

### Q3: What missing values existed in the dataset, and how did you prevent Data Leakage?
- **Missing Value Profile:** Running `df.isnull().sum()` revealed that `total_bedrooms` had 207 missing values (~1% of data). All other 9 columns had zero nulls.
- **Why not drop or fill them before splitting?** Calculating the median across all 20,640 rows before train-test splitting introduces **Data Leakage**—test set statistics bleed into the training partition, creating unrealistically optimistic model validation.
- **Resolution via Pipeline:** The dataset was first split 80/20 (`X_train`: 16,512, `X_test`: 4,128). An automated `ColumnTransformer` was fitted **only on `X_train`** using `SimpleImputer(strategy='median')` for continuous numbers and `StandardScaler()`. The learned median and scaling factors were then applied to `X_test` without recomputing.

### Q4: How was the categorical feature `ocean_proximity` handled?
- **Feature Structure:** Nominal text variable with 5 unique categories: `<1H OCEAN`, `INLAND`, `NEAR OCEAN`, `NEAR BAY`, `ISLAND`.
- **Encoding Technique:** One-Hot Encoding via Scikit-Learn's `OneHotEncoder(handle_unknown='ignore')`.
- **Reason:** Unlike ordinal encoding, One-Hot Encoding does not impose an artificial numerical hierarchy ($1 < 2 < 3$) between geographic zones. Setting `handle_unknown='ignore'` ensures runtime stability if unseen categories appear in live production inputs.

---

## 3. Exploratory Data Analysis (EDA) Insights

### Q5: What were the key findings from Exploratory Data Analysis?
1. **Target Distribution Skewness & Price Cap:** The target variable `median_house_value` is heavily right-skewed with a prominent spike at **\$500,001**. This represents an artificial upper price cap introduced during census data collection.
2. **Dominant Predictor:** `median_income` exhibits the strongest linear correlation with house value ($r = +0.688$), confirming that neighborhood purchasing power is the primary driver of property prices.
3. **Geographic Clustering:** Higher property values are strongly clustered in coastal blocks (`<1H OCEAN`, `NEAR BAY`, `NEAR OCEAN`), whereas `INLAND` locations command significantly lower valuations.

---

## 4. Machine Learning Models & Evaluation

### Q6: Compare the performance of the three models evaluated.

| Model | Algorithm Family | Test RMSE ($) | Test MAE ($) | Test $R^2$ Score | Key Characteristics |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **Linear Regression** | Parametric Baseline | ~72,688 | ~51,000 | ~0.612 | Fast, interpretable; severe underfitting due to non-linear geographic factors. |
| **Random Forest** | Bagging Ensemble | ~49,455 | ~32,900 | ~0.817 | Averages 100 decorrelated trees; captures spatial interactions effectively. |
| **XGBoost (Winner)** | Gradient Tree Boosting | **48,496.32** | **32,452.53** | **0.821** | Sequential error correction via gradient descent; lowest prediction error. |

### Q7: Why did XGBoost outperform Linear Regression and Random Forest?
- **Linear Underfitting:** Linear Regression yielded an $R^2$ of only ~0.61 because geographical coordinates and proximity to the ocean interact non-linearly with income and age.
- **Boosting vs. Bagging:** Random Forest builds independent trees in parallel to reduce variance. XGBoost builds trees sequentially where each successive estimator directly optimizes the residual loss gradients of preceding trees. XGBoost achieved the highest $R^2$ (**0.821**) and lowest MAE (**\$32,452.53**), proving its superior ability to model tabular real estate data.

---

## 5. Web Deployment & Production UI/UX

### Q8: How is the web application deployed, and what user inputs does it accept?
- **UI Frameworks:** Available via both native Flask (`app.py`, `templates/index.html`) and cloud-hosted Streamlit (`Streamlit_App/app.py`).
- **User Inputs:**
  - `longitude` and `latitude` (geographical coordinates)
  - `housing_median_age` (structural age)
  - `total_rooms` & `total_bedrooms` (room counts)
  - `population` & `households` (density metrics)
  - `median_income` (district purchasing power)
  - `ocean_proximity` (categorical dropdown)
- **Live Output:** Instantly computes the estimated median house price using the trained XGBoost model along with visual price distribution comparisons.
