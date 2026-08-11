import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, IsolationForest
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.metrics import r2_score, mean_squared_error, accuracy_score, f1_score
from sklearn.preprocessing import LabelEncoder
from utils.translations import init_language, t

# ==========================================
# 0. Page Configuration & Language Init
# ==========================================
st.set_page_config(
    page_title="AI & Machine Learning Insights Studio",
    page_icon="🤖",
    layout="wide"
)

# تفعيل تهيئة اللغة
init_language()

# قراءة الـ CSS الموحد
try:
    with open("assets/style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

st.title("🤖 AI & Machine Learning Insights Studio")
st.write("Train predictive Machine Learning models, analyze feature importance, and detect statistical anomalies automatically.")

# ==========================================
# 1. Check Dataset Availability
# ==========================================
if "df" not in st.session_state or st.session_state["df"] is None:
    st.warning("⚠️ Please upload a dataset first in the Upload page!")
    st.stop()

df = st.session_state["df"].copy()
file_name = st.session_state.get("file_name", "Dataset")

st.info(f"📁 Active Dataset: **{file_name}** | Dimensions: **{df.shape[0]:,} rows × {df.shape[1]} cols**")
st.divider()

# Classify attributes
num_cols = df.select_dtypes(include=np.number).columns.tolist()
cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()
all_cols = df.columns.tolist()

# Prepare Tabs
tab_ml, tab_anomalies = st.tabs(["🎯 Automated Predictive Machine Learning", "🚨 Isolation Forest Anomaly Detection"])

# ==========================================
# 🎯 TAB 1: Predictive Machine Learning
# ==========================================
with tab_ml:
    st.subheader("🎯 Predictive Modeling & Feature Importance")
    
    col_setup1, col_setup2, col_setup3 = st.columns(3)
    
    with col_setup1:
        target_var = st.selectbox("Select Target Variable (Y)", all_cols, index=len(all_cols)-1, key="target_select")
    
    # Determine task type (Regression vs Classification)
    is_numeric_target = target_var in num_cols
    unique_target_count = df[target_var].nunique()
    
    if is_numeric_target and unique_target_count > 10:
        default_task = "Regression"
    else:
        default_task = "Classification"

    with col_setup2:
        task_type = st.radio("Task Type Detected", ["Regression", "Classification"], index=0 if default_task == "Regression" else 1, key="task_radio")
        
    with col_setup3:
        if task_type == "Regression":
            model_name = st.selectbox("Select Algorithm", ["Random Forest Regressor", "Linear Regression", "Decision Tree Regressor"], key="algo_reg")
        else:
            model_name = st.selectbox("Select Algorithm", ["Random Forest Classifier", "Logistic Regression", "Decision Tree Classifier"], key="algo_clf")

    # Predictors Selection
    available_features = [c for c in all_cols if c != target_var]
    selected_features = st.multiselect("Select Feature Predictors (X)", available_features, default=available_features, key="features_select")

    if st.button("🚀 Train Machine Learning Model", type="primary", use_container_width=True):
        if not selected_features:
            st.error("Please select at least one feature for prediction.")
        else:
            with st.spinner("Training model and processing encodings..."):
                # Data Preparation & Preprocessing
                ml_df = df[[target_var] + selected_features].dropna(subset=[target_var]).copy()
                
                encoders = {}

                # Clean & Encode Features in X
                for col in selected_features:
                    if pd.api.types.is_object_dtype(ml_df[col]) or pd.api.types.is_categorical_dtype(ml_df[col]) or pd.api.types.is_string_dtype(ml_df[col]):
                        fill_val = ml_df[col].mode()[0] if not ml_df[col].mode().empty else "Missing"
                        ml_df[col] = ml_df[col].fillna(fill_val).astype(str)
                        
                        le = LabelEncoder()
                        ml_df[col] = le.fit_transform(ml_df[col])
                        encoders[col] = le
                    else:
                        ml_df[col] = pd.to_numeric(ml_df[col], errors='coerce')
                        mean_val = ml_df[col].mean()
                        ml_df[col] = ml_df[col].fillna(mean_val if not pd.isna(mean_val) else 0)

                # Target Variable Encoding for Classification
                if task_type == "Classification":
                    if pd.api.types.is_object_dtype(ml_df[target_var]) or pd.api.types.is_categorical_dtype(ml_df[target_var]) or pd.api.types.is_string_dtype(ml_df[target_var]):
                        target_le = LabelEncoder()
                        ml_df[target_var] = target_le.fit_transform(ml_df[target_var].astype(str))
                        encoders[target_var] = target_le

                X = ml_df[selected_features]
                y = ml_df[target_var]

                if len(X) < 5:
                    st.error("Dataset has too few rows after cleaning missing values. Please clean data or select different features.")
                    st.stop()

                # Train / Test Split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

                # Instantiate Model
                if task_type == "Regression":
                    if model_name == "Random Forest Regressor":
                        model = RandomForestRegressor(n_estimators=100, random_state=42)
                    elif model_name == "Linear Regression":
                        model = LinearRegression()
                    else:
                        model = DecisionTreeRegressor(random_state=42)
                else:
                    if model_name == "Random Forest Classifier":
                        model = RandomForestClassifier(n_estimators=100, random_state=42)
                    elif model_name == "Logistic Regression":
                        model = LogisticRegression(max_iter=1000)
                    else:
                        model = DecisionTreeClassifier(random_state=42)

                # Fit Model
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)

                # Save trained parameters and metrics to session state
                st.session_state["trained_model"] = model
                st.session_state["model_features"] = selected_features
                st.session_state["encoders"] = encoders
                st.session_state["task_type"] = task_type
                st.session_state["target_var"] = target_var
                st.session_state["y_test"] = y_test
                st.session_state["y_pred"] = y_pred

                st.success("✅ Model Training & Evaluation Complete!")

    # Display Results if model exists in session state
    if "trained_model" in st.session_state:
        model = st.session_state["trained_model"]
        selected_features = st.session_state["model_features"]
        task_type = st.session_state["task_type"]
        y_test = st.session_state["y_test"]
        y_pred = st.session_state["y_pred"]
        
        st.divider()
        st.subheader("📊 Model Performance Evaluation")
        m1, m2, m3 = st.columns(3)

        if task_type == "Regression":
            r2 = r2_score(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            mae = np.mean(np.abs(y_test - y_pred))

            m1.metric("R² Score (Accuracy)", f"{r2:.3f}")
            m2.metric("Root Mean Squared Error (RMSE)", f"{rmse:.3f}")
            m3.metric("Mean Absolute Error (MAE)", f"{mae:.3f}")

            # Actual vs Predicted Plot
            fig_res = px.scatter(x=y_test, y=y_pred, labels={'x': 'Actual Values', 'y': 'Predicted Values'}, title="Actual vs. Predicted Values")
            fig_res.add_trace(go.Scatter(x=[y_test.min(), y_test.max()], y=[y_test.min(), y_test.max()], mode='lines', name='Perfect Fit', line=dict(color='red', dash='dash')))
            st.plotly_chart(fig_res, use_container_width=True)

        else:
            acc = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred, average="weighted")
            
            m1.metric("Model Accuracy", f"{acc * 100:.2f}%")
            m2.metric("Weighted F1-Score", f"{f1:.3f}")
            m3.metric("Test Dataset Count", f"{len(y_test):,}")

        # Feature Importance Plot
        if hasattr(model, "feature_importances_"):
            st.divider()
            st.subheader("💡 Feature Importance Analysis")
            importance_df = pd.DataFrame({
                "Feature": selected_features,
                "Importance": model.feature_importances_
            }).sort_values(by="Importance", ascending=True)

            fig_imp = px.bar(importance_df, x="Importance", y="Feature", orientation="h", title="Top Drivers & Feature Importance", color="Importance", color_continuous_scale="Blues")
            st.plotly_chart(fig_imp, use_container_width=True)

        # Interactive Prediction Playground
        st.divider()
        st.subheader("🎮 Live Prediction Playground")
        st.write("Input custom values to generate real-time AI predictions:")
        
        inputs = {}
        play_cols = st.columns(min(4, len(st.session_state["model_features"])))
        
        for idx, feat in enumerate(st.session_state["model_features"]):
            with play_cols[idx % len(play_cols)]:
                if feat in st.session_state["encoders"]:
                    classes = list(st.session_state["encoders"][feat].classes_)
                    val = st.selectbox(f"{feat}", classes, key=f"play_{feat}")
                    inputs[feat] = st.session_state["encoders"][feat].transform([val])[0]
                else:
                    mean_val = df[feat].mean() if pd.api.types.is_numeric_dtype(df[feat]) else 0.0
                    val = st.number_input(f"{feat}", value=float(mean_val if not pd.isna(mean_val) else 0.0), key=f"play_{feat}")
                    inputs[feat] = val

        if st.button("🔮 Generate Prediction", type="secondary"):
            input_df = pd.DataFrame([inputs])
            pred_val = st.session_state["trained_model"].predict(input_df)[0]
            
            if st.session_state["task_type"] == "Classification" and st.session_state["target_var"] in st.session_state["encoders"]:
                pred_val = st.session_state["encoders"][st.session_state["target_var"]].inverse_transform([int(pred_val)])[0]
            
            st.success(f"🎯 **Predicted Result for {st.session_state['target_var']}:** `{pred_val}`")

