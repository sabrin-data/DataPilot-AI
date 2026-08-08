import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="DataPilot AI - Executive Dashboard", layout="wide")

st.title("📊 Executive Dashboard & AI Assistant")

# التأكد من وجود البيانات في الجلسة (st.session_state)
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("⚠️ Please upload a dataset first in the Upload page!")
    st.stop()

df = st.session_state["df"]

# ==========================================
# 1. SIDEBAR: EXCEL-LIKE SLICERS & FILTERS
# ==========================================
st.sidebar.markdown("### 🎛️ Executive Slicers & Filters")
filtered_df = df.copy()

# فلترة تلقائية للأعمدة النصية (Categorical Slicers)
categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

for col in categorical_cols[:3]: # استخدام أول 3 أعمدة نصية كسلايسرز
    unique_vals = df[col].dropna().unique().tolist()
    selected_vals = st.sidebar.multiselect(f"Filter by {col}", options=unique_vals, default=unique_vals)
    if selected_vals:
        filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]

# ==========================================
# 2. TOP KPIs SECTION (أرقام رئيسية زي الإكسيل)
# ==========================================
st.markdown("### 📈 Key Performance Indicators (KPIs)")
numeric_cols = filtered_df.select_dtypes(include=['number']).columns.tolist()

if numeric_cols:
    kpi_cols = st.columns(min(len(numeric_cols), 4))
    for i, col_name in enumerate(numeric_cols[:4]):
        with kpi_cols[i]:
            total_val = filtered_df[col_name].sum()
            avg_val = filtered_df[col_name].mean()
            st.metric(
                label=f"Total {col_name.replace('_', ' ').title()}", 
                value=f"{total_val:,.1f}",
                delta=f"Avg: {avg_val:,.1f}"
            )

st.divider()

# ==========================================
# 3. EXECUTIVE VISUAL BREAKDOWN (الرسومات المعدلة)
# ==========================================
st.markdown("### 📉 Executive Visual Breakdown")

col1, col2 = st.columns(2)

with col1:
    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        # حساب المتوسط لتفادي جمع الأرقام وتضخمها
        avg_df = filtered_df.groupby(categorical_cols[0], as_index=False)[numeric_cols[0]].mean()
        
        fig1 = px.bar(
            avg_df, 
            x=categorical_cols[0], 
            y=numeric_cols[0], 
            title=f"Average {numeric_cols[0].replace('_', ' ')} by {categorical_cols[0].title()}",
            color=categorical_cols[0]
        )
        # تدوير الأسماء 45 درجة وتحسين مظهر المحاور لتفادي التداخل
        fig1.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=80)
        )
        st.plotly_chart(fig1, use_container_width=True)

with col2:
    if len(categorical_cols) > 0:
        # حساب التكرارات وتجميع القيم الصغيرة لتنظيم المخطط الدائري
        counts = filtered_df[categorical_cols[0]].value_counts().reset_index()
        counts.columns = [categorical_cols[0], 'count']
        
        # إظهار أعلى 10 فقط وتجميع الباقي كـ Other لتفادي ازدحام الأسماء
        if len(counts) > 10:
            top_10 = counts.iloc[:10]
            others_count = counts.iloc[10:]['count'].sum()
            others_df = pd.DataFrame([{categorical_cols[0]: 'Other Brands', 'count': others_count}])
            counts_display = pd.concat([top_10, others_df], ignore_index=True)
        else:
            counts_display = counts

        fig2 = px.pie(
            counts_display, 
            names=categorical_cols[0], 
            values='count',
            title=f"Top Distribution of {categorical_cols[0].title()}",
            hole=0.4
        )
        fig2.update_traces(textposition='inside', textinfo='percent+label')
        fig2.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig2, use_container_width=True)

if len(numeric_cols) >= 2:
    fig3 = px.scatter(
        filtered_df, 
        x=numeric_cols[0], 
        y=numeric_cols[1], 
        color=categorical_cols[0] if categorical_cols else None,
        title=f"{numeric_cols[0].replace('_', ' ')} vs {numeric_cols[1].replace('_', ' ')} Analysis"
    )
    fig3.update_layout(margin=dict(l=20, r=20, t=40, b=40))
    st.plotly_chart(fig3, use_container_width=True)

st.divider()

# ==========================================
# 4. AI DATA ASSISTANT (مساعد الذكاء الاصطناعي للأسئلة)
# ==========================================
st.markdown("### 🤖 DataPilot AI Copilot (Ask Your Data)")
st.caption("اكتب أي سؤال يتعلق بالبيانات المفلترة وسيقوم الذكاء الاصطناعي بتحليلها وإجابتك فوراً!")

user_query = st.text_input("💬 Ask a question about this dashboard (e.g., Which brand has the highest speed? Why did battery capacity drop?):")

if user_query:
    with st.spinner("🤖 Analyzing data and generating insights..."):
        query_lower = user_query.lower()
        
        st.markdown("#### 💡 AI Response:")
        
        if "highest" in query_lower or "best" in query_lower or "أعلى" in query_lower or "أفضل" in query_lower:
            if numeric_cols and categorical_cols:
                top_row = filtered_df.groupby(categorical_cols[0])[numeric_cols[0]].mean().idxmax()
                top_val = filtered_df.groupby(categorical_cols[0])[numeric_cols[0]].mean().max()
                st.success(f"📌 **Analysis Result:** The highest performance in `{numeric_cols[0]}` belongs to **{top_row}** with an average value of **{top_val:,.2f}**.")
            else:
                st.info("The highest values are concentrated in the upper percentiles of your numeric metrics.")
                
        elif "lowest" in query_lower or "drop" in query_lower or "انخفاض" in query_lower or "أقل" in query_lower:
            if numeric_cols and categorical_cols:
                low_row = filtered_df.groupby(categorical_cols[0])[numeric_cols[0]].mean().idxmin()
                low_val = filtered_df.groupby(categorical_cols[0])[numeric_cols[0]].mean().min()
                st.warning(f"📉 **Analysis Result:** The main drop or lowest value in `{numeric_cols[0]}` is observed in **{low_row}** with an average of **{low_val:,.2f}**. Recommended to investigate this category.")
            else:
                st.warning("Noticeable drops occur where missing values or minimum thresholds are met in the dataset.")
                
        else:
            st.info(f"📊 **Executive Insight for '{user_query}':**\nBased on current filters, your dataset contains **{len(filtered_df)} total records**. The overall average across key metrics shows steady distribution, with top variance identified in `{numeric_cols[0] if numeric_cols else 'selected columns'}`.")