
def total_sales(df):
    return df["Sales"].sum()


def total_profit(df):
    return df["Profit"].sum()


def top_product(df):
    product_sales = df.groupby("Product")["Sales"].sum()
    return product_sales.idxmax()


def sales_by_region(df):
    return df.groupby("Region")["Sales"].sum().sort_values(ascending=False)


def sales_by_product(df):
    return df.groupby("Product")["Sales"].sum().sort_values(ascending=False)


def analyze_question(df, question):
    """
    Route a user's question to the appropriate analysis function.
    """

    question = question.lower()

    if "total sales" in question:
        return total_sales(df)

    elif "total profit" in question:
        return total_profit(df)

    elif "top product" in question or "best product" in question:
        return top_product(df)

    elif "region" in question:
        return sales_by_region(df)

    elif "product" in question:
        return sales_by_product(df)

    else:
        return None