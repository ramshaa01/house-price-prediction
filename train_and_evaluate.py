import os
import json
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set directories
BASE_DIR = r"C:\Users\ramsh\.gemini\antigravity\scratch\House_Price_Prediction"
DATASET_DIR = os.path.join(BASE_DIR, "Dataset")
MODEL_DIR = os.path.join(BASE_DIR, "Model")
IMAGES_DIR = os.path.join(BASE_DIR, "Images")

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

# Styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_palette("crest")

print("--- Phase 1 & 2: Loading Ames Housing Dataset ---")
raw_path = os.path.join(DATASET_DIR, "raw_house_data.csv")
df = pd.read_csv(raw_path)
print(f"Dataset shape: {df.shape}")

# Phase 3 & 5: Feature Engineering & Preprocessing
print("--- Phase 3 & 5: Feature Engineering & Preprocessing ---")
# 1. Feature Engineering
# Current year benchmark based on Ames dataset max year or fixed 2010
df['Property_Age'] = 2010 - df['YearBuilt']
df['Total_Living_Area'] = df['GrLivArea'] + df['TotalBsmtSF'].fillna(0)
df['Total_Bathrooms'] = df['FullBath'] + (0.5 * df['HalfBath']) + df['BsmtFullBath'].fillna(0) + (0.5 * df['BsmtHalfBath'].fillna(0))
df['Has_Pool'] = (df['PoolArea'] > 0).astype(int)
df['Has_Garage'] = (df['GarageCars'].fillna(0) > 0).astype(int)
df['Is_Remodeled'] = (df['YearRemodAdd'] > df['YearBuilt']).astype(int)

# 2. Outlier Treatment (Remove extreme anomalies as recommended in Ames documentation: GrLivArea > 4000)
print(f"Shape before outlier removal: {df.shape}")
df = df[df['GrLivArea'] < 4000].copy()
print(f"Shape after outlier removal: {df.shape}")

# Save cleaned dataset
cleaned_path = os.path.join(DATASET_DIR, "cleaned_house_data.csv")
df.to_csv(cleaned_path, index=False)
print(f"Saved cleaned data to {cleaned_path}")

# Phase 4: Exploratory Data Analysis & Visualizations
print("--- Phase 4: Generating EDA Plots ---")
# Plot 1: SalePrice Distribution Before & After Log Transform
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.histplot(df['SalePrice'], kde=True, ax=axes[0], color='#2b5c8f')
axes[0].set_title("SalePrice Distribution (Raw, Right-Skewed)", fontsize=13, fontweight='bold')
axes[0].set_xlabel("Sale Price ($)")
axes[0].set_ylabel("Frequency")

log_price = np.log1p(df['SalePrice'])
sns.histplot(log_price, kde=True, ax=axes[1], color='#2a9d8f')
axes[1].set_title("Log(SalePrice + 1) Distribution (Normalized)", fontsize=13, fontweight='bold')
axes[1].set_xlabel("Log Sale Price")
axes[1].set_ylabel("Frequency")
plt.tight_layout()
p1 = os.path.join(IMAGES_DIR, "price_distribution_before_after_log.png")
fig.savefig(p1, dpi=300)
plt.close(fig)
print(f"Saved: {p1}")

# Plot 2: Scatter Plot Living Area vs Price
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(data=df, x='GrLivArea', y='SalePrice', hue='OverallQual', palette='viridis', alpha=0.8, ax=ax)
ax.set_title("Above Ground Living Area vs Sale Price", fontsize=14, fontweight='bold')
ax.set_xlabel("Living Area (Sq Ft)")
ax.set_ylabel("Sale Price ($)")
plt.tight_layout()
p2 = os.path.join(IMAGES_DIR, "scatter_area_vs_price.png")
fig.savefig(p2, dpi=300)
plt.close(fig)
print(f"Saved: {p2}")

