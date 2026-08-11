import streamlit as st

def init_language():
    """تثبيت اللغة الإنجليزية بشكل دائم بدون إظهار خيار التبديل في السايدبار"""
    st.session_state["lang"] = "en"

def t(key: str) -> str:
    """إرجاع مفتاح النص الأصلي كما هو باللغة الإنجليزية"""
    return key