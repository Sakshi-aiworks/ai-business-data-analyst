import streamlit as st
import pandas as pd

from src.agent import run_agent

from src.analysis import (
    total_sales,
    total_profit,
    top_product,
    sales_by_region,
    sales_by_product,
    sales_over_time,
)

from src.schema import analyze_schema


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="AI Business Data Analyst",
    page_icon="🤖",
    layout="wide"
)


# --------------------------------------------------
# Application Header
# --------------------------------------------------

st.title("🤖 AI Business Data Analyst")

st.write(
    "Upload your business data and ask questions "
    "using natural language."
)


# --------------------------------------------------
# File Upload
# --------------------------------------------------

uploaded_file = st.file_uploader(
    "📁 Upload your business file",
    type=["csv", "xlsx"]
)


if uploaded_file is not None:

    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------

    try:

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"✅ File uploaded successfully: "
            f"{uploaded_file.name}"
        )

    except Exception as e:

        st.error(
            f"❌ Could not read the uploaded file: {e}"
        )

        st.stop()


    # --------------------------------------------------
    # Data Preview
    # --------------------------------------------------

    st.subheader("📊 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.write(
        f"**Rows:** {len(df)}  |  "
        f"**Columns:** {len(df.columns)}"
    )


    # --------------------------------------------------
    # Business KPIs
    # --------------------------------------------------

    st.subheader("📈 Business KPIs")

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)


    # Total Sales
    with kpi1:

        try:

            sales = total_sales(df)

            st.metric(
                "Total Sales",
                sales
            )

        except Exception:

            st.metric(
                "Total Sales",
                "Unavailable"
            )


    # Total Profit
    with kpi2:

        try:

            profit = total_profit(df)

            st.metric(
                "Total Profit",
                profit
            )

        except Exception:

            st.metric(
                "Total Profit",
                "Unavailable"
            )


    # Top Product
    with kpi3:

        try:

            product = top_product(df)

            st.metric(
                "Top Product",
                product
            )

        except Exception:

            st.metric(
                "Top Product",
                "Unavailable"
            )


    # Top Region
    with kpi4:

        try:

            region_data = sales_by_region(df)

            top_region = region_data.idxmax()

            st.metric(
                "Top Region",
                top_region
            )

        except Exception:

            st.metric(
                "Top Region",
                "Unavailable"
            )


    # --------------------------------------------------
    # Business Charts
    # --------------------------------------------------

    st.subheader("📊 Business Insights")

    chart_col1, chart_col2 = st.columns(2)


    # --------------------------------------------------
    # Sales by Region
    # --------------------------------------------------

    with chart_col1:

        st.write("### 🌍 Sales by Region")

        try:

            region_data = sales_by_region(df)

            region_chart = region_data.sort_values(
                ascending=False
            )

            st.bar_chart(
                region_chart
            )

        except Exception:

            st.info(
                "Regional sales data is not available."
            )


    # --------------------------------------------------
    # Sales by Product
    # --------------------------------------------------

    with chart_col2:

        st.write("### 📦 Sales by Product")

        try:

            product_data = sales_by_product(df)

            product_chart = product_data.sort_values(
                ascending=False
            )

            st.bar_chart(
                product_chart
            )

        except Exception:

            st.info(
                "Product sales data is not available."
            )


    # --------------------------------------------------
    # Sales Trend
    # --------------------------------------------------

    st.write("### 📈 Sales Trend")

    try:

        trend_data = sales_over_time(df)

        st.line_chart(
            trend_data
        )

    except Exception:

        st.info(
            "📅 Sales trend is not available because "
            "the dataset does not contain usable date "
            "and sales information."
        )


    # --------------------------------------------------
    # Dataset Schema
    # --------------------------------------------------

    schema = analyze_schema(df)

    st.subheader("🔍 Dataset Information")

    col1, col2 = st.columns(2)


    with col1:

        st.write(
            f"**Rows:** {schema['rows']}"
        )

        st.write(
            f"**Columns:** {schema['columns']}"
        )

        st.write(
            f"**Numeric columns:** "
            f"{', '.join(schema['numeric_columns']) or 'None'}"
        )


    with col2:

        st.write(
            f"**Text columns:** "
            f"{', '.join(schema['text_columns']) or 'None'}"
        )

        st.write(
            f"**Date columns:** "
            f"{', '.join(schema['date_columns']) or 'None'}"
        )


    # --------------------------------------------------
    # Available Columns
    # --------------------------------------------------

    st.write(
        f"**Available columns:** "
        f"{', '.join(schema['column_names'])}"
    )


    # --------------------------------------------------
    # Missing Values
    # --------------------------------------------------

    if schema["missing_values"]:

        st.warning(
            "⚠️ Some columns contain missing values."
        )

        st.write(
            schema["missing_values"]
        )

    else:

        st.success(
            "✅ No missing values detected."
        )


    # --------------------------------------------------
    # AI Data Analyst
    # --------------------------------------------------

    st.subheader("💬 Ask Your Data")

    question = st.text_input(
        "Ask a question about your uploaded data",
        placeholder=(
            "Example: Which product sold the most?"
        )
    )


    # --------------------------------------------------
    # Ask AI
    # --------------------------------------------------

    if st.button("🤖 Ask AI"):

        if question.strip():

            with st.spinner(
                "🔄 AI is analyzing your data..."
            ):

                try:

                    answer = run_agent(
                        df,
                        question
                    )

                    st.subheader("🤖 AI Answer")

                    st.write(answer)

                except Exception as e:

                    st.error(
                        f"❌ Something went wrong: {e}"
                    )

        else:

            st.warning(
                "⚠️ Please enter a question first."
            )