# Plot 3: Boxplot by Neighborhood
top_hoods = df['Neighborhood'].value_counts().nlargest(10).index
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df[df['Neighborhood'].isin(top_hoods)], x='Neighborhood', y='SalePrice', palette='Set2', ax=ax)
ax.set_title("House Price Distribution across Top 10 Neighborhoods", fontsize=14, fontweight='bold')
ax.set_xlabel("Neighborhood")
ax.set_ylabel("Sale Price ($)")
plt.xticks(rotation=45)
plt.tight_layout()
p3 = os.path.join(IMAGES_DIR, "boxplot_neighborhood_vs_price.png")
fig.savefig(p3, dpi=300)
plt.close(fig)
print(f"Saved: {p3}")

# Plot 4: Boxplot by Overall Quality
fig, ax = plt.subplots(figsize=(9, 5))
sns.boxplot(data=df, x='OverallQual', y='SalePrice', palette='Blues_d', ax=ax)
ax.set_title("Sale Price by Overall Property Quality Rating (1-10)", fontsize=14, fontweight='bold')
ax.set_xlabel("Overall Quality Rating")
ax.set_ylabel("Sale Price ($)")
plt.tight_layout()
p4 = os.path.join(IMAGES_DIR, "boxplot_quality_vs_price.png")
fig.savefig(p4, dpi=300)
plt.close(fig)
print(f"Saved: {p4}")

# Plot 5: Correlation Heatmap (Top 15 Features with SalePrice)
numeric_df = df.select_dtypes(include=[np.number])
top_corr_features = numeric_df.corr()['SalePrice'].abs().sort_values(ascending=False).head(15).index
corr_matrix = numeric_df[top_corr_features].corr()

fig, ax = plt.subplots(figsize=(11, 9))
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', cbar=True, ax=ax, linewidths=0.5)
ax.set_title("Correlation Heatmap: Top 15 Predictors of Sale Price", fontsize=14, fontweight='bold')
plt.tight_layout()
p5 = os.path.join(IMAGES_DIR, "correlation_heatmap_top15.png")
fig.savefig(p5, dpi=300)
plt.close(fig)
print(f"Saved: {p5}")

# Phase 6 & 7: Model Building & Evaluation
print("--- Phase 6 & 7: Pipeline, Training & Evaluation ---")

# Define features used in modeling and Streamlit
numeric_features = [
    'GrLivArea', 'Total_Living_Area', 'Total_Bathrooms', 'BedroomAbvGr', 
    'Property_Age', 'GarageCars', 'OverallQual', 'OverallCond',
    'Has_Pool', 'Has_Garage', 'Is_Remodeled'
]
categorical_features = ['Neighborhood']

target = 'SalePrice'

X = df[numeric_features + categorical_features].copy()
y = df[target].copy()
y_log = np.log1p(y)

# 80/20 train/test split
X_train, X_test, y_train_log, y_test_log = train_test_split(
    X, y_log, test_size=0.2, random_state=42
)
y_test_original = np.expm1(y_test_log)

# Create preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ]
)

# Fit preprocessor on training data
X_train_trans = preprocessor.fit_transform(X_train)
X_test_trans = preprocessor.transform(X_test)

# Assert no nulls after preprocessing
assert not np.isnan(X_train_trans).any(), "X_train contains missing values!"
assert not np.isnan(X_test_trans).any(), "X_test contains missing values!"
print("Verification Assertion Passed: 0 missing values after preprocessing pipeline.")

# Save preprocessor pipeline
joblib.dump(preprocessor, os.path.join(MODEL_DIR, "preprocessor_pipeline.pkl"))

# Define Models
models = {
    "Ridge Regression": Ridge(alpha=10.0),
    "Decision Tree": DecisionTreeRegressor(max_depth=6, min_samples_split=10, random_state=42),
    "Random Forest": RandomForestRegressor(n_estimators=150, max_depth=12, min_samples_split=4, random_state=42),
    "XGBoost": XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=4, subsample=0.8, colsample_bytree=0.8, random_state=42)
}

results = {}
trained_models = {}
n_test = len(y_test_original)
p_features = X_test_trans.shape[1]

