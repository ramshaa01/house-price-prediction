import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

BASE_DIR = r"C:\Users\ramsh\.gemini\antigravity\scratch\House_Price_Prediction"
IMAGES_DIR = os.path.join(BASE_DIR, "Images")
DOCS_DIR = os.path.join(BASE_DIR, "Documentation")

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color Palette: Deep Navy, Vibrant Blue, Slate Grey, White
COLOR_NAVY = RGBColor(15, 32, 67)
COLOR_BLUE = RGBColor(30, 90, 180)
COLOR_LIGHT_BG = RGBColor(245, 247, 251)
COLOR_DARK_TEXT = RGBColor(20, 30, 45)
COLOR_WHITE = RGBColor(255, 255, 255)
COLOR_MUTED = RGBColor(100, 115, 130)

blank_layout = prs.slide_layouts[6]

def add_header(slide, title_text, category_text="CAPSTONE INTERNSHIP PRESENTATION"):
    # Header banner
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
    shape.fill.solid()
    shape.fill.fore_color.rgb = COLOR_NAVY
    shape.line.fill.background()

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.8)
    tf.margin_top = Inches(0.15)
    
    p1 = tf.paragraphs[0]
    p1.text = category_text.upper()
    p1.font.size = Pt(10)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(160, 195, 245)
    p1.font.name = "Arial"
    
    p2 = tf.add_paragraph()
    p2.text = title_text
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_WHITE
    p2.font.name = "Arial"

# Slide 1: Title Slide
s1 = prs.slides.add_slide(blank_layout)
bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg1.fill.solid()
bg1.fill.fore_color.rgb = COLOR_NAVY
bg1.line.fill.background()

tb1 = s1.shapes.add_textbox(Inches(1.0), Inches(1.3), Inches(11.333), Inches(4.5))
tf1 = tb1.text_frame
tf1.word_wrap = True

p_sub = tf1.paragraphs[0]
p_sub.text = "MINI PROJECT REPORT OF INTERNSHIP • 2026-27"
p_sub.font.size = Pt(13)
p_sub.font.bold = True
p_sub.font.color.rgb = RGBColor(140, 185, 245)

p_main = tf1.add_paragraph()
p_main.text = "Ames House Price Prediction System"
p_main.font.size = Pt(40)
p_main.font.bold = True
p_main.font.color.rgb = COLOR_WHITE
p_main.space_after = Pt(20)

p_desc = tf1.add_paragraph()
p_desc.text = "An End-to-End Supervised Machine Learning Pipeline & Interactive Deployment"
p_desc.font.size = Pt(18)
p_desc.font.color.rgb = RGBColor(210, 225, 245)
p_desc.space_after = Pt(40)

# Student & Supervisor Info Box
card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.7), Inches(11.333), Inches(2.0))
card.fill.solid()
card.fill.fore_color.rgb = RGBColor(25, 48, 92)
card.line.color.rgb = RGBColor(50, 85, 150)
tf_card = card.text_frame
tf_card.margin_left = Inches(0.4)
tf_card.margin_top = Inches(0.25)

p_cand = tf_card.paragraphs[0]
p_cand.text = "Presented By: Ramsha Fatima  |  Roll No: 2300101530112"
p_cand.font.size = Pt(14)
p_cand.font.bold = True
p_cand.font.color.rgb = COLOR_WHITE

p_sup = tf_card.add_paragraph()
p_sup.text = "Under the Supervision of: Mr. Arpit Dubey, Assistant Professor"
p_sup.font.size = Pt(13)
p_sup.font.color.rgb = RGBColor(200, 215, 235)

p_inst = tf_card.add_paragraph()
p_inst.text = "Department of Computer Science and Engineering, United College of Engineering & Research, Prayagraj"
p_inst.font.size = Pt(12)
p_inst.font.color.rgb = RGBColor(170, 195, 225)

