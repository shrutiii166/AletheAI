import hashlib
import streamlit as st

from workspaces.data_analysis.analysis import (
    load_dataset,
    get_dataset_overview,
    get_statistical_summary,
    create_visualization,
)


def render_data_analysis_workspace():

    st.subheader("Data Analysis & Visualization")

    uploaded_file = st.file_uploader(
        "Upload a CSV or Excel dataset",
        type=["csv", "xlsx", "xls"],
        key="data_analysis_upload",
    )

    # Load the dataset when a new file is uploaded.
    if uploaded_file is not None:

        file_bytes = uploaded_file.getvalue()
        file_hash = hashlib.md5(file_bytes).hexdigest()

        if st.session_state.get("data_analysis_file_hash") != file_hash:

            try:
                uploaded_file.seek(0)
                df = load_dataset(uploaded_file)

                if df.empty:
                    st.warning("The uploaded dataset is empty.")
                    return

                st.session_state.data_analysis_df = df
                st.session_state.data_analysis_file_hash = file_hash
                st.session_state.data_analysis_file_name = uploaded_file.name

            except Exception as e:
                st.error(f"Unable to load dataset: {e}")
                return

    # Retrieve the loaded dataset.
    df = st.session_state.get("data_analysis_df")

    if df is None:
        st.info("Upload a CSV or Excel file to begin analysing your data.")
        return

    st.success(
        f"Loaded: {st.session_state.data_analysis_file_name}"
    )

    overview = get_dataset_overview(df)

    # Dataset metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", overview["rows"])
    col2.metric("Columns", overview["columns"])
    col3.metric("Missing Values", overview["missing_values"])
    col4.metric("Duplicates", overview["duplicates"])

    # Workspace sections
    overview_tab, statistics_tab, visualization_tab, preview_tab = st.tabs(
        ["Overview", "Statistics", "Visualizations", "Data Preview"]
    )

    with overview_tab:
        st.markdown("### Column Information")
        st.dataframe(
            overview["column_details"],
            use_container_width=True,
        )

    with statistics_tab:
        st.markdown("### Statistical Summary")
        st.dataframe(
            get_statistical_summary(df),
            use_container_width=True,
        )

    with visualization_tab:

        st.markdown("### Create a Visualization")

        chart_type = st.selectbox(
            "Chart Type",
            ["Bar", "Line", "Scatter", "Histogram", "Box", "Pie"],
        )

        columns = df.columns.tolist()

        x_column = st.selectbox(
            "X-axis / Category / Numeric Column",
            columns,
        )

        y_options = ["None"] + columns

        y_column = st.selectbox(
            "Y-axis / Values / Grouping Column",
            y_options,
        )

        color_column = st.selectbox(
            "Color Grouping (Optional)",
            ["None"] + columns,
        )

        if st.button("Generate Visualization"):

            try:
                fig = create_visualization(
                    df=df,
                    chart_type=chart_type,
                    x_column=x_column,
                    y_column=None if y_column == "None" else y_column,
                    color_column=(
                        None if color_column == "None" else color_column
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

            except Exception as e:
                st.error(f"Unable to generate chart: {e}")

    with preview_tab:
        st.markdown("### Dataset Preview")

        preview_rows = st.slider(
            "Number of rows to display",
            min_value=5,
            max_value=min(100, len(df)),
            value=min(10, len(df)),
        )

        st.dataframe(
            df.head(preview_rows),
            use_container_width=True,
        )