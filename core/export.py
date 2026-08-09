import io
import zipfile
import pandas as pd

def export_to_zip(df: pd.DataFrame, file_name="Dataset") -> bytes:
    """Packages dataframe into a downloadable ZIP buffer."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
        csv_data = df.to_csv(index=False).encode('utf-8-sig')
        zf.writestr(f"{file_name}_cleaned.csv", csv_data)
    buffer.seek(0)
    return buffer.getvalue()