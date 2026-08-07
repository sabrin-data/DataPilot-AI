import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 0. Page Configuration
# ==========================================
st.set_page_config(
    page_title="Exploratory Data Analysis",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Exploratory Data Analysis (EDA) Studio")
st.write("Interactive statistical analysis, dynamic visual relationship discovery, and automated data insights.")

# ==========================================
# 1. Check Dataset Availability
# ==========================================
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("📂 Please upload a dataset first from the Upload page.")
    st.stop()

df = st.session_state["df"]
file_name = st.session_state.get("file_name", "Dataset")

st.info(f"📁 Active Dataset: **{file_name}** | Dimensions: **{df.shape[0]:,} rows × {df.shape[1]} columns**")
st.divider()

# Classify columns
num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
dt_cols = df.select_dtypes(include=["datetime", "datetimetz"]).columns.tolist()

# ==========================================
# 📊 Section 1: Univariate Analysis
# ==========================================
with st.expander("📊 Section 1: Single Variable Analysis (Univariate Analysis)", expanded=True):
    uni_tab1, uni_tab2 = st.tabs(["🔢 Numerical Variables", "📝 Categorical Variables"])

    # 1. Numerical Analysis
    with uni_tab1:
        if num_cols:
            u_col1, u_col2 = st.columns([1, 2])
            with u_col1:
                selected_num = st.selectbox("Select Numeric Variable", num_cols, key="uni_num")
                
                # Statistics Summary Box
                st.markdown("##### **Statistical Snapshot**")
                s_mean = df[selected_num].mean()
                s_std = df[selected_num].std()
                s_median = df[selected_num].median()
                s_skew = df[selected_num].skew()

                st.write(f"• **Mean:** `{s_mean:.2f}`")
                st.write(f"• **Std Dev:** `{s_std:.2f}`")
                st.write(f"• **Median:** `{s_median:.2f}`")
                st.write(f"• **Skewness:** `{s_skew:.2f}` ({'Right-skewed' if s_skew > 0.5 else 'Left-skewed' if s_skew < -0.5 else 'Symmetric'})")

            with u_col2:
                plot_type = st.radio("Distribution Plot Type", ["Histogram + Boxplot", "Density KDE", "Violin Plot"], horizontal=True)
                if plot_type == "Histogram + Boxplot":
                    fig_uni = px.histogram(df, x=selected_num, marginal="box", title=f"Distribution of {selected_num}", color_discrete_sequence=['#3366CC'])
                elif plot_type == "Density KDE":
                    fig_uni = px.histogram(df, x=selected_num, histnorm='probability density', title=f"Density Plot of {selected_num}", color_discrete_sequence=['#00CC96'])
                else:
                    fig_uni = px.violin(df, y=selected_num, box=True, points="all", title=f"Violin Plot of {selected_num}", color_discrete_sequence=['#AB63FA'])
                
                st.plotly_chart(fig_uni, use_container_width=True)
        else:
            st.info("No numerical variables found for univariate analysis.")

    # 2. Categorical Analysis
    with uni_tab2:
        if cat_cols:
            c_col1, c_col2 = st.columns([1, 2])
            with c_col1:
                selected_cat = st.selectbox("Select Categorical Variable", cat_cols, key="uni_cat")
                top_n = st.slider("Top N Categories to Display", min_value=3, max_value=30, value=10)
                
                val_counts = df[selected_cat].value_counts().head(top_n)
                st.markdown("##### **Value Counts Preview**")
                st.dataframe(val_counts)

            with c_col2:
                cat_chart_type = st.radio("Chart Type", ["Bar Chart", "Pie Chart", "Donut Chart"], horizontal=True)
                if cat_chart_type == "Bar Chart":
                    fig_cat = px.bar(x=val_counts.index, y=val_counts.values, labels={'x': selected_cat, 'y': 'Count'}, title=f"Top {top_n} Categories in {selected_cat}", color_discrete_sequence=['#FF6692'])
                elif cat_chart_type == "Pie Chart":
                    fig_cat = px.pie(names=val_counts.index, values=val_counts.values, title=f"Category Ratio for {selected_cat}")
                else:
                    fig_cat = px.pie(names=val_counts.index, values=val_counts.values, hole=0.5, title=f"Category Ratio for {selected_cat}")
                
                st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("No categorical variables found for univariate analysis.")

# ==========================================
# 📈 Section 2: Bivariate & Relationship Analysis
# ==========================================
with st.expander("📈 Section 2: Multi-Variable Relationship Analysis", expanded=False):
    bi_tab1, bi_tab2, bi_tab3 = st.tabs(["🔵 Scatter / Line Plots", "📦 Numeric vs Categorical", "🔥 Correlation Matrix"])

    # 1. Scatter / Line
    with bi_tab1:
        if len(num_cols) >= 2:
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                x_var = st.selectbox("X-Axis Variable", num_cols, key="sc_x")
            with sc2:
                y_var = st.selectbox("Y-Axis Variable", [c for c in num_cols if c != x_var], key="sc_y")
            with sc3:
                color_var = st.selectbox("Color Grouping (Optional)", ["None"] + cat_cols, key="sc_color")

            color_val = None if color_var == "None" else color_var
            fig_scatter = px.scatter(df, x=x_var, y=y_var, color=color_val, trendline="ols", title=f"Relationship: {x_var} vs {y_var}")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("At least two numerical variables are required for scatter plotting.")

    # 2. Boxplot by Categories
    with bi_tab2:
        if num_cols and cat_cols:
            bx1, bx2 = st.columns(2)
            with bx1:
                box_num = st.selectbox("Select Numerical Metric", num_cols, key="bx_num")
            with bx2:
                box_cat = st.selectbox("Select Categorical Grouping", cat_cols, key="bx_cat")

            fig_box = px.box(df, x=box_cat, y=box_num, color=box_cat, title=f"Distribution of {box_num} grouped by {box_cat}")
            st.plotly_chart(fig_box, use_container_width=True)
        else:
            st.info("Requires at least one numerical and one categorical variable.")

    # 3. Correlation Matrix Heatmap
    with bi_tab3:
        if len(num_cols) >= 2:
            corr_matrix = df[num_cols].corr()
            fig_corr = px.imshow(
                corr_matrix, 
                text_auto=".2f", 
                aspect="auto", 
                color_continuous_scale="RdBu_r",
                title="Full Numeric Attribute Correlation Heatmap"
            )
            st.plotly_chart(fig_corr, use_container_width=True)
        else:
            st.info("At least two numerical attributes are required to calculate correlations.")

# ==========================================
# 🧩 Section 3: Interactive GroupBy & Aggregations
# ==========================================
with st.expander("🧩 Section 3: Custom Data Aggregation & Pivot Table Builder", expanded=False):
    if cat_cols and num_cols:
        ag1, ag2, ag3 = st.columns(3)
        with ag1:
            group_by_cols = st.multiselect("Group By Category(ies)", cat_cols, default=[cat_cols[0]])
        with ag2:
            agg_num_cols = st.multiselect("Target Numeric Metrics", num_cols, default=[num_cols[0]])
        with ag3:
            agg_func = st.selectbox("Aggregation Function", ["mean", "sum", "count", "min", "max", "std"])

        if group_by_cols and agg_num_cols:
            agg_result = df.groupby(group_by_cols)[agg_num_cols].agg(agg_func).reset_index()
            st.markdown(f"##### **Aggregated Summary Table ({agg_func.upper()})**")
            st.dataframe(agg_result, use_container_width=True)
            
            # Download Aggregated Result
            st.download_button(
                "⬇️ Download Aggregated Data (CSV)",
                data=agg_result.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"aggregated_{agg_func}_summary.csv",
                mime="text/csv"
            )
    else:
        st.info("Requires both categorical and numerical columns for GroupBy analysis.")

# ==========================================
# 💡 Section 4: Automated Smart EDA Insights
# ==========================================
with st.expander("💡 Section 4: Automated AI EDA Insights", expanded=True):
    st.subheader("💡 Key Statistical Insights & Correlation Findings")
    
    insights = []
    if len(num_cols) >= 2:
        corr = df[num_cols].corr().abs()
        np.fill_diagonal(corr.values, 0)
        max_corr_pair = corr.unstack().idxmax()
        max_corr_val = corr.unstack().max()
        
        if max_corr_val > 0.6:
            insights.append(f"🔗 **Strong Correlation Detected:** `{max_corr_pair[0]}` and `{max_corr_pair[1]}` have a high correlation coefficient of **{max_corr_val:.2f}**.")

    for col in num_cols:
        skew_val = df[col].skew()
        if abs(skew_val) > 1.5:
            insights.append(f"⚠️ **High Skewness:** Column `{col}` is heavily skewed (Skewness = **{skew_val:.2f}**). Consider applying a Log transformation.")

    if not insights:
        insights.append("✅ No extreme anomalies or dominant strong correlations detected in the current numeric attributes.")

    for ins in insights:
        st.info(ins)

st.divider()

# Transition Button
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    if st.button("Proceed to Interactive Dashboard Studio ➔", type="primary", use_container_width=True):
        st.switch_page("pages/7_Dashboard.py")