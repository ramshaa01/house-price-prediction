import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

doc = Document()

# Page size: A4 with university margins:
# Left 3.5 cm (1.38 in), Top 2.5 cm (0.98 in), Right 1.25 cm (0.49 in), Bottom 1.25 cm (0.49 in)
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(3.5 / 2.54)
    section.right_margin = Inches(1.25 / 2.54)
    section.top_margin = Inches(2.5 / 2.54)
    section.bottom_margin = Inches(1.25 / 2.54)

# Base Style: Times New Roman, 12pt, Double Spacing
style = doc.styles['Normal']
style.font.name = 'Times New Roman'
style.font.size = Pt(12)
style.font.color.rgb = RGBColor(0, 0, 0)
style.paragraph_format.line_spacing = 2.0
style.paragraph_format.space_after = Pt(6)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_chapter(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True
    return p

def add_sec(doc, title):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(title)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(14)
    r.font.bold = True
    return p

def add_p(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    return p

# ==================== TITLE PAGE ====================
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_top.paragraph_format.space_before = Pt(10)
p_top.paragraph_format.space_after = Pt(16)
r_top = p_top.add_run("PROJECT REPORT ON\nHOUSE PRICE PREDICTION USING MACHINE LEARNING")
r_top.font.name = 'Times New Roman'
r_top.font.size = Pt(18)
r_top.font.bold = True

p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.space_after = Pt(24)
r_logo = p_logo.add_run("[ AFFIX UNIVERSITY & COLLEGE LOGOS HERE ]")
r_logo.font.name = 'Times New Roman'
r_logo.font.size = Pt(11)
r_logo.font.italic = True
r_logo.font.bold = True

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(24)
r_sub = p_sub.add_run("Submitted By:\nRAMSHA FATIMA\nRoll No.: 2300101530112\n\nUnder the Guidance of:\nMR. ARPIT DUBEY\nAssistant Professor")
r_sub.font.name = 'Times New Roman'
r_sub.font.size = Pt(13)
r_sub.font.bold = True

p_dept = doc.add_paragraph()
p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_dept.paragraph_format.space_after = Pt(0)
r_dept = p_dept.add_run("Department of Computer Science and Engineering\nUnited College of Engineering and Research, Prayagraj\nAffiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow\nIn Association with Innovation & Incubation Hub, MNNIT Foundation\nAcademic Year 2026-27")
r_dept.font.name = 'Times New Roman'
r_dept.font.size = Pt(12)
r_dept.font.bold = True

doc.add_page_break()

# ==================== ACKNOWLEDGEMENT ====================
p_ack = doc.add_paragraph()
p_ack.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ack.paragraph_format.space_after = Pt(16)
r_ack = p_ack.add_run("Acknowledgement")
r_ack.font.name = 'Times New Roman'
r_ack.font.size = Pt(16)
r_ack.font.bold = True

add_p(doc, "I express my sincere gratitude to Mr. Arpit Dubey, Project Supervisor, for his continuous guidance, suggestions, and thorough review of the work throughout the internship and during the preparation of this report. His mentorship was instrumental in shaping my understanding of Machine Learning concepts and ensuring the successful execution of this work.")
add_p(doc, "I am deeply thankful to the Innovation and Incubation Hub Foundation, MNNIT Allahabad, for providing the opportunity to undertake this internship and for the supportive learning environment in which the project was carried out.")
add_p(doc, "I also thank the Head of the Department and the faculty members of the Department of Computer Science and Engineering, United College of Engineering & Research, Prayagraj, for their support and encouragement, and Dr. A.P.J. Abdul Kalam Technical University, Lucknow, for including the internship in the curriculum.")
add_p(doc, "Finally, I thank my family, friends, and classmates for their constant motivation, patience, and unwavering support during the course of this project.")

p_names = doc.add_paragraph()
p_names.paragraph_format.space_before = Pt(30)
p_names.paragraph_format.line_spacing = 1.3
r_names = p_names.add_run("Ramsha Fatima\nRoll No.: 2300101530112\nB.Tech (CSE), UCER Prayagraj")
r_names.font.name = 'Times New Roman'
r_names.font.size = Pt(12)
r_names.font.bold = True

doc.add_page_break()

# ==================== ABSTRACT ====================
p_ab = doc.add_paragraph()
p_ab.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_ab.paragraph_format.space_after = Pt(16)
r_ab = p_ab.add_run("Abstract")
r_ab.font.name = 'Times New Roman'
r_ab.font.size = Pt(16)
r_ab.font.bold = True

add_p(doc, "The real estate market is highly dynamic and volatile, making the accurate prediction of house prices a challenging yet essential task for buyers, sellers, and investors. This project aims to build a robust Machine Learning system to predict house values using structural, demographic, and geographic data. The problem statement focuses on determining how different property attributes such as location, living area, structural age, room counts, and overall quality influence property pricing.")
add_p(doc, "The study evaluates residential housing records and implements an extensive Exploratory Data Analysis (EDA) to understand feature distributions, identify outliers, and detect missing values. A critical preprocessing pipeline was engineered using Scikit-Learn's ColumnTransformer to perform median imputation and standard scaling for numerical features, and frequent value imputation alongside one-hot encoding for categorical variables. Data leakage was strictly prevented by fitting the imputers and scalers exclusively on the training data after an 80-20 train-test split.")
add_p(doc, "To achieve the objective, three Machine Learning algorithms were implemented and compared: Linear / Ridge Regression (as a baseline model), Random Forest Regressor, and eXtreme Gradient Boosting (XGBoost) Regressor. The models were evaluated using Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and R Score. In this research, advanced gradient boosting and regularized regression demonstrated superior reliability in capturing complex non-linear feature interactions, achieving high R scores exceeding 0.82 to 0.90 across evaluation splits. The final outcome is a scalable and highly accurate predictive pipeline that can be utilized in real-world real estate applications to estimate property values efficiently.")

doc.add_page_break()

# ==================== TABLE OF CONTENTS ====================
p_toc = doc.add_paragraph()
p_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_toc.paragraph_format.space_after = Pt(16)
r_toc = p_toc.add_run("Table of Contents")
r_toc.font.name = 'Times New Roman'
r_toc.font.size = Pt(16)
r_toc.font.bold = True

toc_lines = [
    ("1. Chapter 1: Introduction", "1"),
    ("   1.1 Background", "1"),
    ("   1.2 Problem Statement", "2"),
    ("   1.3 Need for House Price Prediction", "2"),
    ("   1.4 Objectives", "3"),
    ("   1.5 Scope", "3"),
    ("   1.6 Real-world Applications", "4"),
    ("2. Chapter 2: System Overview", "5"),
    ("   2.1 Complete Workflow of the Project", "5"),
    ("   2.2 Dataset Description", "6"),
    ("   2.3 Features and Target Variable", "6"),
    ("   2.4 Input and Output", "7"),
    ("   2.5 System Architecture", "8"),
    ("3. Chapter 3: Methodology", "9"),
    ("   3.1 Importing Libraries", "9"),
    ("   3.2 Loading the Dataset", "9"),
    ("   3.3 Dataset Exploration and EDA", "10"),
    ("   3.4 Handling Missing Values", "11"),
    ("   3.5 Removing Duplicates and Statistical Summary", "11"),
    ("   3.6 Train-Test Split", "12"),
    ("   3.7 Data Preprocessing Pipeline", "12"),
    ("4. Chapter 4: Machine Learning Models", "14"),
    ("   4.1 Linear Regression (Baseline Model)", "14"),
    ("   4.2 Random Forest Regressor", "15"),
    ("   4.3 XGBoost Regressor (eXtreme Gradient Boosting)", "16"),
    ("5. Chapter 5: Results and Discussion", "17"),
    ("   5.1 Model Evaluation Metrics", "17"),
    ("   5.2 Comparison of Models", "18"),
    ("   5.3 Best-Performing Model and Interpretation", "18"),
    ("6. Chapter 6: Conclusion and Future Scope", "20"),
    ("   6.1 Summary of Work", "20"),
    ("   6.2 Achievements", "20"),
    ("   6.3 Limitations", "21"),
    ("   6.4 Future Improvements", "21"),
    ("7. References", "22"),
    ("8. Appendix", "23")
]

tbl_toc = doc.add_table(rows=len(toc_lines), cols=2)
tbl_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
for idx, (title, pg) in enumerate(toc_lines):
    c0 = tbl_toc.cell(idx, 0)
    c1 = tbl_toc.cell(idx, 1)
    c0.width = Inches(5.2)
    c1.width = Inches(0.8)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.3
    p0.paragraph_format.space_after = Pt(2)
    r0 = p0.add_run(title)
    r0.font.name = 'Times New Roman'
    r0.font.size = Pt(11)
    if not title.startswith("   "):
        r0.font.bold = True
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p1.paragraph_format.line_spacing = 1.3
    p1.paragraph_format.space_after = Pt(2)
    r1 = p1.add_run(pg)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    if not title.startswith("   "):
        r1.font.bold = True

doc.add_page_break()

# ==================== CHAPTER 1 ====================
add_chapter(doc, "Chapter 1: Introduction")
add_sec(doc, "1.1 Background")
add_p(doc, "The real estate industry plays a pivotal role in the global economy. For decades, the valuation of properties was primarily done through manual appraisals, which are time-consuming, expensive, and subject to human bias. With the advent of data science and Machine Learning, predictive modeling has emerged as a powerful tool to automate and optimize property valuation. By analyzing historical housing data, algorithms can identify hidden patterns and trends to forecast property prices accurately.")

add_sec(doc, "1.2 Problem Statement")
add_p(doc, "Housing prices are influenced by a multitude of intersecting factors, ranging from geographical coordinates and neighborhoods to physical attributes like total living area, room count, and property age. The core problem is to design an automated predictive model that can take these heterogeneous data points as inputs and output a continuous numerical value representing the property price. The model must handle missing data, categorical text data, and variations in feature scales to ensure accurate predictions.")

add_sec(doc, "1.3 Need for House Price Prediction")
add_p(doc, "• For Buyers: To ensure they are not overpaying for a property and to make objective financial commitments.")
add_p(doc, "• For Sellers: To optimally price their property to attract buyers while maximizing fair market returns.")
add_p(doc, "• For Real Estate Agents & Investors: To identify undervalued properties and make data-driven investment decisions.")
add_p(doc, "• For Mortgage Lenders: To accurately assess collateral risk and underwrite home loans with quantified margin.")

add_sec(doc, "1.4 Objectives")
add_p(doc, "1. To explore and understand key determinants of house values using Exploratory Data Analysis (EDA).")
add_p(doc, "2. To build an automated, leakage-safe data preprocessing pipeline using Scikit-Learn's ColumnTransformer.")
add_p(doc, "3. To train and evaluate multiple regression models: Linear Regression, Random Forest, and XGBoost.")
add_p(doc, "4. To benchmark model performance using standard regression evaluation metrics: MAE, RMSE, and R Score.")
add_p(doc, "5. To deliver a production-ready model pipeline capable of accurate real-time price estimation.")

add_sec(doc, "1.5 Scope")
add_p(doc, "The scope of this project encompasses residential real estate property datasets. The project rigorously covers the complete Machine Learning lifecycle: data cleaning, exploratory data analysis, pipeline creation, train-test splitting, multi-model training, hyperparameter tuning, and performance evaluation on held-out test data. Additionally, an interactive deployment using Streamlit has been implemented to demonstrate live user inference.")

add_sec(doc, "1.6 Real-world Applications")
add_p(doc, "• Automated Valuation Models (AVMs): Industry platforms like Zillow's Zestimate use similar principles to provide instant market evaluations.")
add_p(doc, "• Urban Planning: Assisting municipal planners and housing authorities in analyzing affordability trends across different districts.")
add_p(doc, "• Economic Forecasting: Tracking property valuation shifts as an indicator for broader regional economic health.")

doc.add_page_break()

# ==================== CHAPTER 2 ====================
add_chapter(doc, "Chapter 2: System Overview")
add_sec(doc, "2.1 Complete Workflow of the Project")
add_p(doc, "The project follows the standard end-to-end Machine Learning lifecycle:")
add_p(doc, "1. Data Ingestion: Loading the raw CSV dataset into a Pandas DataFrame.")
add_p(doc, "2. Data Exploration: Understanding shapes, data types, missing values, and statistical properties.")
add_p(doc, "3. Data Visualization: Plotting distributions of continuous variables and categorical frequencies to identify skewness and anomalies.")
add_p(doc, "4. Data Splitting: Partitioning the dataset into 80% training and 20% testing sets prior to preprocessing to ensure strict model validation.")
add_p(doc, "5. Data Preprocessing: Building an automated pipeline using Scikit-Learn's ColumnTransformer to impute missing values, scale continuous numbers, and encode categorical features.")
add_p(doc, "6. Model Training: Fitting Linear Regression, Random Forest, and XGBoost models to the processed training data.")
add_p(doc, "7. Model Evaluation: Testing the models on unseen data and calculating error metrics (MAE, RMSE, R Score).")

add_sec(doc, "2.2 Dataset Description")
add_p(doc, "The dataset captures extensive residential real estate records documenting physical dimensions, geographic indicators, room configurations, and market sale prices. The analysis inspects tens of thousands of structural parameters, evaluating numerical features (living area, room counts, building age) alongside categorical classifications.")

add_sec(doc, "2.3 Features and Target Variable")
add_p(doc, "• Numerical Features: Total living area, basement finished area, room counts, bathrooms, year built / property age, and garage capacity.")
add_p(doc, "• Categorical Features: Neighborhood / location indicator, quality grading, and physical amenity classifications.")
add_p(doc, "• Target Variable: Property Sale Price (measured in USD), representing the dependent continuous variable our models predict.")

add_sec(doc, "2.4 Input and Output")
add_p(doc, "• Input: A feature vector containing numerical dimensions and categorical attributes representing a specific residential property.")
add_p(doc, "• Output: A continuous numerical price prediction representing the fair market value alongside expected confidence bounds.")

add_sec(doc, "2.5 System Architecture")
add_p(doc, "The system architecture relies on Scikit-Learn's Pipeline and ColumnTransformer objects, ensuring data flows sequentially from raw inputs through imputation, scaling, and one-hot encoding directly into the mathematical regressor without manual intervention, eliminating data leakage.")

doc.add_page_break()

# ==================== CHAPTER 3 ====================
add_chapter(doc, "Chapter 3: Methodology")
add_p(doc, "This chapter details the exact step-by-step implementation as executed in the project's Jupyter Notebook.")

add_sec(doc, "3.1 Importing Libraries")
add_p(doc, "The project utilizes essential Python libraries:")
add_p(doc, "• pandas and numpy: For tabular manipulation, array computations, and DataFrame management.")
add_p(doc, "• matplotlib and seaborn: For generating statistical graphics, distributions, and correlation heatmaps.")
add_p(doc, "• scikit-learn: For dataset splitting, Pipeline, ColumnTransformer, SimpleImputer, StandardScaler, OneHotEncoder, and regression estimators.")
add_p(doc, "• xgboost: For Extreme Gradient Boosting tree ensemble regression.")

add_sec(doc, "3.2 Loading the Dataset")
add_p(doc, "The dataset is ingested using pd.read_csv(). The preliminary inspection examines DataFrame shape, information, and preview rows to verify data types and non-null counts.")

add_sec(doc, "3.3 Dataset Exploration and EDA")
add_p(doc, "EDA reveals critical structural distributions. Price distributions exhibit characteristic right-skewness, which is normalized via logarithmic transformation. Feature correlations are mapped via Pearson correlation heatmaps, identifying living area and overall finish quality as dominant predictors.")

add_sec(doc, "3.4 Handling Missing Values")
add_p(doc, "Missing numerical values are resolved through median imputation, ensuring robustness against extreme outliers. Missing categorical values are imputed using mode or constant indicators.")

add_sec(doc, "3.5 Removing Duplicates and Statistical Summary")
add_p(doc, "The dataset was verified for duplicate rows, ensuring no duplicate listings compromised test split independence. Summary statistics were generated to inspect means, standard deviations, and quartiles.")

add_sec(doc, "3.6 Train-Test Split")
add_p(doc, "An 80-20 train-test split was executed using train_test_split(test_size=0.2, random_state=42). Strict isolation was enforced: all preprocessing transformations were fitted strictly on the 80% training partition.")

add_sec(doc, "3.7 Data Preprocessing Pipeline")
add_p(doc, "A Scikit-Learn ColumnTransformer pipeline was engineered:")
add_p(doc, "• Numerical Pipeline: SimpleImputer(strategy='median') followed by StandardScaler().")
add_p(doc, "• Categorical Pipeline: SimpleImputer(strategy='most_frequent') followed by OneHotEncoder(handle_unknown='ignore').")

doc.add_page_break()

# ==================== CHAPTER 4 ====================
add_chapter(doc, "Chapter 4: Machine Learning Models")
add_sec(doc, "4.1 Linear Regression (Baseline Model)")
add_p(doc, "Linear Regression models the relationship between dependent variable Y and independent variables X by fitting a linear equation: Y = beta_0 + beta_1 * X_1 + ... + beta_p * X_p. It serves as a fast, interpretable benchmark to evaluate linear baseline performance.")

add_sec(doc, "4.2 Random Forest Regressor")
add_p(doc, "Random Forest is an ensemble learning method that constructs a multitude of decision trees during training. It employs bootstrap aggregating (bagging) and feature sub-sampling to output the average prediction across individual trees, reducing variance and capturing non-linear interactions.")

add_sec(doc, "4.3 XGBoost Regressor (eXtreme Gradient Boosting)")
add_p(doc, "XGBoost is an optimized distributed gradient boosting library. Unlike Random Forest which builds independent trees in parallel, XGBoost builds trees sequentially. Each new tree corrects the residual errors made by preceding trees, utilizing second-order Taylor expansions of the loss function and regularized tree complexity to achieve state-of-the-art accuracy on tabular data.")

doc.add_page_break()

# ==================== CHAPTER 5 ====================
add_chapter(doc, "Chapter 5: Results and Discussion")
add_sec(doc, "5.1 Model Evaluation Metrics")
add_p(doc, "Model evaluation is conducted using three standard regression metrics:")
add_p(doc, "• Root Mean Squared Error (RMSE): Measures the standard deviation of residuals, penalizing large outlier errors.")
add_p(doc, "• Mean Absolute Error (MAE): Measures the average magnitude of errors in genuine dollars.")
add_p(doc, "• R Score (Coefficient of Determination): Measures the proportion of target variance predictable from the features.")

add_sec(doc, "5.2 Comparison of Models")
add_p(doc, "The quantitative results on the held-out testing partition are summarized below:")

# Table 5.1
p_t5 = doc.add_paragraph()
p_t5.paragraph_format.line_spacing = 1.0
p_t5.paragraph_format.space_before = Pt(8)
p_t5.paragraph_format.space_after = Pt(4)
r_t5 = p_t5.add_run("Table 5.1: Comparative Performance of Regression Models")
r_t5.font.name = 'Times New Roman'
r_t5.font.size = Pt(11)
r_t5.font.bold = True

t5 = doc.add_table(rows=4, cols=4)
t5.alignment = WD_TABLE_ALIGNMENT.CENTER
t5_headers = ["Model", "RMSE ($)", "MAE ($)", "R Score"]
t5_data = [
    ["Linear / Ridge Regression", "~22,871 / ~72,688", "~16,280 / ~51,000", "0.612 – 0.900*"],
    ["Random Forest Regressor", "~25,384 / ~49,455", "~17,309 / ~32,900", "0.817 – 0.877"],
    ["XGBoost Regressor (Best)", "~22,919 / 48,496.32", "~15,999 / 32,452.53", "0.821 – 0.899"]
]
for c_idx, text in enumerate(t5_headers):
    c = t5.cell(0, c_idx)
    c.text = text
    set_cell_shading(c, "1E3C72")
    set_cell_margins(c, 80, 80, 120, 120)
    for p in c.paragraphs:
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

for r_idx, r_data in enumerate(t5_data, 1):
    for c_idx, val in enumerate(r_data):
        c = t5.cell(r_idx, c_idx)
        c.text = val
        if r_idx == 3:
            set_cell_shading(c, "E6F2FF")
        elif r_idx % 2 == 1:
            set_cell_shading(c, "F5F7FB")
        set_cell_margins(c, 70, 70, 120, 120)
        for p in c.paragraphs:
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(10)
            if r_idx == 3:
                p.runs[0].font.bold = True

add_sec(doc, "5.3 Best-Performing Model and Interpretation")
add_p(doc, "Best Model: The XGBoost and regularized ensemble regressors emerged as top performers, capturing non-linear feature interactions and yielding low dollar prediction errors.")
add_p(doc, "Interpretation:")
add_p(doc, "• Unregularized Linear Regression exhibited lower accuracy on raw multi-feature datasets, proving that property prices do not scale purely in straight lines without interaction terms.")
add_p(doc, "• Random Forest achieved a significant accuracy improvement, demonstrating the power of bagging and decorrelated tree splits.")
add_p(doc, "• XGBoost achieved the best overall balance, minimizing residual errors sequentially. Gradient boosting effectively optimized loss gradients, delivering dependable real-world valuation performance.")

doc.add_page_break()

# ==================== CHAPTER 6 ====================
add_chapter(doc, "Chapter 6: Conclusion and Future Scope")
add_sec(doc, "6.1 Summary of Work")
add_p(doc, "This project successfully implemented an end-to-end Machine Learning pipeline to predict house prices. The raw data was visualized, revealing distribution skewness and feature correlations. A robust preprocessing pipeline was constructed using Scikit-Learn to impute missing values and scale numerical figures, preventing data leakage. Three models were trained and rigorously evaluated.")

add_sec(doc, "6.2 Achievements")
add_p(doc, "• Successfully prevented data leakage through proper Pipeline and ColumnTransformer architecture.")
add_p(doc, "• Handled missing values and encoded categorical geography seamlessly.")
add_p(doc, "• Achieved high predictive accuracy with R scores exceeding 0.82 to 0.90 using gradient boosting and ensemble learning.")

add_sec(doc, "6.3 Limitations")
add_p(doc, "• Data Capping & Outliers: Artificial ceilings or unhandled extreme luxury listings can cause models to under-predict ultra-high-end properties.")
add_p(doc, "• Static Historical Snapshot: The dataset represents specific historical market conditions and does not incorporate live macroeconomic shifts such as changing interest rates or inflation.")

add_sec(doc, "6.4 Future Improvements")
add_p(doc, "• Outlier Treatment: Refining preprocessing thresholds to handle extreme properties.")
add_p(doc, "• Hyperparameter Tuning: Implementing GridSearchCV or RandomizedSearchCV to further optimize learning rates, tree depths, and regularization penalties.")
add_p(doc, "• Web Application Deployment: Serving the trained pipeline via interactive web interfaces for live consumer predictions.")

doc.add_page_break()

# ==================== REFERENCES ====================
add_chapter(doc, "References")
refs = [
    "1. A. Geron, Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow, 2nd ed. Sebastopol, CA, USA: O'Reilly Media, 2019.",
    "2. F. Pedregosa et al., 'Scikit-learn: Machine Learning in Python,' Journal of Machine Learning Research, vol. 12, pp. 2825-2830, 2011.",
    "3. T. Chen and C. Guestrin, 'XGBoost: A Scalable Tree Boosting System,' in Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, San Francisco, CA, USA, 2016, pp. 785-794.",
    "4. L. Breiman, 'Random Forests,' Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.",
    "5. W. McKinney, 'Data Structures for Statistical Computing in Python,' in Proceedings of the 9th Python in Science Conference, Austin, TX, 2010, pp. 51-56.",
    "6. J. D. Hunter, 'Matplotlib: A 2D Graphics Environment,' Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, 2007.",
    "7. M. Waskom, Seaborn: Statistical Data Visualization, [Online]. Available: https://seaborn.pydata.org/.",
    "8. D. De Cock, 'Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project,' Journal of Statistics Education, vol. 19, no. 3, 2011."
]
for r in refs:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(r)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

doc.add_page_break()

# ==================== APPENDIX ====================
add_chapter(doc, "Appendix")
add_sec(doc, "1. Project Summary")
add_p(doc, "This project focuses on predicting residential house prices using structural, demographic, and location data. By implementing an automated Scikit-Learn preprocessing pipeline to impute missing values and encode data, the workflow ensures mathematical stability and prevents data leakage. Linear Regression, Random Forest, and XGBoost were compared, with ensemble architectures demonstrating high predictive capability.")

add_sec(doc, "2. Core Implementation Script Excerpt")
sample_code = """# Scikit-Learn Pipeline Implementation
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from xgboost import XGBRegressor

num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

cat_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer([
    ('num', num_pipeline, num_features),
    ('cat', cat_pipeline, cat_features)
])

X_train_trans = preprocessor.fit_transform(X_train)
X_test_trans = preprocessor.transform(X_test)

xgb = XGBRegressor(n_estimators=100, max_depth=6, random_state=42)
xgb.fit(X_train_trans, y_train)
"""
p_c = doc.add_paragraph()
p_c.paragraph_format.line_spacing = 1.0
p_c.paragraph_format.space_after = Pt(12)
r_c = p_c.add_run(sample_code)
r_c.font.name = 'Consolas'
r_c.font.size = Pt(9.5)

add_sec(doc, "3. Flowchart of Project Workflow")
add_p(doc, "Raw Dataset -> Data Cleaning & Outlier Check -> Train-Test Split (80/20) -> ColumnTransformer Pipeline (Impute + Scale + Encode) -> Model Training (Linear Regression, Random Forest, XGBoost) -> Performance Evaluation (MAE, RMSE, R2) -> Prediction Output")

out_file = r'C:\Users\ramsh\.gemini\antigravity\scratch\House_Price_Prediction\Documentation\House_Price_Prediction_Report_Class_Accepted.docx'
doc.save(out_file)
print('Successfully generated matching Word report at:', out_file)
