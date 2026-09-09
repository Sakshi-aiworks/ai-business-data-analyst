import pandas as pd


# ==================================================
# EXISTING BUSINESS ANALYSIS FUNCTIONS
# ==================================================


def total_sales(df):
    """Calculate total sales."""

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return df["Sales"].sum()


def total_profit(df):
    """Calculate total profit."""

    if "Profit" not in df.columns:
        raise ValueError("Profit column is not available.")

    return df["Profit"].sum()


def top_product(df):
    """Find the product with the highest total sales."""

    if "Product" not in df.columns:
        raise ValueError("Product column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
    )

    return product_sales.idxmax()


def sales_by_region(df):
    """Calculate total sales grouped by region."""

    if "Region" not in df.columns:
        raise ValueError("Region column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


def sales_by_product(df):
    """Calculate total sales grouped by product."""

    if "Product" not in df.columns:
        raise ValueError("Product column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


def sales_over_time(df):
    """Calculate total sales over time."""

    if "Date" not in df.columns:
        raise ValueError("Date column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    data = df.copy()

    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    data = data.dropna(
        subset=["Date"]
    )

    if data.empty:
        raise ValueError(
            "No valid dates found."
        )

    return (
        data.groupby("Date")["Sales"]
        .sum()
        .sort_index()
    )


# ==================================================
# GENERIC DATA ANALYSIS FUNCTIONS
# ==================================================


def numeric_columns(df):
    """
    Return all numeric columns in the dataset.
    """

    return df.select_dtypes(
        include="number"
    ).columns.tolist()


def text_columns(df):
    """
    Return all text/object columns in the dataset.
    """

    return df.select_dtypes(
        include=["object", "string", "category"]
    ).columns.tolist()


def calculate_sum(df, column):
    """
    Calculate the sum of any numeric column.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' is not available."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return df[column].sum()


def calculate_average(df, column):
    """
    Calculate the average of any numeric column.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' is not available."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return df[column].mean()


def calculate_min(df, column):
    """
    Find the minimum value of a numeric column.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' is not available."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return df[column].min()


def calculate_max(df, column):
    """
    Find the maximum value of a numeric column.
    """

    if column not in df.columns:
        raise ValueError(
            f"Column '{column}' is not available."
        )

    if not pd.api.types.is_numeric_dtype(
        df[column]
    ):
        raise ValueError(
            f"Column '{column}' is not numeric."
        )

    return df[column].max()


def group_by_column(df, group_column, value_column):
    """
    Group data by one column and calculate
    the sum of another numeric column.

    Example:

    Customer -> Revenue

    Customer A -> 100000
    Customer B -> 150000
    """

    if group_column not in df.columns:
        raise ValueError(
            f"Column '{group_column}' is not available."
        )

    if value_column not in df.columns:
        raise ValueError(
            f"Column '{value_column}' is not available."
        )

    if not pd.api.types.is_numeric_dtype(
        df[value_column]
    ):
        raise ValueError(
            f"Column '{value_column}' is not numeric."
        )

    result = (
        df.groupby(group_column)[value_column]
        .sum()
        .sort_values(ascending=False)
    )

    return result


def top_value(
    df,
    group_column,
    value_column
):
    """
    Find the value in group_column that has
    the highest total value_column.

    Example:

    Customer + Revenue

    Returns the customer with the
    highest total revenue.
    """

    result = group_by_column(
        df,
        group_column,
        value_column
    )

    if result.empty:
        raise ValueError(
            "No data available for analysis."
        )

    return result.index[0]


def column_summary(df):
    """
    Create a summary of every column.
    """

    summary = []

    for column in df.columns:

        summary.append(
            {
                "column": column,
                "data_type": str(
                    df[column].dtype
                ),
                "unique_values": int(
                    df[column].nunique()
                ),
                "missing_values": int(
                    df[column].isna().sum()
                ),
            }
        )

    return pd.DataFrame(summary)