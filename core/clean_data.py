import pandas as pd
import numpy as np

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows from DataFrame."""
    return df.drop_duplicates()

def handle_missing_values(df: pd.DataFrame, strategy="drop", numeric_fill=0, categorical_fill="Missing") -> pd.DataFrame:
    """Handles missing values based on chosen strategy."""
    df_clean = df.copy()
    if strategy == "drop":
        return df_clean.dropna()
    elif strategy == "fill":
        num_cols = df_clean.select_dtypes(include=[np.number]).columns
        cat_cols = df_clean.select_dtypes(include=['object', 'category']).columns
        df_clean[num_cols] = df_clean[num_cols].fillna(numeric_fill)
        df_clean[cat_cols] = df_clean[cat_cols].fillna(categorical_fill)
    return df_clean

def cap_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Caps numerical column outliers using Interquartile Range (IQR)."""
    df_clean = df.copy()
    if column in df_clean.columns and np.issubdtype(df_clean[column].dtype, np.number):
        Q1 = df_clean[column].quantile(0.25)
        Q3 = df_clean[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df_clean[column] = np.clip(df_clean[column], lower_bound, upper_bound)
    return df_clean