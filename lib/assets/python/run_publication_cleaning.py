import sys
import pandas as pd
import os

from feature_selection import read_csv_safe, load_config, apply_pipeline

def summarize(df_before, df_after):
    print("=== Cleaning summary ===")
    print(f"Rows before: {len(df_before)}")
    print(f"Rows after:  {len(df_after)}")
    print(f"Columns:     {list(df_after.columns)}")

if __name__ == "__main__":
    input_path = sys.argv[1]
    output_csv = sys.argv[2]
    output_xlsx = sys.argv[3]
    config_path = sys.argv[4]

    print("[python] Input:", input_path)
    print("[python] Config:", config_path)

    df = read_csv_safe(input_path)
    df_before = df.copy()

    config = load_config(config_path)
    df = apply_pipeline(df, config)

    summarize(df_before, df)

    # Create the output directory if missing
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    df.to_csv(output_csv, index=False)
    df.to_excel(output_xlsx, index=False)

    print("[python] Saved:", output_csv, "and", output_xlsx)