p_aff = tf_card.add_paragraph()
p_aff.text = "Affiliated to Dr. A.P.J. Abdul Kalam Technical University, Lucknow | Organization: Innovation & Incubation Hub Foundation, MNNIT"
p_aff.font.size = Pt(11)
p_aff.font.color.rgb = RGBColor(150, 180, 215)


# Slide 2: Objectives & Problem Statement
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "Chapter 1: Problem Statement & Project Objectives")

# Left Box: The Problem
box_l = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
box_l.fill.solid()
box_l.fill.fore_color.rgb = COLOR_LIGHT_BG
box_l.line.color.rgb = RGBColor(210, 220, 235)
tf_l = box_l.text_frame
tf_l.margin_left = Inches(0.3)
tf_l.margin_top = Inches(0.3)
p = tf_l.paragraphs[0]
p.text = "The Real Estate Valuation Challenge"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(14)

points_l = [
    ("Price Opacity: ", "Property evaluations traditionally rely on manual heuristics and personal appraisal bias."),
    ("Market Inefficiencies: ", "Sellers, buyers, and mortgage lenders face substantial price variance for structurally comparable properties."),
    ("Non-Linear Dynamics: ", "Valuations are driven by complex multi-feature interactions (area, age, location, and finish)."),
    ("The Need: ", "An automated, transparent, machine learning-driven pricing engine with empirical confidence bounds.")
]
for title, desc in points_l:
    p = tf_l.add_paragraph()
    p.text = "• " + title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(10)

# Right Box: Specific Objectives
box_r = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
box_r.fill.solid()
box_r.fill.fore_color.rgb = COLOR_LIGHT_BG
box_r.line.color.rgb = RGBColor(210, 220, 235)
tf_r = box_r.text_frame
tf_r.margin_left = Inches(0.3)
tf_r.margin_top = Inches(0.3)
p = tf_r.paragraphs[0]
p.text = "Project Mandate & Objectives"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(14)

points_r = [
    ("End-to-End ML Lifecycle: ", "Strict adherence to all 8 phases of data science and machine learning development."),
    ("Ames Benchmark Dataset: ", "Comprehensive analysis of 1,460 residential properties across 81 structural attributes."),
    ("Target Accuracy Metric: ", "Exceed an R² score of 0.85 on held-out test data on the genuine dollar scale."),
    ("Multi-Model Benchmarking: ", "Evaluate Ridge, Decision Trees, Random Forest, and XGBoost using 5-Fold Cross Validation."),
    ("Interactive Deployment: ", "Deploy a responsive web app on Streamlit Cloud with real-time 'What-If' counterfactual analysis.")
]
for title, desc in points_r:
    p = tf_r.add_paragraph()
    p.text = "• " + title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(10)


# Slide 3: Tools & Technologies Used
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "Chapter 2: Tools & Technology Stack Architecture")

tools = [
    ("Python 3.11", "Core Language", "High-performance tabular processing & model execution runtime."),
    ("Pandas & NumPy", "Data Manipulation", "Matrix vectorized calculations, tabular restructuring & log1p transforms."),
    ("Scikit-Learn", "Machine Learning", "Pipeline, ColumnTransformer, StandardScaler, Ridge & Random Forest."),
    ("XGBoost", "Gradient Boosting", "Extreme gradient boosted regression trees for non-linear residual learning."),
    ("Matplotlib & Seaborn", "Visualization", "Publication-ready statistical plots, correlation heatmaps, residual diagnostics."),
    ("Joblib", "Serialization", "Zero-overhead binary persistence of trained models and scaling pipelines."),
    ("Streamlit", "App Framework", "Reactive Python-native web application with dynamic state management."),
    ("Git & GitHub", "Version Control", "Public open-source repository management with automated CI/CD flow."),
    ("Streamlit Cloud", "Cloud Deployment", "PaaS containerized microservice serving predictions globally 24/7.")
]

