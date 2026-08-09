def generate_html_report(file_name: str, health_score: float, df_shape: tuple) -> str:
    """Generates an HTML string report for data analytics summary."""
    html_content = f"""
    <html>
        <head><title>Data Analysis Report - {file_name}</title></head>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h1>📊 Data Quality & Analysis Report</h1>
            <hr>
            <p><strong>Dataset Name:</strong> {file_name}</p>
            <p><strong>Total Rows:</strong> {df_shape[0]}</p>
            <p><strong>Total Columns:</strong> {df_shape[1]}</p>
            <p><strong>Health Score:</strong> {health_score} / 100</p>
        </body>
    </html>
    """
    return html_content