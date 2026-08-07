import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="DataPilot AI - Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# Sidebar Branding
with st.sidebar:
    try:
        st.image("assets/logo.png", use_container_width=True)
    except Exception:
        st.markdown("## 🧠 DataPilot AI")
    st.markdown("---")

# Header Title
st.markdown("<h2 style='color: #1E3A8A; font-weight: 800;'>📊 Executive Business Dashboard</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748B; margin-bottom: 25px;'>Interactive Power BI-style analytics engine with dynamic slicing & KPI monitoring.</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Dataset Verification
# ---------------------------------------------------------
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("⚠️ No active dataset found! Please upload a dataset first in the Upload section.")
    st.stop()

df = st.session_state["df"].copy()

# ---------------------------------------------------------
# 3. Dynamic Side Slicers (فلاتر جانبية تفاعلية على نمط Power BI)
# ---------------------------------------------------------
st.sidebar.markdown("### 🎛️ Executive Slicers & Filters")
st.sidebar.markdown("<small style='color: #64748B;'>Filter metrics across dimensions</small>", unsafe_allow_html=True)

# Identify Categorical Columns for Slicers
cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
num_cols = df.select_dtypes(include=['number']).columns.tolist()

filtered_df = df.copy()

if cat_cols:
    # Select top slicers (up to 4 categorical columns)
    slicer_cols = cat_cols[:4]
    
    for col in slicer_cols:
        unique_vals = df[col].dropna().unique().tolist()
        selected_vals = st.sidebar.multiselect(
            label=f"📌 Filter by {col}",
            options=unique_vals,
            default=unique_vals
        )
        if selected_vals:
            filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
else:
    st.sidebar.info("No categorical columns available for dynamic slicing.")

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered_df):,}** of **{len(df):,}** records")

# ---------------------------------------------------------
# 4. Executive KPI Scorecards Row
# ---------------------------------------------------------
st.markdown("### 📈 Key Performance Indicators (KPIs)")

kpi_cols = st.columns(4)

with kpi_cols[0]:
    st.metric(
        label="Total Records",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df):,} from total" if len(filtered_df) != len(df) else "All Data"
    )

with kpi_cols[1]:
    if num_cols:
        val1 = filtered_df[num_cols[0]].mean()
        st.metric(label=f"Avg {num_cols[0]}", value=f"{val1:,.1f}")
    else:
        st.metric(label="Metrics", value="N/A")

with kpi_cols[2]:
    if len(num_cols) > 1:
        val2 = filtered_df[num_cols[1]].sum()
        st.metric(label=f"Total {num_cols[1]}", value=f"{val2:,.0f}")
    else:
        st.metric(label="Secondary Metric", value="N/A")

with kpi_cols[3]:
    if len(cat_cols) > 0:
        top_cat = filtered_df[cat_cols[0]].mode()[0] if not filtered_df.empty else "N/A"
        st.metric(label=f"Top {cat_cols[0]}", value=str(top_cat))
    else:
        st.metric(label="Dominant Category", value="N/A")

st.divider()

# ---------------------------------------------------------
# 5. Interactive Charts Grid (Power BI Layout)
# ---------------------------------------------------------
st.markdown("### 📉 Executive Visual Breakdown")

if filtered_df.empty:
    st.error("No data available for the selected slicer filters!")
    st.stop()

row1_col1, row1_col2 = st.columns(2)

# --- Chart 1: Categorical Comparison Bar Chart ---
with row1_col1:
    if len(cat_cols) >= 1 and len(num_cols) >= 1:
        cat_target = cat_cols[0]
        num_target = num_cols[0]
        
        grouped = filtered_df.groupby(cat_target)[num_target].mean().reset_index()
        fig1 = px.bar(
            grouped,
            x=cat_target,
            y=num_target,
            title=f"<b>Average {num_target} by {cat_target}</b>",
            text_auto='.2s',
            color_discrete_sequence=['#3B82F6']
        )
        fig1.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Insufficient numeric/categorical columns for Bar Analytics.")

# --- Chart 2: Metric Distribution / Target vs Categorical ---
with row1_col2:
    if len(cat_cols) >= 2 and len(num_cols) >= 1:
        cat1 = cat_cols[0]
        cat2 = cat_cols[1] if len(cat_cols) > 1 else cat_cols[0]
        
        grouped2 = filtered_df.groupby([cat1, cat2]).size().reset_index(name='Count')
        fig2 = px.bar(
            grouped2,
            x=cat1,
            y='Count',
            color=cat2,
            barmode='group',
            title=f"<b>{cat1} Breakdown grouped by {cat2}</b>",
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig2.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)
    elif len(num_cols) >= 1:
        fig2 = px.histogram(
            filtered_df,
            x=num_cols[0],
            nbins=20,
            title=f"<b>Distribution of {num_cols[0]}</b>",
            color_discrete_sequence=['#8B5CF6']
        )
        fig2.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig2, use_container_width=True)

# --- Row 2 Visuals ---
row2_col1, row2_col2 = st.columns(2)

# --- Chart 3: Proportional Donut Chart ---
with row2_col1:
    if cat_cols:
        target_pie = cat_cols[0]
        pie_data = filtered_df[target_pie].value_counts().reset_index()
        pie_data.columns = [target_pie, 'Count']
        
        fig3 = px.pie(
            pie_data,
            names=target_pie,
            values='Count',
            hole=0.45,
            title=f"<b>Proportional Composition ({target_pie})</b>",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        fig3.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig3, use_container_width=True)

# --- Chart 4: Correlation / Trend Scatter ---
with row2_col2:
    if len(num_cols) >= 2:
        fig4 = px.scatter(
            filtered_df,
            x=num_cols[0],
            y=num_cols[1],
            color=cat_cols[0] if cat_cols else None,
            title=f"<b>{num_cols[0]} vs {num_cols[1]} Analysis</b>",
            opacity=0.8
        )
        fig4.update_layout(template="plotly_white", margin=dict(t=40, b=20, l=20, r=20))
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Need at least 2 numeric columns for Multi-Variable Scatter Analysis.")