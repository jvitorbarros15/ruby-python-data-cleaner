import pandas as pd
import sys

input_file = sys.argv[1]

output_file_unique_title = "publications_unique_title.xlsx"

# --- 1. Read CSV ---
df = pd.read_csv(input_file, encoding='latin1')
print(f"Total rows in original file: {len(df)}")

# --- 2. Remove exact (identical) duplicates ---
df_no_duplicates = df.drop_duplicates(keep='first')
duplicates_removed = len(df) - len(df_no_duplicates)
print(f"✅ Removed {duplicates_removed} identical duplicates")

# --- 3. Normalize DTM_PUB values ---
df_no_duplicates['DTM_PUB'] = (
    df_no_duplicates['DTM_PUB']
    .astype(str)
    .str.strip()
    .str.title()
)

# Replace empty, 'nan', or 'none' with None
df_no_duplicates.loc[df_no_duplicates['DTM_PUB'].isin(['', 'Nan', 'None']), 'DTM_PUB'] = None

# --- 4. Define valid months ---
valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# --- 5. Mark which rows have a valid month ---
df_no_duplicates['HAS_MONTH'] = df_no_duplicates['DTM_PUB'].isin(valid_months)

# --- 6. Sort so valid months come first ---
df_sorted = df_no_duplicates.sort_values(by='HAS_MONTH', ascending=False)

# --- 7. For each TITLE, keep only one row (the one with a month if available) ---
df_unique_title = df_sorted.groupby('TITLE', as_index=False).first()

# --- 8. Default missing DTM_PUB to 'December' ---
df_unique_title['DTM_PUB'] = df_unique_title['DTM_PUB'].fillna('December')

titles_removed = len(df_no_duplicates) - len(df_unique_title)
print(f"✅ Removed {titles_removed} duplicate titles across different users")
print(f"Rows remaining after keeping unique titles: {len(df_unique_title)}")

# --- 9. Drop helper column and export ---
df_unique_title.drop(columns=['HAS_MONTH'], inplace=True)
df_unique_title.to_excel(output_file_unique_title, index=False)

print(f"✅ Clean file saved as: {output_file_unique_title}")