for idx, (tool, role, purpose) in enumerate(tools):
    col = idx % 3
    row = idx // 3
    left = Inches(0.8 + col * 4.0)
    top = Inches(1.5 + row * 1.8)
    card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(1.6))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_LIGHT_BG
    card.line.color.rgb = RGBColor(210, 225, 240)
    tf = card.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = tool
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    p2 = tf.add_paragraph()
    p2.text = role.upper()
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_BLUE
    
    p3 = tf.add_paragraph()
    p3.text = purpose
    p3.font.size = Pt(10)
    p3.font.color.rgb = COLOR_DARK_TEXT


# Slide 4: System Functionality & Live UI
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "Chapter 3: System Functionality & Live Application UI")

# Left Column: Features
box_desc = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.0), Inches(5.6))
box_desc.fill.solid()
box_desc.fill.fore_color.rgb = COLOR_LIGHT_BG
box_desc.line.color.rgb = RGBColor(210, 225, 240)
tf = box_desc.text_frame
tf.margin_left = Inches(0.25)
tf.margin_top = Inches(0.25)

p = tf.paragraphs[0]
p.text = "Interactive Web Capabilities"
p.font.size = Pt(17)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(10)

features = [
    ("Real-Time Input Panel: ", "Dynamic sliders for living area, basement sq ft, construction year, room counts, and neighborhood."),
    ("Instant Fair Valuation: ", "Point prediction plus empirical confidence range (± 1 MAE: $16,280)."),
    ("What-If Scenario Analyzer: ", "Instant financial ROI feedback for adding a bedroom (+200 sq ft) or completing a full remodel."),
    ("Embedded EDA Dashboard: ", "Live tabs with market price distribution and correlation heatmaps."),
    ("Zero-Crash Deployment: ", "Relative pathing via pathlib and pinned dependency tree ensures 100% Linux cloud uptime.")
]
for title, desc in features:
    p = tf.add_paragraph()
    p.text = "• " + title
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(8)

# Right Column: Screenshot
img_path = os.path.join(IMAGES_DIR, "streamlit_app_screenshot.png")
if os.path.exists(img_path):
    s4.shapes.add_picture(img_path, Inches(6.1), Inches(1.4), width=Inches(6.4))


# Slide 5: The Complete Machine Learning Lifecycle
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "Chapter 4: End-to-End Machine Learning Lifecycle")

phases = [
    ("Phase 1: Problem Definition", "Identified residential price opacity; defined supervised continuous regression."),
    ("Phase 2: Data Collection", "Fetched Ames benchmark dataset (1,460 records across 81 structural features)."),
    ("Phase 3: Data Preprocessing", "Removed 4 extreme outliers (GrLivArea > 4000); median & mode imputation; log1p transform."),
    ("Phase 4: Exploratory Data Analysis", "Identified strong right-skewness, quality grading separation, and neighborhood price tiers."),
    ("Phase 5: Feature Engineering", "Engineered Property_Age, Total_Living_Area, Total_Bathrooms, and amenity indicators."),
    ("Phase 6: Model Building & Tuning", "Trained Ridge, Decision Tree, Random Forest, and XGBoost with 5-Fold Cross Validation."),
    ("Phase 7: Model Evaluation", "Benchmarked on held-out 20% test split on genuine USD dollar scale (MAE, RMSE, R²)."),
    ("Phase 8: Cloud Deployment", "Deployed interactive Streamlit app to Streamlit Community Cloud with GitHub CI/CD.")
]

for idx, (p_title, p_desc) in enumerate(phases):
    col = idx % 2
    row = idx // 2
    left = Inches(0.8 + col * 5.9)
    top = Inches(1.4 + row * 1.35)
    
    card = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.6), Inches(1.2))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_LIGHT_BG
    card.line.color.rgb = RGBColor(210, 225, 240)
    tf = card.text_frame
    tf.margin_left = Inches(0.2)
    tf.margin_top = Inches(0.12)
    
    p = tf.paragraphs[0]
    p.text = p_title
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = p_desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK_TEXT


# Slide 6: Exploratory Data Analysis (EDA) Highlights
s6 = prs.slides.add_slide(blank_layout)
add_header(s6, "Chapter 4: Exploratory Data Analysis (EDA) Key Insights")

