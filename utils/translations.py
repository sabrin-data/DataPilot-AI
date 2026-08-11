import streamlit as st

def init_language():
    """تثبيت اللغة الإنجليزية بشكل دائم"""
    st.session_state["lang"] = "en"

def t(key: str) -> str:
    """إرجاع مفتاح النص الأصلي كما هو باللغة الإنجليزية"""
    return key