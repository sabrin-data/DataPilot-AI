import streamlit as st
from utils.translations import init_language, t

# ==========================================
# 0. Page Configuration
# ==========================================
st.set_page_config(
    page_title="DataPilot AI - Home",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌐 1. Initialize Language & Sidebar Selector (يحتوي على اللوجو الموحد)
init_language()

# 🎨 2. Load Custom CSS from Assets
try:
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# 🔄 3. RTL Page Direction Handling (Dynamic based on selected language)
if st.session_state.get("lang") == "ar":
    st.markdown("""
        <style>
            .stApp {
                direction: RTL;
                text-align: right;
            }
            .cap-num {
                margin-right: 0px !important;
                margin-left: 10px !important;
            }
            .card-1, .card-2, .card-3, .card-4, .card-5, .card-6, .card-7, .card-8, .card-9 {
                border-left: none !important;
                border-right: 5px solid !important;
            }
            .card-1 { border-right-color: #3B82F6 !important; }
            .card-2 { border-right-color: #22C55E !important; }
            .card-3 { border-right-color: #EF4444 !important; }
            .card-4 { border-right-color: #F59E0B !important; }
            .card-5 { border-right-color: #8B5CF6 !important; }
            .card-6 { border-right-color: #06B6D4 !important; }
            .card-7 { border-right-color: #EC4899 !important; }
            .card-8 { border-right-color: #14B8A6 !important; }
            .card-9 { border-right-color: #A855F7 !important; }
        </style>
    """, unsafe_allow_html=True)

# Custom Styling with Colorful Modern UI & Sidebar Styling
st.markdown("""
    <style>
        /* 🎯 Sidebar Navigation Complete Bold Fix */
        [data-testid="stSidebarNav"] * {
            font-weight: 700 !important;
            color: #0F172A !important;
        }

        [data-testid="stSidebarNav"] a, 
        [data-testid="stSidebarNav"] a span,
        [data-testid="stSidebarNav"] li div span {
            font-weight: 700 !important;
            font-size: 15px !important;
            color: #0F172A !important;
        }

        [data-testid="stSidebarNav"] a[aria-current="page"],
        [data-testid="stSidebarNav"] a[aria-current="page"] span {
            font-weight: 900 !important;
            color: #2563EB !important;
            background-color: #E0E7FF !important;
            border-radius: 8px !important;
        }

        [data-testid="stSidebarNav"] a:hover span {
            color: #2563EB !important;
        }

        /* Modern Title Styling */
        .main-title {
            font-size: 40px;
            font-weight: 800;
            background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 50%, #8B5CF6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        .sub-title {
            font-size: 17px;
            color: #475569;
            margin-bottom: 25px;
            font-weight: 500;
        }
        
        /* General Card Base */
        .cap-card {
            border-radius: 16px;
            padding: 22px;
            height: 100%;
            margin-bottom: 20px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.6);
        }
        .cap-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
        }

        /* Specific Vibrant Card Color Gradients */
        .card-1 { background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); border-left: 5px solid #3B82F6; }
        .card-2 { background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%); border-left: 5px solid #22C55E; }
        .card-3 { background: linear-gradient(135deg, #FEF2F2 0%, #FEE2E2 100%); border-left: 5px solid #EF4444; }
        .card-4 { background: linear-gradient(135deg, #FFFBEB 0%, #FEF3C7 100%); border-left: 5px solid #F59E0B; }
        .card-5 { background: linear-gradient(135deg, #F5F3FF 0%, #EDE9FE 100%); border-left: 5px solid #8B5CF6; }
        .card-6 { background: linear-gradient(135deg, #ECFEFF 0%, #CFFAFE 100%); border-left: 5px solid #06B6D4; }
        .card-7 { background: linear-gradient(135deg, #FDF2F8 0%, #FCE7F3 100%); border-left: 5px solid #EC4899; }
        .card-8 { background: linear-gradient(135deg, #F0FDFA 0%, #CCFBF1 100%); border-left: 5px solid #14B8A6; }
        .card-9 { background: linear-gradient(135deg, #FAF5FF 0%, #F3E8FF 100%); border-left: 5px solid #A855F7; }

        /* Card Numbers & Headers */
        .cap-card h4 {
            margin-top: 0;
            margin-bottom: 12px;
            color: #1E293B;
            font-size: 18px;
            display: flex;
            align-items: center;
        }
        .cap-num {
            color: white;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 8px;
            margin-right: 10px;
            font-size: 14px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .num-1 { background-color: #3B82F6; }
        .num-2 { background-color: #22C55E; }
        .num-3 { background-color: #EF4444; }
        .num-4 { background-color: #F59E0B; }
        .num-5 { background-color: #8B5CF6; }
        .num-6 { background-color: #06B6D4; }
        .num-7 { background-color: #EC4899; }
        .num-8 { background-color: #14B8A6; }
        .num-9 { background-color: #A855F7; }

        .cap-card p {
            color: #334155;
            font-size: 14px;
            line-height: 1.5;
            margin: 0;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 🚀 Home / Landing Page Interface (مع اللوجو الرئيسي)
# ==========================================
head_col1, head_col2 = st.columns([1, 5])

with head_col1:
    try:
        st.image("assets/logo.png", width=110)
    except Exception:
        pass

with head_col2:
    st.markdown("<div class='main-title'>DataPilot AI</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='sub-title'>{t('sub_title') if t('sub_title') != 'sub_title' else 'An Enterprise-Grade Automated Data Sanitation, Profiling, Interactive Analytics, and AI Reporting Engine.'}</div>", unsafe_allow_html=True)

# Active File Banner
col_status, col_btn = st.columns([3, 1])

with col_status:
    if "df" in st.session_state and st.session_state["df"] is not None:
        file_name = st.session_state.get("file_name", "Dataset")
        df_shape = st.session_state["df"].shape
        st.success(f"📁 **Active Dataset:** {file_name} ({df_shape[0]:,} rows × {df_shape[1]} columns)")
    else:
        st.info(t("no_dataset") if t("no_dataset") != "no_dataset" else "📂 **No Active Dataset:** Upload a CSV or Excel file to begin analysis.")

with col_btn:
    if st.button("📌 Upload Dataset ➔", type="primary", use_container_width=True):
        st.switch_page("pages/2_Upload.py")

st.divider()

# Platform Capabilities & Data Pipeline Section
st.subheader("🎨 Explore Platform Modules & Pipeline")

# --- Row 1 (Steps 1, 2, 3) ---
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    <div class='cap-card card-1'>
        <h4><span class='cap-num num-1'>1</span> Upload & Inspect</h4>
        <p>Seamlessly ingest CSV and Excel files with automated encoding detection and structural verification.</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class='cap-card card-2'>
        <h4><span class='cap-num num-2'>2</span> Data Overview</h4>
        <p>Power BI-style diagnostics featuring a Data Health Score (0-100), quality metrics, and descriptive stats.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class='cap-card card-3'>
        <h4><span class='cap-num num-3'>3</span> Advanced Cleaning</h4>
        <p>8-phase comprehensive sanitation: text normalization, word mapping, currency parsing, and outlier caps.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Row 2 (Steps 4, 5, 6) ---
c4, c5, c6 = st.columns(3)
with c4:
    st.markdown("""
    <div class='cap-card card-4'>
        <h4><span class='cap-num num-4'>4</span> Feature Engineering</h4>
        <p>Perform feature scaling, categorical encoding, datetime extraction, and custom column engineering.</p>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class='cap-card card-5'>
        <h4><span class='cap-num num-5'>5</span> Exploratory Analysis</h4>
        <p>Uncover patterns, correlations, distributions, and multi-variable trends via interactive Plotly charts.</p>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
    <div class='cap-card card-6'>
        <h4><span class='cap-num num-6'>6</span> Interactive Dashboard</h4>
        <p>Dynamic executive scorecards, KPI filters, treemaps, and custom scatter matrices.</p>
    </div>
    """, unsafe_allow_html=True)

# --- Row 3 (Steps 7, 8, 9) ---
c7, c8, c9 = st.columns(3)
with c7:
    st.markdown("""
    <div class='cap-card card-7'>
        <h4><span class='cap-num num-7'>7</span> AI Machine Learning</h4>
        <p>Train automated ML models (Regression/Classification), analyze feature drivers, and run Isolation Forest anomaly detection.</p>
    </div>
    """, unsafe_allow_html=True)

with c8:
    st.markdown("""
    <div class='cap-card card-8'>
        <h4><span class='cap-num num-8'>8</span> Executive Report Generator</h4>
        <p>Compile dataset metrics, cleaning audit logs, and summary stats into printable HTML reports.</p>
    </div>
    """, unsafe_allow_html=True)

with c9:
    st.markdown("""
    <div class='cap-card card-9'>
        <h4><span class='cap-num num-9'>9</span> Project Bundle Export</h4>
        <p>Package all cleaned CSV/Excel files, audit text logs, and JSON schema metadata into a single ZIP file.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.info("👈 Use the navigation sidebar on the left to start exploring your dataset!")