# ==========================================
# 🚨 TAB 2: Isolation Forest Anomaly Detection
# ==========================================
with tab_anomalies:
    st.subheader("🚨 Machine Learning Anomaly Detection (Isolation Forest)")
    st.write("Automatically identify multidimensional statistical anomalies and outliers in your numerical attributes.")

    if len(num_cols) >= 2:
        anom_cols = st.multiselect("Select Numerical Attributes for Anomaly Scanning", num_cols, default=num_cols[:min(4, len(num_cols))], key="anom_cols_select")
        contamination_rate = st.slider("Expected Anomaly Contamination Rate (%)", min_value=1, max_value=15, value=5, key="contam_slider") / 100.0

        if st.button("🔍 Detect Anomalies", type="primary"):
            anom_df = df[anom_cols].dropna().copy()
            
            if len(anom_df) > 0:
                iso_model = IsolationForest(contamination=contamination_rate, random_state=42)
                preds = iso_model.fit_predict(anom_df)
                
                anom_df["Anomaly_Status"] = np.where(preds == -1, "Anomaly 🚨", "Normal ✅")
                
                anom_count = (preds == -1).sum()
                st.warning(f"🚨 **Detected {anom_count:,} Anomalies** out of **{len(anom_df):,}** total records ({anom_count/len(anom_df)*100:.2f}%).")

                # 2D Visualizer
                if len(anom_cols) >= 2:
                    fig_anom = px.scatter(
                        anom_df, 
                        x=anom_cols[0], 
                        y=anom_cols[1], 
                        color="Anomaly_Status",
                        color_discrete_map={"Normal ✅": "#1f77b4", "Anomaly 🚨": "#d62728"},
                        title=f"Multidimensional Anomalies: {anom_cols[0]} vs {anom_cols[1]}"
                    )
                    st.plotly_chart(fig_anom, use_container_width=True)

                # Preview Anomalies Table
                st.markdown("##### **Detected Anomaly Records Preview**")
                st.dataframe(anom_df[anom_df["Anomaly_Status"] == "Anomaly 🚨"], use_container_width=True)
            else:
                st.error("No valid data points found after dropping missing values.")
    else:
        st.info("At least two numerical columns are required for multidimensional anomaly detection.")

st.divider()

# Transition Button
col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
with col_b2:
    if st.button("Proceed to Executive Report Generator ➔", type="primary", use_container_width=True):
        st.switch_page("pages/9_Report_Generator.py")