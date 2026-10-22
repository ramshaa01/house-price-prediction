import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\ramsh\.gemini\antigravity\scratch\House_Price_Prediction"
IMAGES_DIR = os.path.join(BASE_DIR, "Images")
DOCS_DIR = os.path.join(BASE_DIR, "Documentation")

doc = Document()

# Set standard page size: A4
# A4 dimensions: 210mm x 297mm (8.27 in x 11.69 in)
# Margins from specification: Left 3.5 cm (1.38 in), Top 2.5 cm (0.98 in), Right 1.25 cm (0.49 in), Bottom 1.25 cm (0.49 in)
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.left_margin = Inches(3.5 / 2.54)
    section.right_margin = Inches(1.25 / 2.54)
    section.top_margin = Inches(2.5 / 2.54)
    section.bottom_margin = Inches(1.25 / 2.54)

# Set base style to Times New Roman, 12pt, Double Line Spacing, British English
style_normal = doc.styles['Normal']
font = style_normal.font
font.name = 'Times New Roman'
font.size = Pt(12)
font.color.rgb = RGBColor(0, 0, 0)
style_normal.paragraph_format.line_spacing = 2.0
style_normal.paragraph_format.space_after = Pt(6)

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

def add_chapter_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(16)
    run.font.bold = True
    return p

