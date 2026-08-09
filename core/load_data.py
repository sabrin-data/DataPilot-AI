import pandas as pd
import io

def load_dataset(uploaded_file) -> pd.DataFrame:
    """Reads uploaded CSV or Excel file and returns a Pandas DataFrame."""
    if uploaded_file is None:
        return None
    
    file_name = uploaded_file.name
    if file_name.endswith('.csv'):
        # Try different encodings
        try:
            return pd.read_csv(uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding='latin1')
    elif file_name.endswith(('.xls', '.xlsx')):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload CSV or Excel.")