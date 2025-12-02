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


def standardize_month(df, month_column, default_month=None):
    if month_column not in df.columns:
        print(f"[warning] Month column '{month_column}' not found, skipping month standardization")
        return df

    raw = df[month_column]

    normalized = raw.astype(str).str.strip().str.lower()

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

    normalized = normalized.replace(mapping)

    # Treat empty strings and literal "nan" or "none" as missing
    normalized = normalized.replace(["", "nan", "none"], pd.NA)

    # Put back into the dataframe
    df[month_column] = normalized

    # Fill missing with default month if provided
    if default_month:
        df[month_column] = df[month_column].fillna(default_month)

    return df

def strip_whitespace(df):
    for col in df.select_dtypes(include=["object", "string"]).columns:
        df[col] = df[col].astype(str).str.strip()
    return df

def filter_by_status(df, status_column, allowed_values):
    if status_column not in df.columns:
        print(f"[warning] Status column '{status_column}' not found, skipping status filter")
        return df

    if not allowed_values:
        return df

    return df[df[status_column].isin(allowed_values)]

def apply_pipeline(df, config):
    # Strip whitespace first
    if config.get("strip_whitespace"):
        df = strip_whitespace(df)

    # Remove exact duplicates
    if config.get("remove_duplicates"):
        df = remove_duplicates(df)

    # Standardize month and fill missing
    if config.get("standardize_month"):
        month_col = config.get("month_column", "month")
        default_month = config.get("default_month")
        df = standardize_month(df, month_col, default_month)

    # Status filter if you decide to use it
    allowed = config.get("allowed_statuses") or []
    if allowed:
        df = filter_by_status(
            df,
            config.get("status_column", "STATUS"),
            allowed,
        )

    return df
