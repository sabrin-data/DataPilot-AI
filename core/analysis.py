import pandas as pd

def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Generates comprehensive summary statistics."""
    if df is None or df.empty:
        return pd.DataFrame()
    return df.describe(include='all').T

def get_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Computes numeric correlation matrix."""
    numeric_df = df.select_dtypes(include=['number'])
    return numeric_df.corr()