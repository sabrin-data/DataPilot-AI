import plotly.express as px

def build_histogram(df, column, n_bins=30):
    """Builds interactive Plotly histogram."""
    fig = px.histogram(df, x=column, nbins=n_bins, title=f"Distribution of {column}")
    fig.update_layout(template="plotly_white")
    return fig

def build_scatter_plot(df, x_col, y_col, color_col=None):
    """Builds interactive scatter plot."""
    fig = px.scatter(df, x=x_col, y=y_col, color=color_col, title=f"{x_col} vs {y_col}")
    fig.update_layout(template="plotly_white")
    return fig