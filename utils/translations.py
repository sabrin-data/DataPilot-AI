import streamlit as st

def init_language():
    """تثبيت اللغة الإنجليزية وإظهار اللوجو مرة واحدة فقط بدون تكرار"""
    st.session_state["lang"] = "en"
    
    # التحقق من عدم عرض اللوجو سابقاً لتجنب التكرار
    if "logo_rendered" not in st.session_state:
        try:
            st.sidebar.image("assets/logo.png", use_container_width=True)
            st.session_state["logo_rendered"] = True
        except Exception:
            pass

def t(key: str) -> str:
    """إرجاع مفتاح النص الأصلي كما هو باللغة الإنجليزية"""
    return key