p1_path = os.path.join(IMAGES_DIR, "price_distribution_before_after_log.png")
if os.path.exists(p1_path):
    s6.shapes.add_picture(p1_path, Inches(0.8), Inches(1.4), width=Inches(5.7))

p5_path = os.path.join(IMAGES_DIR, "correlation_heatmap_top15.png")
if os.path.exists(p5_path):
    s6.shapes.add_picture(p5_path, Inches(6.8), Inches(1.4), width=Inches(5.7))

# Bottom Annotation Banner
banner = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.7), Inches(11.7), Inches(1.3))
banner.fill.solid()
banner.fill.fore_color.rgb = COLOR_NAVY
banner.line.fill.background()
tf = banner.text_frame
tf.margin_left = Inches(0.3)
tf.margin_top = Inches(0.15)
p = tf.paragraphs[0]
p.text = "CRITICAL EDA TAKEAWAYS:"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = RGBColor(160, 200, 255)

p2 = tf.add_paragraph()
p2.text = "1. Target Log-Transform: Converted skewed $180k median distribution to normal bell curve, stabilizing regression variance."
p2.font.size = Pt(11)
p2.font.color.rgb = COLOR_WHITE

p3 = tf.add_paragraph()
p3.text = "2. Dominant Correlates: Overall Quality (r = 0.79), Living Area (r = 0.71), Garage Capacity (r = 0.64), and Basement Area (r = 0.61)."
p3.font.size = Pt(11)
p3.font.color.rgb = COLOR_WHITE


# Slide 7: Feature Engineering & Domain Importance
s7 = prs.slides.add_slide(blank_layout)
add_header(s7, "Chapter 5: Feature Engineering & Top Value Drivers")

# Left: Engineered Features
box_fe = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.4), Inches(5.6))
box_fe.fill.solid()
box_fe.fill.fore_color.rgb = COLOR_LIGHT_BG
box_fe.line.color.rgb = RGBColor(210, 225, 240)
tf = box_fe.text_frame
tf.margin_left = Inches(0.25)
tf.margin_top = Inches(0.25)

p = tf.paragraphs[0]
p.text = "Domain-Specific Formulations"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(12)

fe_items = [
    ("Property_Age = 2010 - YearBuilt", "Quantifies true structural depreciation rather than arbitrary calendar dates."),
    ("Total_Living_Area = GrLivArea + TotalBsmtSF", "Combines above-ground and subterranean finished square footage for total usable area."),
    ("Total_Bathrooms = FullBath + 0.5*HalfBath...", "Unified sanitary metric capturing full and half fixtures throughout the house."),
    ("Has_Pool & Has_Garage", "Binary indicators transforming sparse counts into high-signal boolean flags."),
    ("Is_Remodeled = (YearRemodAdd > YearBuilt)", "Detects whether modern renovations have offset property age.")
]
for form, exp in fe_items:
    p = tf.add_paragraph()
    p.text = "• " + form
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = "\n  " + exp
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(8)

# Right: Feature Importance Plot
fi_path = os.path.join(IMAGES_DIR, "feature_importance.png")
if os.path.exists(fi_path):
    s7.shapes.add_picture(fi_path, Inches(6.5), Inches(1.4), width=Inches(6.0))


# Slide 8: Model Evaluation & Performance Benchmark
s8 = prs.slides.add_slide(blank_layout)
add_header(s8, "Chapter 6: Model Evaluation & Comparative Benchmark")

# Metrics Table
rows = 5
cols = 6
table_shape = s8.shapes.add_table(rows, cols, Inches(0.8), Inches(1.5), Inches(11.733), Inches(2.2))
table = table_shape.table

