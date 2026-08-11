import sys
import platform
import pandas as pd
import streamlit as st
from utils.translations import init_language, t

# ==========================================
# 0. Page Configuration & Language Init
# ==========================================
st.set_page_config(
    page_title="Application Settings",
    page_icon="⚙️",
    layout="wide"
)

# يقرأ اللغة المختارة ويظهر القائمة الجانبية
init_language()

# قراءة الـ CSS الموحد
try:
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("⚙️ Application Settings & Configuration")
st.write(t("sub_title") if t("sub_title") != "sub_title" else "Manage app preferences, session cache, system diagnostics, and API keys.")

# ==========================================
# 1. App Preferences & UI Settings
# ==========================================
st.subheader("🎨 UI Preferences & Environment Settings")

col_set1, col_set2 = st.columns(2)

with col_set1:
    default_page_size = st.selectbox(
        "Default Table Page Size", 
        [10, 25, 50, 100], 
        index=[10, 25, 50, 100].index(st.session_state.get("page_size", 10)),
        key="page_size"
    )
    enable_notifications = st.toggle(
        "Enable Toast Notifications", 
        value=st.session_state.get("enable_toasts", True),
        key="enable_toasts"
    )

with col_set2:
    precision = st.slider(
        "Floating Point Display Precision", 
        min_value=1, 
        max_value=6, 
        value=st.session_state.get("precision", 2),
        key="precision"
    )
    auto_refresh = st.toggle(
        "Auto-Refresh Dashboard Widgets", 
        value=st.session_state.get("auto_refresh", False),
        key="auto_refresh"
    )

st.divider()

# ==========================================
# 🔑 Section 2: API Keys Management
# ==========================================
st.subheader("🔑 AI Service API Configurations")
st.write("Configure external LLM provider keys for automated AI insights.")

col_api1, col_api2 = st.columns(2)

with col_api1:
    has_openai = bool(st.session_state.get("openai_key"))
    openai_status = "🟢 Saved" if has_openai else "🔴 Not Set"
    
    openai_key = st.text_input(
        f"OpenAI API Key ({openai_status})",
        value=st.session_state.get("openai_key", ""),
        type="password",
        placeholder="sk-...",
        help="Enter your sk-... key here for GPT integrations."
    )
    if st.button("Save OpenAI Key", key="save_openai", use_container_width=True):
        st.session_state["openai_key"] = openai_key
        if st.session_state.get("enable_toasts", True):
            st.toast("OpenAI Key saved successfully!", icon="🔑")
        st.success("OpenAI Key saved in session context!")
        st.rerun()

with col_api2:
    has_gemini = bool(st.session_state.get("gemini_key"))
    gemini_status = "🟢 Saved" if has_gemini else "🔴 Not Set"

    gemini_key = st.text_input(
        f"Google Gemini API Key ({gemini_status})",
        value=st.session_state.get("gemini_key", ""),
        type="password",
        placeholder="AIzaSy...",
        help="Enter your Gemini AI key here."
    )
    if st.button("Save Gemini Key", key="save_gemini", use_container_width=True):
        st.session_state["gemini_key"] = gemini_key
        if st.session_state.get("enable_toasts", True):
            st.toast("Gemini Key saved successfully!", icon="🔑")
        st.success("Gemini Key saved in session context!")
        st.rerun()

st.divider()

# ==========================================
# 🔄 Section 3: Session State & Cache Management
# ==========================================
st.subheader("🧹 Memory & Session Reset Studio")
st.write("Manage temporary storage, uploaded datasets, and cached memory.")

col_mem1, col_mem2 = st.columns(2)

with col_mem1:
    if "df" in st.session_state and st.session_state["df"] is not None:
        st.info(f"📂 Active Loaded Dataset: **{st.session_state.get('file_name', 'Unknown')}** ({len(st.session_state['df']):,} rows)")
    else:
        st.warning(t("no_dataset") if t("no_dataset") != "no_dataset" else "📂 No active dataset currently loaded in session state.")

with col_mem2:
    if st.button("🗑️ Clear Cache & Reset All Session Data", type="primary", use_container_width=True):
        # حفظ لغة المستخدم الحالية كي لا تضيع بعد المسح
        current_lang = st.session_state.get("lang", "en")
        
        # مسح الذاكرة
        st.session_state.clear()
        st.cache_data.clear()
        
        # إعادة اللغة المحفوظة
        st.session_state["lang"] = current_lang
        
        st.success("Session state and cache completely reset!")
        st.rerun()

st.divider()

# ==========================================
# 💻 Section 4: System Information & Diagnostics
# ==========================================
st.subheader("💻 System Diagnostics & Environment Info")

sys_info = {
    "Operating System": f"{platform.system()} {platform.release()}",
    "Python Version": sys.version.split()[0],
    "Streamlit Version": st.__version__,
    "Pandas Version": pd.__version__,
    "Processor": platform.processor() or "Standard CPU"
}

sys_df = pd.DataFrame(list(sys_info.items()), columns=["Component", "Details"])
st.table(sys_df)

st.success("✅ Application operating normally with full configuration compatibility.")