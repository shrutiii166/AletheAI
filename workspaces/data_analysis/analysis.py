import pandas as pd
import plotly.express as px


def load_dataset(uploaded_file):
    """Load a CSV or Excel file into a DataFrame."""

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".csv"):
        try:
            return pd.read_csv(uploaded_file, encoding="utf-8")
        except UnicodeDecodeError:
            uploaded_file.seek(0)
            return pd.read_csv(uploaded_file, encoding="latin-1")

    elif file_name.endswith((".xlsx", ".xls")):
        return pd.read_excel(uploaded_file)

    else:
        raise ValueError("Unsupported file format. Upload CSV or Excel.")


def get_dataset_overview(df):
    """Generate a basic dataset overview."""

    return {
        "rows": df.shape[0],
        "columns": df.shape[1],
        "duplicates": int(df.duplicated().sum()),
        "missing_values": int(df.isnull().sum().sum()),
        "column_details": pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values,
            "Unique Values": df.nunique().values,
        }),
    }


def get_statistical_summary(df):
    """Generate descriptive statistics."""

    return df.describe(include="all").transpose()


def create_visualization(
    df,
    chart_type,
    x_column,
    y_column=None,
    color_column=None,
):
    """Generate an interactive Plotly visualization."""

    if x_column not in df.columns:
        raise ValueError("Select a valid X-axis column.")

    if y_column and y_column not in df.columns:
        raise ValueError("Select a valid Y-axis column.")

    if color_column and color_column not in df.columns:
        raise ValueError("Select a valid color column.")

    if chart_type == "Bar":
        if not y_column:
            raise ValueError("Bar charts require an X and Y column.")

        fig = px.bar(
            df, x=x_column, y=y_column, color=color_column,
            title=f"{y_column} by {x_column}",
        )

    elif chart_type == "Line":
        if not y_column:
            raise ValueError("Line charts require an X and Y column.")

        fig = px.line(
            df, x=x_column, y=y_column, color=color_column,
            title=f"{y_column} across {x_column}",
        )

    elif chart_type == "Scatter":
        if not y_column:
            raise ValueError("Scatter charts require an X and Y column.")

        fig = px.scatter(
            df, x=x_column, y=y_column, color=color_column,
            title=f"{y_column} vs {x_column}",
        )

    elif chart_type == "Histogram":
        fig = px.histogram(
            df, x=x_column, color=color_column,
            title=f"Distribution of {x_column}",
        )

    elif chart_type == "Box":
        if not pd.api.types.is_numeric_dtype(df[x_column]):
            raise ValueError("The Box plot's Y-axis must be numeric.")

        fig = px.box(
            df, y=x_column, x=y_column, color=color_column,
            title=f"Distribution of {x_column}",
        )

    elif chart_type == "Pie":
        if y_column:
            fig = px.pie(
                df, names=x_column, values=y_column,
                title=f"{y_column} by {x_column}",
            )
        else:
            counts = (
                df[x_column]
                .value_counts()
                .rename_axis(x_column)
                .reset_index(name="Count")
            )

            fig = px.pie(
                counts, names=x_column, values="Count",
                title=f"Distribution of {x_column}",
            )

    else:
        raise ValueError("Unsupported chart type.")

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
    )

    return fig