headers = ["Model Architecture", "MAE ($)", "RMSE ($)", "Test R² Score", "Adjusted R²", "5-Fold CV Mean R²"]
for idx, h in enumerate(headers):
    cell = table.cell(0, idx)
    cell.text = h
    cell.fill.solid()
    cell.fill.fore_color.rgb = COLOR_NAVY
    for p in cell.text_frame.paragraphs:
        p.font.bold = True
        p.font.size = Pt(11)
        p.font.color.rgb = COLOR_WHITE
        p.alignment = PP_ALIGN.CENTER

data = [
    ["Ridge Regression (Winner)", "$16,280.23", "$22,871.54", "0.9003", "0.8863", "0.8918 ± 0.015"],
    ["XGBoost Regressor", "$15,999.01", "$22,919.00", "0.8999", "0.8858", "0.8916 ± 0.027"],
    ["Random Forest Regressor", "$17,309.61", "$25,384.09", "0.8772", "0.8599", "0.8730 ± 0.027"],
    ["Decision Tree Regressor", "$22,916.82", "$32,449.46", "0.7994", "0.7711", "0.7834 ± 0.026"]
]

for row_idx, row_data in enumerate(data, 1):
    for col_idx, val in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        cell.text = val
        cell.fill.solid()
        if row_idx == 1:
            cell.fill.fore_color.rgb = RGBColor(230, 242, 255)
        else:
            cell.fill.fore_color.rgb = COLOR_WHITE if row_idx % 2 == 0 else COLOR_LIGHT_BG
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = (row_idx == 1 or col_idx == 0)
            p.font.color.rgb = COLOR_BLUE if (row_idx == 1 and col_idx == 3) else COLOR_DARK_TEXT
            p.alignment = PP_ALIGN.CENTER if col_idx > 0 else PP_ALIGN.LEFT

# Bottom: Model Diagnostics Graphics
p6_path = os.path.join(IMAGES_DIR, "actual_vs_predicted.png")
p7_path = os.path.join(IMAGES_DIR, "residuals_plot.png")
if os.path.exists(p6_path):
    s8.shapes.add_picture(p6_path, Inches(0.8), Inches(4.0), width=Inches(5.7))
if os.path.exists(p7_path):
    s8.shapes.add_picture(p7_path, Inches(6.8), Inches(4.0), width=Inches(5.7))


# Slide 9: Limitations & Real-World Constraints
s9 = prs.slides.add_slide(blank_layout)
add_header(s9, "Chapter 7: Limitations & Environmental Constraints")

limits = [
    ("Geographic & Demographic Specialization", 
     "Trained strictly on Ames, Iowa housing transactions. Market price baselines and architectural styles cannot be directly extrapolated to Indian metropolitan areas without local calibration."),
    
    ("Static Sample Boundary", 
     "Comprises 1,456 historical residential properties up to 2010. Does not account for post-2010 macroeconomic fluctuations such as inflation surges, interest rate shifts, and real estate market cycles."),
     
    ("Missing Multi-Modal Features", 
     "Does not incorporate unstructured visual imagery (interior quality photos, street appeal) or satellite GIS elevation and zoning data, which human appraisers naturally inspect."),
     
    ("Empirical Confidence Limits", 
     "The predicted valuation is accompanied by a ± 1 MAE ($16,280) interval; edge cases with extreme bespoke luxury configurations remain subject to higher variance.")
]

for idx, (title, desc) in enumerate(limits):
    top = Inches(1.5 + idx * 1.35)
    card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.733), Inches(1.15))
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_LIGHT_BG
    card.line.color.rgb = RGBColor(215, 225, 240)
    tf = card.text_frame
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = f"{idx+1}. {title}"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = COLOR_DARK_TEXT


# Slide 10: Conclusion & Future Scope
s10 = prs.slides.add_slide(blank_layout)
add_header(s10, "Chapter 8: Conclusion & Future Roadmap")

# Left: Conclusions
box_c = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.4))
box_c.fill.solid()
box_c.fill.fore_color.rgb = COLOR_LIGHT_BG
box_c.line.color.rgb = RGBColor(210, 225, 240)
tf = box_c.text_frame
tf.margin_left = Inches(0.3)
tf.margin_top = Inches(0.3)
p = tf.paragraphs[0]
p.text = "Key Project Achievements"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(14)

