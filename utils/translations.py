import streamlit as st

# ==========================================
# 0. Translation Dictionary
# ==========================================
TRANSLATIONS = {
    "en": {
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
    "ar": {
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
        
        # تحويل الاسم المحتار إلى كود اللغة القياسي
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