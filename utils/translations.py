import streamlit as st

def init_language():
    """تثبيت اللغة الإنجليزية بشكل دائم وإظهار اللوجو في السايدبار"""
    st.session_state["lang"] = "en"
    
    # إظهار اللوجو في أعلى القائمة الجانبية (Sidebar) لكل الصفحات
    try:
        st.sidebar.image("assets/logo.png", use_container_width=True)
    except Exception:
        pass

def t(key: str) -> str:
    """إرجاع مفتاح النص الأصلي كما هو باللغة الإنجليزية"""
    return key