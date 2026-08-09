import pandas as pd
import numpy as np

def calculate_health_score(df: pd.DataFrame) -> float:
    """
    Calculates an overall data health score out of 100
    based on missing values and row duplicates.
    """
    if df is None or df.empty:
        return 0.0

    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()
    
    # Missing value impact (70% weight)
    missing_score = max(0, 100 - (missing_cells / total_cells * 100))
    
    # Duplicates impact (30% weight)
    dup_score = max(0, 100 - (duplicate_rows / len(df) * 100)) if len(df) > 0 else 100
    
    overall_score = (missing_score * 0.7) + (dup_score * 0.3)
    return round(overall_score, 1)

def format_bytes(size_in_bytes: int) -> str:
    """Converts bytes to human-readable memory format (KB, MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024.0:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} TB"