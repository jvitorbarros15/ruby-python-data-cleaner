import json
import pandas as pd

def read_csv_safe(path):
    try:
        return pd.read_csv(path, encoding="utf8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin1")


def load_config(config_path):
    with open(config_path, "r", encoding="utf8") as f:
        return json.load(f)


def remove_duplicates(df):
    return df.drop_duplicates()


def standardize_month(df, month_column):
    if month_column not in df.columns:
        print(f"[warning] Month column '{month_column}' not found, skipping month standardization")
        return df

    raw = df[month_column].astype(str).str.strip().str.lower()

    mapping = {
        "jan": "January",
        "january": "January",
        "fev": "February",
        "feb": "February",
        "mar": "March",
        "apr": "April",
        "abr": "April",
        "may": "May",
        "mai": "May",
        "jun": "June",
        "jul": "July",
        "aug": "August",
        "ago": "August",
        "sep": "September",
        "sept": "September",
        "set": "September",
        "oct": "October",
        "out": "October",
        "nov": "November",
        "dec": "December",
        "dez": "December"
    }

    df[month_column] = raw.replace(mapping)
    return df


def apply_pipeline(df, config):
    # remove duplicates
    if config.get("remove_duplicates"):
        df = remove_duplicates(df)

    # standardize month
    if config.get("standardize_month"):
        month_col = config.get("month_column", "month")
        df = standardize_month(df, month_col)

    return df
