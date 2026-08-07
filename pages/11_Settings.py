import streamlit as st
import sys
import platform
import pandas as pd

# ==========================================
# 0. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Application Settings",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ Application Settings & Configuration")
st.write("Manage app preferences, session cache, system diagnostics, and API keys.")

# ==========================================
# 1. App Preferences & UI Settings
# ==========================================
st.subheader("🎨 UI Preferences & Environment Settings")

col_set1, col_set2 = st.columns(2)

with col_set1:
    default_page_size = st.selectbox("Default Table Page Size", [10, 25, 50, 100], index=0)
    enable_notifications = st.toggle("Enable Toast Notifications", value=True)

with col_set2:
    precision = st.slider("Floating Point Display Precision", min_value=1, max_value=6, value=2)
    auto_refresh = st.toggle("Auto-Refresh Dashboard Widgets", value=False)

st.divider()

# ==========================================
# 🔑 Section 2: API Keys Management
# ==========================================
st.subheader("🔑 AI Service API Configurations")
st.write("Configure external LLM provider keys for automated AI insights.")

col_api1, col_api2 = st.columns(2)

with col_api1:
    openai_key = st.text_input("OpenAI API Key", type="password", help="Enter your sk-... key here for GPT integrations.")
    if st.button("Save OpenAI Key"):
        st.session_state["openai_key"] = openai_key
        st.success("OpenAI Key saved in session context!")

with col_api2:
    gemini_key = st.text_input("Google Gemini API Key", type="password", help="Enter your Gemini AI key here.")
    if st.button("Save Gemini Key"):
        st.session_state["gemini_key"] = gemini_key
        st.success("Gemini Key saved in session context!")

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
        st.warning("📂 No active dataset currently loaded in session state.")

with col_mem2:
    if st.button("🗑️ Clear Cache & Reset All Session Data", type="primary", use_container_width=True):
        st.session_state.clear()
        st.cache_data.clear()
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
    "Processor": platform.processor()
}

sys_df = pd.DataFrame(list(sys_info.items()), columns=["Component", "Details"])
st.table(sys_df)

st.success("✅ Application operating normally with full configuration compatibility.")