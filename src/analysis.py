import pandas as pd


# --------------------------------------------------
# Total Sales
# --------------------------------------------------

def total_sales(df):
    """
    Calculate total sales from the business data.
    """

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return df["Sales"].sum()


# --------------------------------------------------
# Total Profit
# --------------------------------------------------

def total_profit(df):
    """
    Calculate total profit from the business data.
    """

    if "Profit" not in df.columns:
        raise ValueError("Profit column is not available.")

    return df["Profit"].sum()


# --------------------------------------------------
# Top Product
# --------------------------------------------------

def top_product(df):
    """
    Find the product with the highest total sales.
    """

    if "Product" not in df.columns:
        raise ValueError("Product column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    product_sales = (
        df.groupby("Product")["Sales"]
        .sum()
    )

    return product_sales.idxmax()


# --------------------------------------------------
# Sales by Region
# --------------------------------------------------

def sales_by_region(df):
    """
    Calculate total sales grouped by region.
    """

    if "Region" not in df.columns:
        raise ValueError("Region column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return (
        df.groupby("Region")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


# --------------------------------------------------
# Sales by Product
# --------------------------------------------------

def sales_by_product(df):
    """
    Calculate total sales grouped by product.
    """

    if "Product" not in df.columns:
        raise ValueError("Product column is not available.")

    if "Sales" not in df.columns:
        raise ValueError("Sales column is not available.")

    return (
        df.groupby("Product")["Sales"]
        .sum()
        .sort_values(ascending=False)
    )


# --------------------------------------------------
# Sales Over Time
# --------------------------------------------------

def sales_over_time(df):
    """
    Calculate total sales over time.

    Converts the Date column into a proper datetime
    format and groups sales by date.
    """

    if "Date" not in df.columns:
        raise ValueError(
            "Date column is not available."
        )

    if "Sales" not in df.columns:
        raise ValueError(
            "Sales column is not available."
        )

    data = df.copy()

    # Convert Date column to datetime
    data["Date"] = pd.to_datetime(
        data["Date"],
        errors="coerce"
    )

    # Remove rows where Date could not be converted
    data = data.dropna(
        subset=["Date"]
    )

    if data.empty:
        raise ValueError(
            "No valid dates found."
        )

    # Group sales by date
    trend = (
        data.groupby("Date")["Sales"]
        .sum()
        .sort_index()
    )

    return trend