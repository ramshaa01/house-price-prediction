# House Price Prediction System: Comprehensive Viva & Technical Interview Questions

A structured preparation guide for project vivas, capstone evaluations, and machine learning technical interviews based on the Ames House Price Prediction project.

---

## Category 1: Problem Definition, Dataset & Architecture

### Q1: What is the objective of this project, and why did you formulate it as a regression problem?
**Answer:**
The objective is to predict continuous market property values based on structural dimensions, architectural quality, room configurations, property age, and amenities. It is formulated as a **supervised regression** task because the target variable (`SalePrice`) is continuous, quantitative, and numeric ($), unlike classification where outputs are discrete categories.

### Q2: Why choose the Ames Housing dataset over older datasets like the Boston Housing dataset?
**Answer:**
1. **Modernity & Realism:** The Ames dataset (compiled by Dean De Cock) reflects contemporary residential real estate with 81 rich features, whereas Boston Housing is from the 1970s and contains significant data quality and ethical concerns (e.g., racial demographic variables).
2. **Granular Architectural Attributes:** Ames includes detailed structural parameters: basement finish types, quality vs condition scales, garage types, and remodel timestamps, making it an industry-standard benchmark for tabular regression.

### Q3: How did you identify and handle outliers in the dataset?
**Answer:**
- We analyzed scatter plots of `GrLivArea` (above ground living area) against `SalePrice`.
- As recommended in the original Ames assessor documentation, properties with `GrLivArea > 4,000 sq ft` with abnormally low sale prices were anomalous partial/agricultural sales that severely distorted linear slope parameters.
- Removing these 4 records reduced sample noise and prevented high-leverage distortion without causing data starvation.

---

## Category 2: Data Preprocessing & Pipeline Design

### Q4: Why did you apply a $\log(1 + x)$ (`log1p`) transformation to the target variable `SalePrice`?
**Answer:**
1. **Skewness Reduction:** Raw residential house prices are heavily right-skewed (long right tail caused by luxury properties). A log-transformation transforms the distribution into a near-normal Gaussian bell curve.
2. **Homoscedasticity:** It stabilizes error variance across different price regimes, preventing high-priced homes from disproportionately dominating the loss function (Mean Squared Error).
3. **Multiplicative Errors:** It penalizes relative percentage errors uniformly rather than absolute dollar disparities.
4. *Note:* For final evaluation, all predictions were inverse-transformed using $\exp(y) - 1$ (`expm1`) so metrics reflect genuine dollar values.

### Q5: How did you prevent data leakage during preprocessing and feature scaling?
**Answer:**
- We used `scikit-learn`'s `ColumnTransformer` inside an isolated training pipeline.
- The pipeline was fitted strictly on the **training set** (`X_train`) and only used to transform the **test set** (`X_test`).
- Imputation medians and `StandardScaler` ($\mu, \sigma$) values were computed exclusively on `X_train`, preventing information from the test distribution leaking into the model.

### Q6: How were categorical variables handled?
**Answer:**
- **Nominal Variables (e.g., `Neighborhood`):** Encoded using `OneHotEncoder(handle_unknown='ignore', sparse_output=False)` to prevent artificial numerical hierarchies. Setting `handle_unknown='ignore'` guarantees runtime robustness if unseen categories appear in production.
- **Ordinal Variables (e.g., `OverallQual`, `OverallCond`):** Preserved on their calibrated integer scales (1 to 10) because higher values represent higher material quality.

---

## Category 3: Feature Engineering & Multicollinearity

### Q7: What new domain features did you engineer, and what was the rationale?
**Answer:**
1. **`Property_Age` (`2010 - YearBuilt`):** Property age directly captures physical depreciation, obsolete floorplans, and wear-and-tear better than raw calendar years.
2. **`Total_Living_Area` (`GrLivArea + TotalBsmtSF`):** Appraisers and buyers value usable subterranean space in addition to above-grade space.
3. **`Total_Bathrooms` (`FullBath + 0.5*HalfBath + BsmtFullBath + 0.5*BsmtHalfBath`):** Creates a composite measure of plumbing and fixture utility across the entire dwelling.
4. **Binary Amenity Indicators (`Has_Pool`, `Has_Garage`, `Is_Remodeled`):** Sparse features were simplified into high-signal boolean flags.

### Q8: What is multicollinearity, and how did you address it?
**Answer:**
- **Definition:** High linear intercorrelations between independent variables (e.g., `GrLivArea` and `Total_Living_Area`, or `YearBuilt` and `Property_Age`).
- **Consequence:** In ordinary least squares (OLS), multicollinearity causes high variance in coefficient estimates, making them sensitive to minor sample shifts.
- **Remedy:** We used **Ridge Regression (L2 regularization)**, which adds a penalty $\alpha \sum \beta_j^2$ to the loss function. This conditions the matrix inversion $(X^T X + \alpha I)^{-1}$ and shrinks correlated weights jointly without arbitrary feature drops.

