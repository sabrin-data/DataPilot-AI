import streamlit as st

# قاموس النصوص للغتين
TRANSLATIONS = {
    "English": {
        "title": "🔍 Exploratory Data Analysis (EDA) Studio",
        "sub_title": "Interactive statistical analysis, dynamic visual relationship discovery, and automated data insights.",
        "active_dataset": "Active Dataset",
        "dimensions": "Dimensions",
        "rows": "rows",
        "cols": "columns",
        "sec1_title": "📊 Section 1: Single Variable Analysis (Univariate Analysis)",
        "sec2_title": "📈 Section 2: Multi-Variable Relationship Analysis",
        "sec3_title": "🧩 Section 3: Custom Data Aggregation & Pivot Table Builder",
        "sec4_title": "💡 Section 4: Automated AI EDA Insights",
        "no_dataset": "📂 Please upload a dataset first from the Upload page.",
        "proceed_btn": "Proceed to Interactive Dashboard Studio ➔",
        "lang_select": "🌐 Choose Language / اختر اللغة"
    },
    "العربية": {
        "title": "🔍 استوديو تحليل البيانات الاستكشافي (EDA)",
        "sub_title": "تحليل إحصائي تفاعلي، اكتشاف العلاقات البصرية، واستخراج الأفكار الآلية للبيانات.",
        "active_dataset": "مجموعة البيانات النشطة",
        "dimensions": "الأبعاد",
        "rows": "صفوف",
        "cols": "أعمدة",
        "sec1_title": "📊 القسم الأول: تحليل المتغير المالي (Univariate)",
        "sec2_title": "📈 القسم الثاني: تحليل العلاقات متعددة المتغيرات",
        "sec3_title": "🧩 القسم الثالث: تجميع البيانات المخصص وبناء الجداول المحورية",
        "sec4_title": "💡 القسم الرابع: الرؤى والتحليلات الذكية الآلية",
        "no_dataset": "📂 يرجى رفع ملف البيانات أولاً من صفحة الرفع (Upload).",
        "proceed_btn": "الانتقال إلى استوديو لوحة التحكم التفاعلية ➔",
        "lang_select": "🌐 Choose Language / اختر اللغة"
    }
}

def init_language():
    """إعداد زر اختيار اللغة في القائمة الجانبية وتخزينها في session_state"""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "English"

    with st.sidebar:
        st.markdown("---")
        selected_lang = st.selectbox(
            "🌐 Language / اللغة",
            ["English", "العربية"],
            index=0 if st.session_state["lang"] == "English" else 1,
            key="global_lang_selector"
        )
        st.session_state["lang"] = selected_lang

def t(key):
    """دالة لجلب النص المترجم بحسب اللغة المختارة"""
    lang = st.session_state.get("lang", "English")
    return TRANSLATIONS.get(lang, {}).get(key, key)
