import streamlit as st

# ==========================================
# 0. Comprehensive Translation Dictionary
# ==========================================
TRANSLATIONS = {
    "en": {
        # --- General & Common ---
        "sub_title": "An Enterprise-Grade Automated Data Sanitation, Profiling, Interactive Analytics, and AI Reporting Engine.",
        "no_dataset": "📂 No Active Dataset: Upload a CSV or Excel file to begin analysis.",
        "active_dataset": "Active Dataset",
        "dimensions": "Dimensions",
        "rows": "rows",
        "cols": "columns",
        "proceed_btn": "Proceed to Interactive Dashboard Studio ➔",
        "lang_select": "🌐 Choose Language / اختر اللغة",
        
        # --- Home Page ---
        "title": "🔍 Exploratory Data Analysis (EDA) Studio",
        "sec1_title": "📊 Section 1: Single Variable Analysis (Univariate Analysis)",
        "sec2_title": "📈 Section 2: Multi-Variable Relationship Analysis",
        "sec3_title": "🧩 Section 3: Custom Data Aggregation & Pivot Table Builder",
        "sec4_title": "💡 Section 4: Automated AI EDA Insights",

        # --- Data Overview Page ---
        "Data Overview": "Data Overview",
        "do_title": "📋 Automated Data Overview & Health Audit",
        "do_sec1": "📁 Section 1: Dataset Information & Dtypes Breakdown",
        "do_file_name": "File Name",
        "do_total_rows": "Total Rows",
        "do_total_cols": "Total Columns",
        "do_memory": "Memory Footprint",
        "do_num_cols": "Numeric Columns",
        "do_cat_cols": "Text/Categorical",
        "do_date_cols": "Date/Time Columns",
        "do_bool_cols": "Boolean Columns",
        "do_sec2": "⭐ Section 2: Data Quality & Health Score",
        "do_health_metric": "Overall Health Metric:",

        # --- Feature Engineering Page ---
        "Feature Engineering": "Feature Engineering",
        "fe_title": "⚙️ Feature Engineering Studio",
        "fe_sub": "Create custom calculated columns, bin numerical features, scale variables, and perform transformations.",
        "fe_mod1_title": "➕ Module 1: Create Custom Calculated Column (A op B)",
        "fe_select_col1": "Select First Column (A)",
        "fe_select_op": "Select Operation",
        "fe_select_col2": "Select Second Column (B)",
        "fe_new_col_name": "New Column Name",
        "fe_btn_construct": "✨ Construct Calculated Feature",
        "fe_mod2_title": "📦 Module 2: Feature Binning / Quantization (Continuous to Categorical)",
        "fe_select_num_col": "Select Numeric Column to Bin",
        "fe_num_bins": "Number of Bins / Groups",
        "fe_binned_col_name": "Binned Column Name",
        "fe_btn_binned": "📦 Generate Binned Feature"
    },
    "ar": {
        # --- عام ومترجمات مشتركة ---
        "sub_title": "منصة ذكية ومتكاملة لتنظيف البيانات، التحليل الإحصائي، الرسوم التفاعلية وتوليد التقارير بالذكاء الاصطناعي.",
        "no_dataset": "📂 لا توجد بيانات نشطة: يرجى تحميل ملف CSV أو Excel للبدء.",
        "active_dataset": "مجموعة البيانات النشطة",
        "dimensions": "الأبعاد",
        "rows": "صفوف",
        "cols": "أعمدة",
        "proceed_btn": "الانتقال إلى استوديو لوحة التحكم التفاعلية ➔",
        "lang_select": "🌐 Choose Language / اختر اللغة",

        # --- الصفحة الرئيسية ---
        "title": "🔍 استوديو تحليل البيانات الاستكشافي (EDA)",
        "sec1_title": "📊 القسم الأول: تحليل المتغير الأحادي (Univariate Analysis)",
        "sec2_title": "📈 القسم الثاني: تحليل العلاقات متعددة المتغيرات",
        "sec3_title": "🧩 القسم الثالث: تجميع البيانات المخصص وبناء الجداول المحورية",
        "sec4_title": "💡 القسم الرابع: الرؤى والتحليلات الذكية الآلية",

        # --- صفحة نظرة عامة على البيانات ---
        "Data Overview": "نظرة عامة على البيانات",
        "do_title": "📋 ملخص البيانات الآلي وتدقيق الجودة",
        "do_sec1": "📁 القسم الأول: معلومات البيانات وتوزيع أنواع البيانات",
        "do_file_name": "اسم الملف",
        "do_total_rows": "إجمالي الصفوف",
        "do_total_cols": "إجمالي الأعمدة",
        "do_memory": "حجم الذاكرة",
        "do_num_cols": "الأعمدة الرقمية",
        "do_cat_cols": "النصوص / الفئات",
        "do_date_cols": "أعمدة التاريخ/الوقت",
        "do_bool_cols": "الأعمدة المنطقية",
        "do_sec2": "⭐ القسم الثاني: جودة البيانات ومؤشر الصحة",
        "do_health_metric": "مؤشر الصحة العام:",

        # --- صفحة هندسة الميزات ---
        "Feature Engineering": "هندسة الميزات والخصائص",
        "fe_title": "⚙️ استوديو هندسة الميزات والخصائص",
        "fe_sub": "إنشاء أعمدة جديدة، تقسيم البيانات الرقمية إلى فئات، والتحويلات الرياضية والتشفير.",
        "fe_mod1_title": "➕ الوحدة 1: إنشاء عمود محساب مخصص (A op B)",
        "fe_select_col1": "اختر العمود الأول (A)",
        "fe_select_op": "اختر العملية الحسابية",
        "fe_select_col2": "اختر العمود الثاني (B)",
        "fe_new_col_name": "اسم العمود الجديد",
        "fe_btn_construct": "✨ إنشاء الميزة الحسابية",
        "fe_mod2_title": "📦 الوحدة 2: تقسيم الميزات (Binning / Quantization)",
        "fe_select_num_col": "اختر العمود الرقمي للتقسيم",
        "fe_num_bins": "عدد المجموعات / الفئات",
        "fe_binned_col_name": "اسم العمود المجمع",
        "fe_btn_binned": "📦 إنشاء الميزة المجمعة"
    }
}

# ==========================================
# 1. Helper Functions
# ==========================================
def init_language():
    """إعداد زر اختيار اللغة في القائمة الجانبية وتحديث الواجهة فورياً"""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "en"

    with st.sidebar:
        st.markdown("---")
        
        current_index = 0 if st.session_state["lang"] == "en" else 1
        
        selected_lang_label = st.selectbox(
            "🌐 Language / اللغة",
            ["English", "العربية"],
            index=current_index,
            key="global_lang_selector"
        )
        
        # تحويل الاسم المختار إلى كود اللغة القياسي
        new_lang_code = "en" if selected_lang_label == "English" else "ar"
        
        # إذا تغيرت اللغة، نقوم بتحديث الـ session_state وإعادة تحميل الصفحة
        if new_lang_code != st.session_state["lang"]:
            st.session_state["lang"] = new_lang_code
            st.rerun()

def t(key: str) -> str:
    """دالة لجلب النص المترجم بحسب اللغة المختارة مع التراجع التلقائي للإنجليزية"""
    lang = st.session_state.get("lang", "en")
    
    # البحث عن النص باللغة الحالية، ثم بالإنجليزية، وأخيراً إرجاع المفتاح نفسه
    text = TRANSLATIONS.get(lang, {}).get(key)
    if text is None:
        text = TRANSLATIONS.get("en", {}).get(key, key)
        
    return text