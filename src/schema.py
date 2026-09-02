import pandas as pd


def analyze_schema(df):
    """
    Analyze the structure of an uploaded dataset.
    """

    schema = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "numeric_columns": [],
        "text_columns": [],
        "date_columns": [],
        "missing_values": {},
    }

    for column in df.columns:

        # ------------------------------------------
        # Missing values
        # ------------------------------------------

        missing = int(df[column].isna().sum())

        if missing > 0:
            schema["missing_values"][column] = missing

        # ------------------------------------------
        # Numeric columns
        # ------------------------------------------

        if pd.api.types.is_numeric_dtype(df[column]):

            schema["numeric_columns"].append(column)

        else:

            # --------------------------------------
            # Try to detect date-like columns
            # --------------------------------------

            converted_dates = pd.to_datetime(
                df[column],
                errors="coerce"
            )

            valid_dates = converted_dates.notna().sum()

            total_values = df[column].notna().sum()

            if total_values > 0 and valid_dates / total_values >= 0.8:

                schema["date_columns"].append(column)

            else:

                schema["text_columns"].append(column)

    return schema