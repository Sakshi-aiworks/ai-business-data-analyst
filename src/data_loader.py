import pandas as pd # type: ignore


def load_data(file_path):
    """
    Load CSV or Excel data into a Pandas DataFrame.
    """

    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)

    elif file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)

    else:
        raise ValueError("Only CSV and Excel files are supported.")

    return df