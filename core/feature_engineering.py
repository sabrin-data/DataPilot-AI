import pandas as pd

def encode_categorical(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """Applies One-Hot Encoding to selected categorical columns."""
    return pd.get_dummies(df, columns=columns, drop_first=True)

def scale_numerical(df: pd.DataFrame, columns: list, method="minmax") -> pd.DataFrame:
    """Scales numerical features using MinMax scaling."""
    df_scaled = df.copy()
    for col in columns:
        if col in df_scaled.columns:
            min_val = df_scaled[col].min()
            max_val = df_scaled[col].max()
            if max_val != min_val:
                df_scaled[col] = (df_scaled[col] - min_val) / (max_val - min_val)
    return df_scaled