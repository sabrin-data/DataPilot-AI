from sklearn.ensemble import IsolationForest
import pandas as pd

def detect_anomalies(df: pd.DataFrame, contamination=0.05) -> pd.DataFrame:
    """Detects multi-dimensional anomalies using Isolation Forest."""
    df_res = df.copy()
    num_cols = df_res.select_dtypes(include=['number']).dropna().columns
    
    if len(num_cols) >= 2:
        iso_model = IsolationForest(contamination=contamination, random_state=42)
        preds = iso_model.fit_predict(df_res[num_cols].fillna(0))
        df_res["Anomaly_Score"] = preds
        df_res["Anomaly_Status"] = df_res["Anomaly_Score"].map({1: "Normal", -1: "Anomaly 🚨"})
    return df_res