---

## Category 4: Model Training, Evaluation & Algorithms

### Q9: Compare the 4 models evaluated in your project.
**Answer:**

| Model | Nature | Strengths | Limitations | Project $R^2$ |
| :--- | :--- | :--- | :--- | :---: |
| **Ridge Regression** | Linear with L2 penalty | Fast, interpretable, handles collinearity well, smooth extrapolation | Misses complex non-linear feature interactions | **0.9003 (Best)** |
| **Decision Tree** | Non-parametric partition | Captures non-linear thresholds, highly interpretable | Prone to high variance and overfitting | **0.7994** |
| **Random Forest** | Bagging ensemble (parallel) | Reduces variance by averaging decorrelated trees | Slower inference, large file size | **0.8772** |
| **XGBoost** | Gradient boosting (sequential) | Optimizes residuals, handles sparsity, tree pruning | Requires tuning ($\eta$, subsample, max_depth) | **0.8999** |

### Q10: Why did Ridge Regression perform slightly better than or comparable to XGBoost?
**Answer:**
- After log-transforming `SalePrice`, the relationship between composite square footage, overall quality rating, and property age is predominantly linear.
- On medium-sized tabular datasets (~1,450 rows), gradient boosted trees can marginally overfit local leaf partitions despite regularization, whereas L2-penalized linear models have low variance and generalize reliably.

### Q11: Explain the difference between MAE, MSE, RMSE, and $R^2$. Why report all of them?
**Answer:**
1. **MAE (Mean Absolute Error):** $\frac{1}{n} \sum |y_i - \hat{y}_i|$. Represents the average expected dollar deviation ($16,280). Robust to extreme outliers.
2. **MSE (Mean Squared Error):** $\frac{1}{n} \sum (y_i - \hat{y}_i)^2$. Heavily penalizes large errors because disparities are squared.
3. **RMSE (Root Mean Squared Error):** $\sqrt{\text{MSE}}$. Restores error to dollar units ($22,871). The spread between RMSE and MAE indicates the magnitude of occasional large residual errors.
4. **$R^2$ (Coefficient of Determination):** $1 - \frac{SS_{\text{res}}}{SS_{\text{tot}}}$. Indicates the proportion of target variance explained by the model ($90.03\%$).
5. **Adjusted $R^2$:** Penalizes adding features that do not improve explanatory power ($88.63\%$).

---

## Category 5: Deployment, Streamlit & Production

### Q12: How does the application generate dynamic confidence bounds?
**Answer:**
Along with the point estimate $\hat{y}$, the app shows an uncertainty range $[\hat{y} - \text{MAE}, \hat{y} + \text{MAE}]$. This gives buyers and sellers realistic valuation bounds rather than a false sense of single-dollar precision.

### Q13: What is the purpose of the "What-If" scenario analyzer?
**Answer:**
It provides counterfactual decision support. A homeowner can test:
- *"What if I finish 200 sq ft and add a bedroom?"* (Simulates $+\Delta \text{SqFt}$ and Bedroom count).
- *"What if I remodel the property to improve quality by 1 level?"*  
The model calculates the marginal financial delta in real time, aiding ROI appraisal.

### Q14: How is production reproducibility and OS compatibility guaranteed?
**Answer:**
1. **OS-Agnostic Pathing:** Uses Python's `pathlib.Path(__file__).resolve().parent.parent` rather than hardcoded Windows backslashes (`\`) or shell-dependent relative paths, allowing cross-platform deployment on Linux (Streamlit Cloud) and Windows.
2. **Pinned Dependency Tree:** Specific package versions (`scikit-learn==1.9.0`, `xgboost==3.2.0`, `joblib==1.5.3`) prevent `UnpicklingError` or incompatible binary serialization bugs.

---

## Category 6: Rapid-Fire / Viva Defense Questions

- **Q: What is K-Fold Cross Validation?**  
  *A:* Splitting data into $K$ equal folds (here $K=5$), iteratively training on $K-1$ folds and validating on the remaining fold to measure out-of-sample generalization variance.
- **Q: What is the most important feature driving house price?**  
  *A:* `OverallQual` (Overall material and finish quality rating), accounting for ~39.4% of total feature importance in tree models, followed by `Total_Living_Area` (~17.9%).
- **Q: Can this model be used immediately in New York or London?**  
  *A:* No. The model was trained on Ames, Iowa market dynamics. Real estate pricing is hyper-local; transfer requires retraining with regional location coordinates and macro-economic factors.
- **Q: How would you monitor this model once deployed?**  
  *A:* Track prediction drift (PSI / Population Stability Index), monitor changes in interest rates / inflation, and periodically retrain on recent quarterly closing transactions.
