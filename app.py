import streamlit as st
import pandas as pd

from src.agent import run_agent
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
# Title
# --------------------------------------------------

st.title("🤖 AI Business Data Analyst")

st.write(
    "Upload your business data and ask questions using natural language."
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
    # Read CSV
    # --------------------------------------------------

    if uploaded_file.name.lower().endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    # --------------------------------------------------
    # Read Excel
    # --------------------------------------------------

    else:

        df = pd.read_excel(uploaded_file)


    st.success(
        f"✅ File uploaded successfully: {uploaded_file.name}"
    )


    # --------------------------------------------------
    # Data Preview
    # --------------------------------------------------

    st.subheader("📊 Data Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True
    )


    # --------------------------------------------------
    # Basic Dataset Information
    # --------------------------------------------------

    st.write(
        f"**Rows:** {len(df)}  |  "
        f"**Columns:** {len(df.columns)}"
    )


    # --------------------------------------------------
    # Schema Analysis
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

        st.write(schema["missing_values"])

    else:

        st.success(
            "✅ No missing values detected."
        )


    # --------------------------------------------------
    # Question Section
    # --------------------------------------------------

    st.subheader("💬 Ask Your Data")


    question = st.text_input(
        "Ask a question about your uploaded data",
        placeholder="Example: Which product sold the most?"
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