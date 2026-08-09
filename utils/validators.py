import pandas as pd

def validate_dataframe(df: pd.DataFrame) -> tuple[bool, str]:
    """
    Validates uploaded DataFrame structure and content.
    Returns (is_valid, error_message).
    """
    if df is None:
        return False, "Dataset is null or unreadable."
    
    if df.empty:
        return False, "Uploaded file contains an empty dataset (0 rows)."
    
    if df.shape[1] == 0:
        return False, "Dataset does not contain any valid columns."
        
    return True, "Dataset passed validation checks."