for name, model in models.items():
    # 5-Fold Cross Validation on train split (log scale)
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train_trans, y_train_log, cv=cv, scoring='r2')
    
    # Train
    model.fit(X_train_trans, y_train_log)
    trained_models[name] = model
    
    # Predict on test
    pred_log = model.predict(X_test_trans)
    pred_original = np.expm1(pred_log)
    
    mae = mean_absolute_error(y_test_original, pred_original)
    mse = mean_squared_error(y_test_original, pred_original)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test_original, pred_original)
    adj_r2 = 1 - ((1 - r2) * (n_test - 1) / (n_test - p_features - 1))
    
    results[name] = {
        "MAE": round(float(mae), 2),
        "MSE": round(float(mse), 2),
        "RMSE": round(float(rmse), 2),
        "R2_Score": round(float(r2), 4),
        "Adjusted_R2": round(float(adj_r2), 4),
        "CV_R2_Mean": round(float(cv_scores.mean()), 4),
        "CV_R2_Std": round(float(cv_scores.std()), 4)
    }

# Print metrics comparison table
metrics_df = pd.DataFrame(results).T
print("\n=== Model Evaluation Comparison Table (Original Price Scale $) ===")
print(metrics_df)

# Identify Best Model by R2_Score
best_model_name = metrics_df['R2_Score'].idxmax()
best_model = trained_models[best_model_name]
print(f"\nBest Performing Model: {best_model_name} (R2: {results[best_model_name]['R2_Score']})")

# Save Best Model
joblib.dump(best_model, os.path.join(MODEL_DIR, "best_house_price_model.pkl"))

# Save Model Metadata
metadata = {
    "dataset": "Ames Housing (Kaggle / OpenML benchmark)",
    "records": len(df),
    "features_used": numeric_features + categorical_features,
    "best_model": best_model_name,
    "model_metrics": results
}
with open(os.path.join(MODEL_DIR, "model_metadata.json"), "w") as f:
    json.dump(metadata, f, indent=4)
print(f"Saved model metadata to {os.path.join(MODEL_DIR, 'model_metadata.json')}")

# Diagnostic Plots for Best Model
best_pred_original = np.expm1(best_model.predict(X_test_trans))
residuals = y_test_original - best_pred_original

# Plot 6: Actual vs Predicted
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(y_test_original, best_pred_original, alpha=0.6, color='#1d3557', edgecolors='k')
min_val = min(y_test_original.min(), best_pred_original.min())
max_val = max(y_test_original.max(), best_pred_original.max())
ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label="Ideal 45° Fit")
ax.set_title(f"Actual vs Predicted Prices ({best_model_name})", fontsize=14, fontweight='bold')
ax.set_xlabel("Actual Sale Price ($)")
ax.set_ylabel("Predicted Sale Price ($)")
ax.legend()
plt.tight_layout()
p6 = os.path.join(IMAGES_DIR, "actual_vs_predicted.png")
fig.savefig(p6, dpi=300)
plt.close(fig)
print(f"Saved: {p6}")

# Plot 7: Residual Plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(best_pred_original, residuals, alpha=0.6, color='#e63946', edgecolors='k')
ax.axhline(0, color='black', linestyle='--', lw=2)
ax.set_title(f"Residuals vs Predicted Values ({best_model_name})", fontsize=14, fontweight='bold')
ax.set_xlabel("Predicted Sale Price ($)")
ax.set_ylabel("Residuals ($) [Actual - Predicted]")
plt.tight_layout()
p7 = os.path.join(IMAGES_DIR, "residuals_plot.png")
fig.savefig(p7, dpi=300)
plt.close(fig)
print(f"Saved: {p7}")

# Feature Importances for Tree Models
if hasattr(best_model, "feature_importances_"):
    # Extract feature names
    cat_cols = preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_features)
    all_feature_names = numeric_features + list(cat_cols)
    importances = best_model.feature_importances_
    feat_imp = pd.Series(importances, index=all_feature_names).sort_values(ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=feat_imp.values, y=feat_imp.index, palette='mako', ax=ax)
    ax.set_title(f"Top 10 Feature Importances ({best_model_name})", fontsize=14, fontweight='bold')
    ax.set_xlabel("Relative Importance")
    plt.tight_layout()
    p8 = os.path.join(IMAGES_DIR, "feature_importance.png")
    fig.savefig(p8, dpi=300)
    plt.close(fig)
    print(f"Saved: {p8}")
    print("\nTop 5 Most Important Features:")
    for rank, (feat, score) in enumerate(feat_imp.head(5).items(), 1):
        print(f" {rank}. {feat}: {score:.4f}")