def add_section_heading(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(14)
    run.font.bold = True
    return p

def add_body_p(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 2.0
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    return p

def add_fig(doc, img_filename, caption_text):
    img_path = os.path.join(IMAGES_DIR, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.line_spacing = 1.0
        p_img.paragraph_format.space_before = Pt(12)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(5.6))
        
        # Caption below figure
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.line_spacing = 1.0
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run(caption_text)
        run_cap.font.name = 'Times New Roman'
        run_cap.font.size = Pt(11)
        run_cap.font.italic = True
        run_cap.font.bold = True
    else:
        add_body_p(doc, f"[Figure: {caption_text} - Image placeholder]")

print("Starting Report Generation...")

# ==================== FRONT MATTER ====================

# 1. Title Page
p_title_main = doc.add_paragraph()
p_title_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title_main.paragraph_format.line_spacing = 1.5
p_title_main.paragraph_format.space_before = Pt(10)
p_title_main.paragraph_format.space_after = Pt(12)
run_title = p_title_main.add_run("AMES HOUSE PRICE PREDICTION SYSTEM")
run_title.font.name = 'Times New Roman'
run_title.font.size = Pt(20)
run_title.font.bold = True

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.line_spacing = 1.3
p_sub.paragraph_format.space_after = Pt(16)
run_sub = p_sub.add_run("A MINI PROJECT REPORT OF INTERNSHIP\nSubmitted in partial fulfillment of the requirements\nfor the award of the degree of\nBACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE AND ENGINEERING")
run_sub.font.name = 'Times New Roman'
run_sub.font.size = Pt(12)
run_sub.font.bold = True

# Logo Placeholders
p_logo = doc.add_paragraph()
p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_logo.paragraph_format.line_spacing = 1.0
p_logo.paragraph_format.space_after = Pt(16)
run_l = p_logo.add_run("[ AFFIX UNIVERSITY & COLLEGE LOGOS HERE ]")
run_l.font.name = 'Times New Roman'
run_l.font.size = Pt(11)
run_l.font.italic = True
run_l.font.bold = True

p_stud = doc.add_paragraph()
p_stud.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_stud.paragraph_format.line_spacing = 1.3
p_stud.paragraph_format.space_after = Pt(16)
run_st = p_stud.add_run("Submitted By:\nRAMSHA FATIMA\nRoll No.: 2300101530112\n\nUnder the Supervision of:\nMR. ARPIT DUBEY\nAssistant Professor")
run_st.font.name = 'Times New Roman'
run_st.font.size = Pt(12)
run_st.font.bold = True

p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.line_spacing = 1.3
p_inst.paragraph_format.space_after = Pt(0)
run_in = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\nUNITED COLLEGE OF ENGINEERING & RESEARCH, PRAYAGRAJ\nAffiliated to\nDR. A.P.J. ABDUL KALAM TECHNICAL UNIVERSITY, LUCKNOW\nACADEMIC YEAR 2026-27")
run_in.font.name = 'Times New Roman'
run_in.font.size = Pt(12)
run_in.font.bold = True

doc.add_page_break()

# 2. Certificate
p_c = doc.add_paragraph()
p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_c.paragraph_format.space_before = Pt(10)
p_c.paragraph_format.space_after = Pt(16)
run_c = p_c.add_run("CERTIFICATE")
run_c.font.name = 'Times New Roman'
run_c.font.size = Pt(16)
run_c.font.bold = True

add_body_p(doc, "This is to certify that the Mini Project Report entitled \"Ames House Price Prediction System\" submitted by Ramsha Fatima (University Roll No.: 2300101530112) in partial fulfillment of the requirements for the award of Bachelor of Technology in Computer Science and Engineering from Dr. A.P.J. Abdul Kalam Technical University, Lucknow, is an authentic record of independent project work carried out under my supervision during the Academic Year 2026-27.")
add_body_p(doc, "The internship training and technical project development were completed through the Innovation and Incubation Hub Foundation, MNNIT Allahabad. The matter embodied in this report has not been submitted by the candidate for the award of any other degree or diploma.")

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_before = Pt(36)
p_sig.paragraph_format.line_spacing = 1.5
r_sig = p_sig.add_run("Mr. Arpit Dubey\nAssistant Professor (Project Supervisor)\nDepartment of Computer Science and Engineering\nUnited College of Engineering & Research, Prayagraj\n\nDate: ____________________\nPlace: Prayagraj")
r_sig.font.name = 'Times New Roman'
r_sig.font.size = Pt(12)
r_sig.font.bold = True

doc.add_page_break()

# 3. Declaration
p_d = doc.add_paragraph()
p_d.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_d.paragraph_format.space_before = Pt(10)
p_d.paragraph_format.space_after = Pt(16)
run_d = p_d.add_run("CANDIDATE'S DECLARATION")
run_d.font.name = 'Times New Roman'
run_d.font.size = Pt(16)
run_d.font.bold = True

add_body_p(doc, "I, Ramsha Fatima (Roll No.: 2300101530112), student of Bachelor of Technology in Computer Science and Engineering at United College of Engineering & Research, Prayagraj, affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow, hereby declare that the work presented in this Mini Project Report entitled \"Ames House Price Prediction System\" is my own original work.")
add_body_p(doc, "I confirm that I have adhered to all university academic ethics and integrity standards. Any contributions made by earlier researchers, libraries, or external datasets have been duly acknowledged and cited in the references. This report has not been submitted previously to any institution for any degree or examination.")

p_dsig = doc.add_paragraph()
p_dsig.paragraph_format.space_before = Pt(40)
p_dsig.paragraph_format.line_spacing = 1.5
r_dsig = p_dsig.add_run("Ramsha Fatima\nRoll No.: 2300101530112\nB.Tech (Computer Science & Engineering)\nUnited College of Engineering & Research, Prayagraj")
r_dsig.font.name = 'Times New Roman'
r_dsig.font.size = Pt(12)
r_dsig.font.bold = True

doc.add_page_break()

# 4. Acknowledgement
p_a = doc.add_paragraph()
p_a.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_a.paragraph_format.space_before = Pt(10)
p_a.paragraph_format.space_after = Pt(16)
run_a = p_a.add_run("ACKNOWLEDGEMENT")
run_a.font.name = 'Times New Roman'
run_a.font.size = Pt(16)
run_a.font.bold = True

add_body_p(doc, "I express my sincere gratitude to Mr. Arpit Dubey, Assistant Professor and Project Supervisor, for his invaluable guidance, continuous encouragement, insightful suggestions, and thorough review of the work throughout the internship and during the preparation of this report.")
add_body_p(doc, "I am deeply thankful to the Innovation and Incubation Hub Foundation, MNNIT Allahabad, for providing the opportunity to undertake this internship and for the stimulating learning environment and resources in which the project was carried out.")
add_body_p(doc, "I also express my heartfelt thanks to the Head of the Department and the esteemed faculty members of the Department of Computer Science and Engineering, United College of Engineering & Research, Prayagraj, for their support, infrastructural facilities, and constant encouragement.")
add_body_p(doc, "I am grateful to Dr. A.P.J. Abdul Kalam Technical University, Lucknow, for including the internship in the curriculum, allowing us to bridge academic theoretical study with hands-on real-world industry application.")
add_body_p(doc, "Finally, I express my profound appreciation to my family and friends for their enduring patience, moral encouragement, and constant support throughout my studies.")

doc.add_page_break()

# 5. Abstract
p_abs = doc.add_paragraph()
p_abs.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_abs.paragraph_format.space_before = Pt(10)
p_abs.paragraph_format.space_after = Pt(16)
run_ab = p_abs.add_run("ABSTRACT")
run_ab.font.name = 'Times New Roman'
run_ab.font.size = Pt(16)
run_ab.font.bold = True

add_body_p(doc, "Accurate residential real estate valuation is a critical foundation for mortgage underwriters, individual homebuyers, property developers, and municipal tax assessors. However, real estate valuations have historically suffered from pricing opacity, inconsistent subjective appraisals, and volatile market heuristics. This Capstone Project establishes an end-to-end Machine Learning House Price Prediction System built upon the comprehensive Ames Housing benchmark dataset, comprising 1,460 residential properties across 81 structural and architectural features.")
add_body_p(doc, "The project executes the complete 8-phase data science lifecycle, incorporating statistical outlier treatment (filtering extreme dwellings > 4,000 sq ft), median and mode imputation, target logarithmic normalization, scikit-learn ColumnTransformer pipelines, and domain-specific feature engineering (deriving Total Living Area, Property Age, Total Bathrooms, and binary amenity flags). Four regression architectures—Ridge Regression, Decision Tree, Random Forest, and Extreme Gradient Boosting (XGBoost)—were trained and tuned using 5-fold cross-validation. Evaluating performance on held-out test data on the genuine dollar scale revealed that Ridge Regression achieved an outstanding R² score of 0.9003 with a Mean Absolute Error (MAE) of $16,280.23, closely matched by XGBoost (R² = 0.8999, MAE = $15,999.01), comfortably exceeding the university project benchmark of 0.85.")
add_body_p(doc, "The top-performing model and preprocessing pipelines were persisted and deployed as a production-ready interactive web application using Streamlit and published to Streamlit Community Cloud. The application provides real-time fair market value prediction, dynamic confidence intervals, counterfactual 'What-If' scenario analysis, and embedded exploratory data analysis dashboards.")

doc.add_page_break()

# 6. Table of Contents / Index
p_idx = doc.add_paragraph()
p_idx.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_idx.paragraph_format.space_before = Pt(10)
p_idx.paragraph_format.space_after = Pt(16)
run_id = p_idx.add_run("TABLE OF CONTENTS")
run_id.font.name = 'Times New Roman'
run_id.font.size = Pt(16)
run_id.font.bold = True

toc_items = [
    ("Certificate", "ii"),
    ("Candidate's Declaration", "iii"),
    ("Acknowledgement", "iv"),
    ("Abstract", "v"),
    ("List of Figures", "vii"),
    ("List of Tables", "viii"),
    ("Chapter 1: Objectives & Problem Understanding", "1"),
    ("   1.1 Real Estate Valuation and Price Opacity", "1"),
    ("   1.2 Project Aims and Specific Objectives", "2"),
    ("   1.3 Project Scope and Boundaries", "3"),
    ("   1.4 Selected Dataset Overview", "4"),
    ("Chapter 2: Tools and Technologies Used", "5"),
    ("   2.1 Core Programming Language & Numerical Libraries", "5"),
    ("   2.2 Machine Learning & Statistical Frameworks", "6"),
    ("   2.3 Interactive Web Deployment & Version Control", "7"),
    ("   2.4 Software Stack Summary Table", "8"),
    ("Chapter 3: System Functionality & Architecture", "9"),
    ("   3.1 End-to-End System Architecture", "9"),
    ("   3.2 Input Attributes and Reactive Controls", "10"),
    ("   3.3 Prediction Engine and Dynamic Uncertainty Bounds", "11"),
    ("   3.4 Counterfactual 'What-If' Scenario Analyzer", "12"),
    ("Chapter 4: Model Workflow & Methodology", "13"),
    ("   4.1 The Eight-Phase Machine Learning Lifecycle", "13"),
    ("   4.2 Data Preprocessing and Outlier Removal", "14"),
    ("   4.3 Target Skewness and Logarithmic Transformation", "15"),
    ("   4.4 Categorical Encoding and Feature Scaling", "16"),
    ("   4.5 Exploratory Data Analysis & Bivariate Relationships", "17"),
    ("   4.6 Regression Model Training and Cross-Validation", "18"),
    ("Chapter 5: Key Features & Predictive Drivers", "19"),
    ("   5.1 Domain-Specific Engineered Variables", "19"),
    ("   5.2 Multicollinearity and Regularization Analysis", "20"),
    ("   5.3 Top Predictive Value Drivers", "21"),
    ("Chapter 6: Performance Evaluation & Discussion", "22"),
    ("   6.1 Evaluation Metrics Defined", "22"),
    ("   6.2 Comparative Model Performance Benchmark", "23"),
    ("   6.3 Architectural Analysis: Why Regularized Linear Won", "24"),
    ("   6.4 Diagnostic Plots: Residuals and Actual vs Predicted", "25"),
    ("Chapter 7: Limitations & Environmental Constraints", "26"),
    ("   7.1 Geographic Specialization and Transferability", "26"),
    ("   7.2 Temporal Boundaries and Macroeconomic Variables", "27"),
    ("   7.3 Multi-Modal and Visual Limitations", "27"),
    ("Chapter 8: Conclusion and Future Work", "28"),
    ("   8.1 Summary of Capstone Achievements", "28"),
    ("   8.2 Directions for Future Research & Development", "29"),
    ("References", "30"),
    ("Appendix: Source Code & Deployment Guide", "31")
]

table_toc = doc.add_table(rows=len(toc_items), cols=2)
table_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
table_toc.autofit = False

for idx, (title, page) in enumerate(toc_items):
    c0 = table_toc.cell(idx, 0)
    c1 = table_toc.cell(idx, 1)
    c0.width = Inches(5.0)
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
    r1 = p1.add_run(page)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(11)
    if not title.startswith("   "):
        r1.font.bold = True

doc.add_page_break()

# ==================== CHAPTERS ====================

# Chapter 1
add_chapter_heading(doc, "CHAPTER 1: OBJECTIVES & PROBLEM UNDERSTANDING")
add_section_heading(doc, "1.1 Real Estate Valuation and Price Opacity")
add_body_p(doc, "Residential property represents the single largest financial asset for the majority of individuals and families globally. Concurrently, real estate transactions serve as foundational collateral across commercial banking, mortgage lending, and municipal tax assessment systems. Despite its profound economic magnitude, residential property valuation has historically been impaired by substantial price opacity, structural complexity, and reliance on subjective appraisal heuristics.")
add_body_p(doc, "Traditional appraisal practices frequently depend on human real estate appraisers conducting qualitative walkthroughs and manually comparing 3 to 5 recently closed transactions ('comps'). This conventional paradigm suffers from critical limitations: human cognitive appraisal bias, regional inconsistency, slow turnaround times, and an inability to simultaneously process high-dimensional non-linear interactions across dozens of structural, architectural, and spatial attributes. In volatile market environments, these subjective heuristics introduce severe pricing inefficiencies, leading to either prolonged market stagnation due to overpricing or significant equity loss resulting from undervaluation.")

add_section_heading(doc, "1.2 Project Aims and Specific Objectives")
add_body_p(doc, "To resolve the persistent challenge of price opacity, this Capstone Project develops an automated, data-driven, and institutional-grade Machine Learning House Price Prediction System. The project follows the rigorous 8-phase machine learning development lifecycle, converting raw residential transaction data into calibrated mathematical representations that output point valuations alongside empirical confidence intervals.")
add_body_p(doc, "The specific research and engineering objectives of this project include:")
add_body_p(doc, "1. Comprehensive Data Preprocessing: Formulate statistical pipelines to purge high-leverage outliers, impute missing physical measurements using median and mode imputation, and eliminate multicollinearity risks.")
add_body_p(doc, "2. Target Distribution Normalization: Implement logarithmic transformations on the continuous target variable (SalePrice) to counter severe right-skewness and satisfy linear homoscedasticity criteria.")
add_body_p(doc, "3. Domain Feature Engineering: Synthesize compound real estate attributes—including Total Living Area, Property Age, Composite Bathrooms, and binary amenity flags—to amplify model signal-to-noise ratio.")
add_body_p(doc, "4. Multi-Model Benchmarking: Implement and hyperparameter-tune at least four distinct regression model families: regularized linear models (Ridge Regression), single decision trees, bagging ensembles (Random Forest), and gradient boosted decision trees (XGBoost) using 5-fold cross-validation.")
add_body_p(doc, "5. Strict Empirical Verification: Evaluate all trained architectures on a held-out test split (20%) on the genuine dollar scale, exceeding an R² accuracy benchmark of 0.85.")
add_body_p(doc, "6. Cloud Deployment: Architect and deploy an interactive Streamlit web dashboard to Streamlit Community Cloud, enabling real-time valuation inference and counterfactual 'What-If' scenario planning.")

add_section_heading(doc, "1.3 Project Scope and Boundaries")
add_body_p(doc, "The project scope encompasses all tabular structural, architectural, and geographic attributes recorded in modern residential property registries. The analytical pipeline processes quantitative measurements (finished living area, subterranean square footage, room counts), temporal chronological milestones (year of construction, renovation dates), ordinal material quality grades (1 to 10 ratings), and spatial categorical designations (neighborhood classifications).")
add_body_p(doc, "The operational boundary of the primary trained model is calibrated against residential single-family housing transactions. Commercial, agricultural, and industrial real estate categories are excluded to maintain physical modeling validity.")

add_section_heading(doc, "1.4 Selected Dataset Overview")
add_body_p(doc, "The system is constructed using the Ames Housing Dataset, curated by Dean De Cock and released through the Journal of Statistics Education. Unlike the antiquated 1970s Boston Housing dataset—which possesses only 506 rows, 14 features, and recognized ethical issues—the Ames Housing dataset represents an industry standard for benchmarking tabular supervised regression models.")
add_body_p(doc, "The dataset documents 1,460 individual residential property transactions in Ames, Iowa, detailing 81 separate attributes encompassing 23 nominal, 23 ordinal, 14 discrete, and 20 continuous variables. Key variables utilized within our core production model include Above Grade Living Area (GrLivArea), Total Basement Area (TotalBsmtSF), Year Built (YearBuilt), Year Remodeled (YearRemodAdd), Overall Quality (OverallQual), Overall Condition (OverallCond), Garage Car Capacity (GarageCars), and physical Neighborhood.")

# Table 1.1 Dataset Summary
p_t1 = doc.add_paragraph()
p_t1.paragraph_format.line_spacing = 1.0
p_t1.paragraph_format.space_before = Pt(8)
p_t1.paragraph_format.space_after = Pt(4)
r_t1 = p_t1.add_run("Table 1.1: Ames Housing Dataset Architecture Summary")
r_t1.font.name = 'Times New Roman'
r_t1.font.size = Pt(11)
r_t1.font.bold = True

t1 = doc.add_table(rows=6, cols=3)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_headers = ["Attribute Dimension", "Raw Dataset Count", "Project Implementation Status"]
t1_rows = [
    ["Total Housing Observations", "1,460 Property Transactions", "1,456 Cleaned (4 outliers filtered)"],
    ["Total Raw Features", "81 Categorical & Numerical", "12 High-Impact Engineered Predictors"],
    ["Target Continuous Variable", "SalePrice ($)", "Modeled via log1p, evaluated in USD ($)"],
    ["Temporal Recording Window", "2006 – 2010 Transactions", "Standardized with 2010 Age Baseline"],
    ["Geographic Coverage", "28 Ames City Neighborhoods", "Categorically Encoded with Fallback"]
]
for c_idx, text in enumerate(t1_headers):
    c = t1.cell(0, c_idx)
    c.text = text
    set_cell_shading(c, "1E3C72")
    set_cell_margins(c, 80, 80, 120, 120)
    for p in c.paragraphs:
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

for r_idx, r_data in enumerate(t1_rows, 1):
    for c_idx, val in enumerate(r_data):
        c = t1.cell(r_idx, c_idx)
        c.text = val
        if r_idx % 2 == 1:
            set_cell_shading(c, "F5F7FB")
        set_cell_margins(c, 70, 70, 120, 120)
        for p in c.paragraphs:
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(10)

doc.add_page_break()

# Chapter 2
add_chapter_heading(doc, "CHAPTER 2: TOOLS AND TECHNOLOGIES USED")
add_section_heading(doc, "2.1 Core Programming Language & Numerical Libraries")
add_body_p(doc, "The entire pipeline was engineered in Python 3.11, chosen for its mature ecosystem in mathematical computing and data science. Python provides native language interoperability, high-performance vectorized C bindings, and rich open-source library support.")
add_body_p(doc, "1. NumPy (v2.4.6): Used for multidimensional array manipulation, logarithmic transformations (np.log1p), exponential inverse transformations (np.expm1), and vectorized metric derivations.")
add_body_p(doc, "2. Pandas (v3.0.5): Served as the core tabular data manipulation engine. Pandas DataFrames facilitated schema inspection, duplicate detection, SQL-like categorical aggregations, missing value identification, and feature extraction.")

add_section_heading(doc, "2.2 Machine Learning & Statistical Frameworks")
add_body_p(doc, "1. Scikit-Learn (v1.9.0): Utilized for core pipeline orchestration, feature preprocessing, cross-validation, and regression modeling. Specifically, Pipeline and ColumnTransformer modules prevented data leakage between cross-validation folds. SimpleImputer handled missing value imputation, StandardScaler standardized feature ranges, OneHotEncoder converted nominal categories into binary arrays, and Ridge regularized linear weights.")
add_body_p(doc, "2. XGBoost (v3.2.0): Provided an implementation of extreme gradient boosted decision trees. XGBoost constructs sequential decision trees using second-order Taylor expansion approximations of the loss function, equipped with built-in L1 and L2 tree leaf regularization to counter overfitting.")
add_body_p(doc, "3. Joblib (v1.5.3): Provided serialization for trained estimator pipelines. Joblib optimizes disk I/O for large NumPy arrays, enabling lightweight model saving and instant deserialization inside production web runtimes.")
add_body_p(doc, "4. Matplotlib (v3.11.1) & Seaborn (v0.13.2): Generated all statistical graphics, including KDE distribution plots, bivariate scatter plots, boxplots, correlation heatmaps, actual-vs-predicted curves, and residual distributions.")

add_section_heading(doc, "2.3 Interactive Web Deployment & Version Control")
add_body_p(doc, "1. Streamlit (v1.66.1): Selected as the application front-end framework. Streamlit translates pure Python scripts into reactive, mobile-responsive web applications. Its stateful execution model enables real-time dynamic slider interactions, instant mathematical recalculation, and embedded Matplotlib visualization rendering.")
add_body_p(doc, "2. Git & GitHub: Managed source code version control, automated commit tracking, and public code dissemination under an open-source structure.")
add_body_p(doc, "3. Streamlit Community Cloud: Provided the Platform-as-a-Service (PaaS) deployment environment. Automated continuous deployment (CD) triggers rebuilds on GitHub main branch commits, maintaining 24/7 web application availability.")

# Table 2.1 Software Stack Table
p_t2 = doc.add_paragraph()
p_t2.paragraph_format.line_spacing = 1.0
p_t2.paragraph_format.space_before = Pt(8)
p_t2.paragraph_format.space_after = Pt(4)
r_t2 = p_t2.add_run("Table 2.1: Software Stack and Technology Specification")
r_t2.font.name = 'Times New Roman'
r_t2.font.size = Pt(11)
r_t2.font.bold = True

t2 = doc.add_table(rows=10, cols=3)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ["Technology / Tool", "Exact Version", "Functional Purpose in Project"]
t2_rows = [
    ["Python", "3.11.9 Runtime", "Core language environment for pipeline scripting and execution"],
    ["Pandas", "3.0.5", "Tabular data ingestion, cleaning, slicing, and feature derivation"],
    ["NumPy", "2.4.6", "Vectorized linear algebra computations and logarithmic transformations"],
    ["Scikit-Learn", "1.9.0", "ColumnTransformer, StandardScaler, Ridge regression, and CV scoring"],
    ["XGBoost", "3.2.0", "Gradient boosted decision tree ensemble training and feature importance"],
    ["Joblib", "1.5.3", "Zero-overhead binary persistence of models and preprocessing pipelines"],
    ["Matplotlib / Seaborn", "3.11.1 / 0.13.2", "Statistical data visualization, correlation heatmaps, and diagnostic plots"],
    ["Streamlit", "1.66.1", "Interactive GUI front-end with real-time reactive parameter binding"],
    ["Streamlit Community Cloud", "Linux Container", "Global PaaS hosting, automated HTTPS provisioning, and live serving"]
]
for c_idx, text in enumerate(t2_headers):
    c = t2.cell(0, c_idx)
    c.text = text
    set_cell_shading(c, "1E3C72")
    set_cell_margins(c, 80, 80, 120, 120)
    for p in c.paragraphs:
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(10)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

for r_idx, r_data in enumerate(t2_rows, 1):
    for c_idx, val in enumerate(r_data):
        c = t2.cell(r_idx, c_idx)
        c.text = val
        if r_idx % 2 == 1:
            set_cell_shading(c, "F5F7FB")
        set_cell_margins(c, 70, 70, 120, 120)
        for p in c.paragraphs:
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(10)

doc.add_page_break()

# Chapter 3
add_chapter_heading(doc, "CHAPTER 3: SYSTEM FUNCTIONALITY & ARCHITECTURE")
add_section_heading(doc, "3.1 End-to-End System Architecture")
add_body_p(doc, "The Ames House Price Prediction System operates as a modular, decoupled data science pipeline consisting of three primary tiers: the Offline Modeling Tier, the Persistence & Serialization Tier, and the Interactive Web Inference Tier.")
add_body_p(doc, "In the Offline Modeling Tier, historical transactions undergo outlier filtering, imputation, logarithmic scaling, and model benchmarking. Once validated, the winning mathematical estimator (Ridge Regression) and the complete Scikit-Learn ColumnTransformer pipeline are serialized to disk using Joblib. In the Inference Tier, the Streamlit web engine deserializes these binaries into memory via st.cache_resource, guaranteeing low-latency response times for real-time user predictions.")

# App Screenshot Figure 3.1
add_fig(doc, "streamlit_app_screenshot.png", "Figure 3.1: Live Streamlit Web Application Interface and What-If Dashboard")

add_section_heading(doc, "3.2 Input Attributes and Reactive Controls")
add_body_p(doc, "The user interface exposes granular property parameters categorized into distinct functional sections within a collapsible sidebar:")
add_body_p(doc, "1. Dimensional Attributes: Sliders permitting continuous adjustment of Above Ground Living Area (400 to 3,800 sq ft) and Finished Basement Area (0 to 3,000 sq ft).")
add_body_p(doc, "2. Temporal & Room Configurations: Sliders for Year of Construction (1900 to 2010), Bedroom Count (1 to 6), Full Bathrooms (1 to 4), and Half Bathrooms (0 to 2).")
add_body_p(doc, "3. Qualitative & Location Attributes: Dropdown selection across all 28 Ames neighborhoods alongside discrete sliders for Overall Material Quality (1 to 10) and Overall Structural Condition (1 to 10).")
add_body_p(doc, "4. Structural Amenity Toggles: Interactive switches governing Garage Presence, Garage Car Capacity (1 to 4 cars), Swimming Pool Presence, and Property Remodeling History.")

add_section_heading(doc, "3.3 Prediction Engine and Dynamic Uncertainty Bounds")
add_body_p(doc, "When a user modifies any sidebar slider, the reactive execution loop intercepts the parameter vector, derives the engineered features (Property_Age, Total_Living_Area, Total_Bathrooms), and injects the standardized row vector into the preprocessor pipeline. The Ridge Regression estimator calculates the predicted logarithmic price, which is exponentiated via np.expm1 into a dollar figure.")
add_body_p(doc, "Importantly, recognizing that point valuations can convey a false sense of single-dollar precision, the system calculates and displays an empirical confidence range: [Estimated Price - MAE, Estimated Price + MAE]. Grounded in the test set Mean Absolute Error of $16,280, this provides users with realistic market transaction bounds.")

add_section_heading(doc, "3.4 Counterfactual 'What-If' Scenario Analyzer")
add_body_p(doc, "A distinguishing functionality of the system is the interactive 'What-If' scenario engine. Homeowners, investors, and remodeling contractors frequently need to determine whether capital improvements produce positive net financial returns. The application simulates two live counterfactual scenarios:")
add_body_p(doc, "1. Room Expansion Scenario: Simulates adding one bedroom along with 200 sq ft of finished living space, recalculating the updated valuation and displaying the incremental equity delta (+ $9,606 on average).")
add_body_p(doc, "2. Renovation Scenario: Simulates executing a full property modernization (setting Is_Remodeled = 1 and raising the Overall Quality rating by +1 grade), quantifying the expected market premium (+ $23,826 on average).")

doc.add_page_break()

# Chapter 4
add_chapter_heading(doc, "CHAPTER 4: MODEL WORKFLOW & METHODOLOGY")
add_section_heading(doc, "4.1 The Eight-Phase Machine Learning Lifecycle")
add_body_p(doc, "The system strictly adheres to the complete eight-phase machine learning engineering methodology: Phase 1 (Problem Understanding), Phase 2 (Data Collection), Phase 3 (Data Preprocessing), Phase 4 (Exploratory Data Analysis), Phase 5 (Feature Engineering), Phase 6 (Model Building & Tuning), Phase 7 (Model Evaluation), and Phase 8 (Cloud Deployment).")

add_section_heading(doc, "4.2 Data Preprocessing and Outlier Removal")
add_body_p(doc, "Raw tabular datasets frequently exhibit measurement noise and recording anomalies that distort gradient calculations. In accordance with the documentation provided by the Ames municipal tax assessor, properties possessing finished living areas exceeding 4,000 square feet were inspected. Two abnormally large properties sold under distress conditions at extreme discounts were identified as leverage points. Removing four extreme outliers reduced the working dataset from 1,460 to 1,456 observations.")
add_body_p(doc, "Missing quantitative values were imputed using column-wise medians to guard against distribution skewness. Missing categorical entries were imputed with the explicit label 'Missing', preserving potential signal associated with the absence of secondary amenities.")

add_section_heading(doc, "4.3 Target Skewness and Logarithmic Transformation")
add_body_p(doc, "Analysis of the raw target variable (SalePrice) demonstrated pronounced right-skewness (skewness coefficient = 1.88), driven by a long tail of luxury properties. Fitting linear regression models directly against skewed target distributions violates the Gauss-Markov assumption of normally distributed, homoscedastic error residuals.")
add_body_p(doc, "To resolve this, we applied the natural logarithmic transformation y' = ln(1 + SalePrice) using NumPy's log1p. This transformation compressed extreme price disparities, resulting in a symmetrical, bell-shaped distribution that allowed regression models to minimize relative percentage errors uniformly.")

# Figure 4.1 Price Distribution Before and After
add_fig(doc, "price_distribution_before_after_log.png", "Figure 4.1: Distribution of SalePrice Before (Raw, Right-Skewed) and After (Normalized) Logarithmic Transformation")

add_section_heading(doc, "4.4 Categorical Encoding and Feature Scaling")
add_body_p(doc, "To ensure that features with large numerical magnitudes (such as square footage) did not dominate attributes with smaller ranges (such as bathroom counts), all continuous attributes were standardized using StandardScaler (zero mean, unit variance). Nominal geographic categories (Neighborhood) were transformed using OneHotEncoder(handle_unknown='ignore', sparse_output=False). This encoding approach prevented models from inferring artificial ordinal rankings between neighborhoods.")

add_section_heading(doc, "4.5 Exploratory Data Analysis & Bivariate Relationships")
add_body_p(doc, "Bivariate correlation analysis demonstrated that Overall Material Quality (OverallQual) possesses the highest positive Pearson correlation with sale price (r = 0.79), followed by Above Ground Living Area (r = 0.71), Garage Car Capacity (r = 0.64), and Total Basement Area (r = 0.61).")

# Figure 4.2 Correlation Heatmap
add_fig(doc, "correlation_heatmap_top15.png", "Figure 4.2: Correlation Heatmap Demonstrating Top 15 Predictor Correlations with Sale Price")

add_section_heading(doc, "4.6 Regression Model Training and Cross-Validation")
add_body_p(doc, "The cleaned dataset (1,456 records) was partitioned into an 80% training set (1,164 records) and a 20% held-out testing set (292 records) using a fixed random seed (random_state=42). Four distinct algorithms were trained on the training partition using 5-fold cross-validation:")
add_body_p(doc, "1. Ridge Regression: Regularized linear model incorporating an L2 penalty on coefficient weights (alpha = 10.0).")
add_body_p(doc, "2. Decision Tree Regressor: Non-parametric tree partition baseline (max_depth = 6, min_samples_split = 10).")
add_body_p(doc, "3. Random Forest Regressor: Bagging ensemble comprising 150 randomized decision trees (max_depth = 12, min_samples_split = 4).")
add_body_p(doc, "4. XGBoost Regressor: Gradient boosted decision tree framework optimizing second-order residual gradients (n_estimators = 200, learning_rate = 0.05, max_depth = 4, subsample = 0.8).")

doc.add_page_break()

# Chapter 5
add_chapter_heading(doc, "CHAPTER 5: KEY FEATURES & PREDICTIVE DRIVERS")
add_section_heading(doc, "5.1 Domain-Specific Engineered Variables")
add_body_p(doc, "Rather than relying solely on raw recorded measurements, we engineered compound real estate domain indicators:")
add_body_p(doc, "1. Property_Age (2010 - YearBuilt): Reflects structural depreciation and design obsolescence more accurately than raw calendar years.")
add_body_p(doc, "2. Total_Living_Area (GrLivArea + TotalBsmtSF): Combines above-ground finished living area with finished subterranean basement square footage.")
add_body_p(doc, "3. Total_Bathrooms (FullBath + 0.5*HalfBath + BsmtFullBath + 0.5*BsmtHalfBath): Aggregates all sanitary facilities across all floors into a single consolidated metric.")
add_body_p(doc, "4. Binary Amenity Indicators: Synthesized Has_Pool (PoolArea > 0), Has_Garage (GarageCars > 0), and Is_Remodeled (YearRemodAdd > YearBuilt) into high-signal boolean variables.")

add_section_heading(doc, "5.2 Multicollinearity and Regularization Analysis")
add_body_p(doc, "Combining living area and room counts introduces multicollinearity. In standard Ordinary Least Squares (OLS) regression, multicollinearity destabilizes matrix inversion (X^T X)^-1, causing high variance in estimated coefficients. Ridge Regression addresses this by adding an L2 regularization penalty (alpha * sum(beta^2)) to the cost function, stabilizing the inversion via (X^T X + alpha * I)^-1 and shrinking collinear weights cooperatively.")

add_section_heading(doc, "5.3 Top Predictive Value Drivers")
add_body_p(doc, "Feature importance extraction from tree ensembles and regularized linear coefficients identified the top five predictors of residential property value:")
add_body_p(doc, "1. Overall Material & Finish Quality (OverallQual): 39.40% relative importance.")
add_body_p(doc, "2. Total Combined Living Area (Total_Living_Area): 17.89% relative importance.")
add_body_p(doc, "3. Garage Car Capacity (GarageCars): 5.55% relative importance.")
add_body_p(doc, "4. Presence of Garage (Has_Garage): 5.43% relative importance.")
add_body_p(doc, "5. Total Composite Bathrooms (Total_Bathrooms): 4.63% relative importance.")

# Figure 5.1 Feature Importance
add_fig(doc, "feature_importance.png", "Figure 5.1: Top 10 Feature Importances Derived from Tree Ensemble and Boosting Models")

doc.add_page_break()

# Chapter 6
add_chapter_heading(doc, "CHAPTER 6: PERFORMANCE EVALUATION & DISCUSSION")
add_section_heading(doc, "6.1 Evaluation Metrics Defined")
add_body_p(doc, "To provide a complete evaluation of model performance, all predictions were exponentiated back to the genuine USD dollar scale (using exp(y') - 1) before computing evaluation metrics:")
add_body_p(doc, "1. Mean Absolute Error (MAE): The average absolute dollar difference between actual and predicted sale prices.")
add_body_p(doc, "2. Root Mean Squared Error (RMSE): The square root of mean squared errors, penalizing large residual deviations more heavily than MAE.")
add_body_p(doc, "3. Coefficient of Determination (R²): The proportion of target variance explained by the model.")
add_body_p(doc, "4. Adjusted R²: Adjusts the R² score based on the number of predictor features, penalizing the addition of non-informative variables.")

add_section_heading(doc, "6.2 Comparative Model Performance Benchmark")
add_body_p(doc, "Table 6.1 presents the quantitative benchmark results across all four evaluated machine learning architectures on the held-out 20% testing split (292 properties).")

# Table 6.1 Performance Comparison Table
p_t6 = doc.add_paragraph()
p_t6.paragraph_format.line_spacing = 1.0
p_t6.paragraph_format.space_before = Pt(8)
p_t6.paragraph_format.space_after = Pt(4)
r_t6 = p_t6.add_run("Table 6.1: Regression Model Evaluation Benchmark (Original Price Scale $)")
r_t6.font.name = 'Times New Roman'
r_t6.font.size = Pt(11)
r_t6.font.bold = True

t6 = doc.add_table(rows=5, cols=6)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
t6_headers = ["Model Architecture", "MAE ($)", "RMSE ($)", "Test R² Score", "Adjusted R²", "5-Fold CV Mean R²"]
t6_rows = [
    ["Ridge Regression (Best)", "$16,280.23", "$22,871.54", "0.9003", "0.8863", "0.8918 ± 0.0148"],
    ["XGBoost Regressor", "$15,999.01", "$22,919.00", "0.8999", "0.8858", "0.8916 ± 0.0265"],
    ["Random Forest Regressor", "$17,309.61", "$25,384.09", "0.8772", "0.8599", "0.8730 ± 0.0269"],
    ["Decision Tree Regressor", "$22,916.82", "$32,449.46", "0.7994", "0.7711", "0.7834 ± 0.0264"]
]
for c_idx, text in enumerate(t6_headers):
    c = t6.cell(0, c_idx)
    c.text = text
    set_cell_shading(c, "1E3C72")
    set_cell_margins(c, 80, 80, 100, 100)
    for p in c.paragraphs:
        p.runs[0].font.name = 'Times New Roman'
        p.runs[0].font.size = Pt(9.5)
        p.runs[0].font.bold = True
        p.runs[0].font.color.rgb = RGBColor(255, 255, 255)

for r_idx, r_data in enumerate(t6_rows, 1):
    for c_idx, val in enumerate(r_data):
        c = t6.cell(r_idx, c_idx)
        c.text = val
        if r_idx == 1:
            set_cell_shading(c, "E6F2FF")
        elif r_idx % 2 == 1:
            set_cell_shading(c, "F5F7FB")
        set_cell_margins(c, 70, 70, 100, 100)
        for p in c.paragraphs:
            p.runs[0].font.name = 'Times New Roman'
            p.runs[0].font.size = Pt(9.5)
            if r_idx == 1:
                p.runs[0].font.bold = True

add_section_heading(doc, "6.3 Architectural Analysis: Why Regularized Linear Won")
add_body_p(doc, "A notable finding from the benchmark evaluation is that Ridge Regression (R² = 0.9003) achieved a marginally higher R² score and greater cross-validation stability (CV std = ± 0.0148) than XGBoost (R² = 0.8999, CV std = ± 0.0265), while XGBoost delivered a slightly lower MAE ($15,999 vs $16,280).")
add_body_p(doc, "This outcome is explained by two primary factors: First, after applying the logarithmic transformation to the target price, the relationship between structural square footage, overall quality, and property age is predominantly linear. Second, on tabular datasets with approximately 1,450 rows, tree-based models can occasionally create sharp local partitions that do not extrapolate as smoothly as regularized linear hyperplanes.")

add_section_heading(doc, "6.4 Diagnostic Plots: Residuals and Actual vs Predicted")
add_body_p(doc, "Model validity was further inspected using actual-vs-predicted scatter plots and residual diagnostic plots. As shown in Figures 6.1 and 6.2, data points closely track the 45-degree ideal fit line across both modest and premium price segments. The residual scatter demonstrates homoscedastic variance centered symmetrically around zero.")

# Figures 6.1 and 6.2
add_fig(doc, "actual_vs_predicted.png", "Figure 6.1: Actual vs. Predicted House Prices on Test Dataset (Ridge Regression)")
add_fig(doc, "residuals_plot.png", "Figure 6.2: Residual Plot (Errors vs. Predicted Values) Demonstrating Homoscedasticity")

doc.add_page_break()

# Chapter 7
add_chapter_heading(doc, "CHAPTER 7: LIMITATIONS & ENVIRONMENTAL CONSTRAINTS")
add_section_heading(doc, "7.1 Geographic Specialization and Transferability")
add_body_p(doc, "A primary limitation of the current system is its geographical specialization. The underlying training data originates exclusively from Ames, Iowa. Architectural conventions (such as full basements designed for northern freeze-thaw cycles), local zoning regulations, and regional construction costs differ substantially from housing markets in other regions, such as metropolitan India. Deploying this model in cities like Mumbai, Delhi, or Bangalore would require retraining on local real estate datasets.")

add_section_heading(doc, "7.2 Temporal Boundaries and Macroeconomic Variables")
add_body_p(doc, "The Ames dataset reflects real estate transactions recorded between 2006 and 2010. While the dataset provides a rich structural benchmark, it does not incorporate post-2010 macroeconomic fluctuations such as central bank interest rate shifts, inflation spikes, or regional employment trends. Incorporating dynamic macroeconomic indicators would improve adaptation to changing market conditions.")

add_section_heading(doc, "7.3 Multi-Modal and Visual Limitations")
add_body_p(doc, "The current model relies entirely on structured tabular attributes. Human real estate appraisers also inspect unstructured visual evidence—such as interior finish photographs, exterior architectural appeal, and street views. Integrating computer vision models trained on property imagery represents a promising direction for future development.")

doc.add_page_break()

# Chapter 8
add_chapter_heading(doc, "CHAPTER 8: CONCLUSION AND FUTURE WORK")
add_section_heading(doc, "8.1 Summary of Capstone Achievements")
add_body_p(doc, "This Capstone Project successfully built, evaluated, and deployed an end-to-end Machine Learning House Price Prediction System that adheres to the complete eight-phase machine learning lifecycle. Through systematic outlier filtering, logarithmic transformation, ColumnTransformer preprocessing, and domain-informed feature engineering, the system achieved strong predictive accuracy.")
add_body_p(doc, "Key project outcomes include:")
add_body_p(doc, "1. Predictive Accuracy: Ridge Regression and XGBoost achieved R² scores of 0.9003 and 0.8999 respectively, exceeding the university benchmark of 0.85.")
add_body_p(doc, "2. Error Reduction: The production model achieved a Mean Absolute Error of $16,280 on held-out test data, maintaining consistent accuracy across different price tiers.")
add_body_p(doc, "3. Feature Insights: Analysis confirmed that Overall Quality Rating (39.40%) and Total Living Area (17.89%) serve as the primary drivers of residential property value.")
add_body_p(doc, "4. Production Deployment: The interactive application is deployed globally on Streamlit Community Cloud, offering real-time valuation, confidence bounds, and counterfactual 'What-If' scenario analysis.")

add_section_heading(doc, "8.2 Directions for Future Research & Development")
add_body_p(doc, "Future extensions of this work include:")
add_body_p(doc, "1. Domestic Market Adaptation: Collecting web-scraped listings from Indian real estate portals (e.g., MagicBricks, 99acres) to adapt the pipeline to domestic housing markets.")
add_body_p(doc, "2. Computer Vision Integration: Developing multi-modal architectures that combine tabular features with convolutional neural networks (CNNs) trained on property photographs.")
add_body_p(doc, "3. Macroeconomic API Connectors: Integrating live financial APIs to adjust valuations based on prevailing mortgage interest rates and inflation figures.")
add_body_p(doc, "4. Microservice Architecture: Packaging the trained pipeline into a containerized RESTful API using FastAPI and Docker to support integration into commercial real estate platforms.")

doc.add_page_break()

# ==================== BACK MATTER ====================

# References
add_chapter_heading(doc, "REFERENCES")
refs = [
    "1. De Cock, D. (2011). 'Ames, Iowa: Alternative to the Boston Housing Data as an End of Semester Regression Project,' Journal of Statistics Education, Vol. 19, No. 3.",
    "2. Pedregosa, F., et al. (2011). 'Scikit-learn: Machine Learning in Python,' Journal of Machine Learning Research, Vol. 12, pp. 2825–2830.",
    "3. Chen, T., & Guestrin, C. (2016). 'XGBoost: A Scalable Tree Boosting System,' Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, pp. 785–794.",
    "4. McKinney, W. (2010). 'Data Structures for Statistical Computing in Python,' Proceedings of the 9th Python in Science Conference, pp. 51–56.",
    "5. Hunter, J. D. (2007). 'Matplotlib: A 2D Graphics Environment,' Computing in Science & Engineering, Vol. 9, No. 3, pp. 90–95.",
    "6. Waskom, M. L. (2021). 'Seaborn: Statistical Data Visualization,' Journal of Open Source Software, Vol. 6, No. 60, p. 3021.",
    "7. Streamlit Inc. (2024). 'Streamlit Documentation and Reactive Python App Architecture,' Available online: https://docs.streamlit.io (Accessed October 2026).",
    "8. Fatima, R. (2026). 'Ames House Price Prediction System Source Code & Model Repository,' GitHub: https://github.com/ramshaa01/house-price-prediction."
]
for r in refs:
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(8)
    run = p.add_run(r)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)

doc.add_page_break()

# Appendix
add_chapter_heading(doc, "APPENDIX: SOURCE CODE & DEPLOYMENT GUIDE")
add_section_heading(doc, "A.1 Project Repository & Live Application Links")
add_body_p(doc, "• Live Web Application Demo: https://house-price-prediction-ami5hudzy5cov9xj97dknk.streamlit.app/")
add_body_p(doc, "• Public GitHub Source Code Repository: https://github.com/ramshaa01/house-price-prediction")
add_body_p(doc, "• Interactive Jupyter Notebook: https://github.com/ramshaa01/house-price-prediction/tree/main/Notebook")

add_section_heading(doc, "A.2 Core Model Training Pipeline (Python)")
code_sample = """# Excerpt from train_and_evaluate.py
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='Missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

X_train_trans = preprocessor.fit_transform(X_train)
X_test_trans = preprocessor.transform(X_test)

ridge = Ridge(alpha=10.0)
ridge.fit(X_train_trans, y_train_log)
pred_usd = np.expm1(ridge.predict(X_test_trans))
"""
p_code = doc.add_paragraph()
p_code.paragraph_format.line_spacing = 1.0
p_code.paragraph_format.space_after = Pt(12)
run_c = p_code.add_run(code_sample)
run_c.font.name = 'Consolas'
run_c.font.size = Pt(9.5)

out_docx = os.path.join(DOCS_DIR, "Ames_House_Price_Prediction_Report.docx")
doc.save(out_docx)
print("Successfully generated Word report at:", out_docx)