c_points = [
    ("Exceeded 85% Benchmark: ", "Ridge achieved 90.03% R² and XGBoost achieved 89.99% R² on the genuine dollar scale."),
    ("Validated Generalization: ", "5-Fold Cross Validation confirmed tight standard deviation (± 0.015), ruling out overfitting."),
    ("Robust Pipeline Architecture: ", "Sklearn ColumnTransformer prevented data leakage while handling scaling and categorical encoding."),
    ("Live Public Deployment: ", "Successfully deployed globally on Streamlit Community Cloud with interactive What-If simulation.")
]
for title, desc in c_points:
    p = tf.add_paragraph()
    p.text = "✓ " + title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(15, 120, 60)
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(10)

# Right: Future Scope
box_f = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.4))
box_f.fill.solid()
box_f.fill.fore_color.rgb = COLOR_LIGHT_BG
box_f.line.color.rgb = RGBColor(210, 225, 240)
tf_f = box_f.text_frame
tf_f.margin_left = Inches(0.3)
tf_f.margin_top = Inches(0.3)
p = tf_f.paragraphs[0]
p.text = "Future Technical Roadmap"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = COLOR_NAVY
p.space_after = Pt(14)

f_points = [
    ("Indian Market Retraining: ", "Collect Tier-1/Tier-2 Indian city property data (MagicBricks / 99acres) for domestic valuation."),
    ("Computer Vision Integration: ", "Use Convolutional Neural Networks (CNNs) / Vision Transformers to grade interior finishes from photos."),
    ("Real-Time Financial APIs: ", "Integrate real-time inflation and mortgage rate APIs for dynamic macro adjustments."),
    ("RESTful Microservice: ", "Wrap pipeline in FastAPI / Docker for seamless integration into real estate listing portals.")
]
for title, desc in f_points:
    p = tf_f.add_paragraph()
    p.text = "➔ " + title
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = COLOR_BLUE
    run = p.add_run()
    run.text = desc
    run.font.bold = False
    run.font.color.rgb = COLOR_DARK_TEXT
    p.space_after = Pt(10)


# Slide 11: Demonstration & Project Links
s11 = prs.slides.add_slide(blank_layout)
bg11 = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
bg11.fill.solid()
bg11.fill.fore_color.rgb = COLOR_NAVY
bg11.line.fill.background()

tb = s11.shapes.add_textbox(Inches(1.0), Inches(1.0), Inches(11.333), Inches(5.5))
tf = tb.text_frame
tf.word_wrap = True

p = tf.paragraphs[0]
p.text = "Project Demonstration & Code Access"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = COLOR_WHITE
p.space_after = Pt(30)

links = [
    ("Live Interactive Web Application:", "https://house-price-prediction-ami5hudzy5cov9xj97dknk.streamlit.app/"),
    ("Public GitHub Source Repository:", "https://github.com/ramshaa01/house-price-prediction"),
    ("Model Artifacts & Jupyter Notebook:", "https://github.com/ramshaa01/house-price-prediction/tree/main/Notebook"),
    ("Documentation & Viva Guide:", "https://github.com/ramshaa01/house-price-prediction/tree/main/Documentation")
]

for title, url in links:
    p = tf.add_paragraph()
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(140, 195, 255)
    
    p2 = tf.add_paragraph()
    p2.text = url
    p2.font.size = Pt(14)
    p2.font.color.rgb = COLOR_WHITE
    p2.space_after = Pt(16)

p_thanks = tf.add_paragraph()
p_thanks.text = "Thank You! Questions & Discussion are Welcome."
p_thanks.font.size = Pt(22)
p_thanks.font.bold = True
p_thanks.font.color.rgb = RGBColor(240, 245, 255)

out_pptx = os.path.join(DOCS_DIR, "House_Price_Prediction_Presentation.pptx")
prs.save(out_pptx)
print("Saved presentation to:", out_pptx)
