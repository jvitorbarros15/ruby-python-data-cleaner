import pandas as pd
import sys, os

# Use paths passed from Ruby
input_file = sys.argv[1] if len(sys.argv) > 1 else "Book2.csv"
output_file = sys.argv[2] if len(sys.argv) > 2 else "publications_audit.xlsx"


# ------------- Helper -----------------------------------------------------
def normalize_month(x):
    if pd.isna(x):
        return None
    s = str(x).strip().title()
    if s in ["", "Nan", "None"]:
        return None
    return s

valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# ------------- Read -------------------------------------------------------
df = pd.read_csv(input_file, encoding='latin1')
print(f"Original rows: {len(df)}")

# Keep a copy for diff/inspection
df_original = df.copy()

# ------------- Step 1: remove identical duplicates -------------------------
df_no_exact_dup = df.drop_duplicates(keep='first')
exact_duplicates_removed = df.shape[0] - df_no_exact_dup.shape[0]
print(f"Exact duplicates removed: {exact_duplicates_removed}")

# Save exact duplicates removed for inspection
# We get rows that are in original but not in df_no_exact_dup (preserve order)
mask_kept = df_original.duplicated(keep='first')
identical_removed = df_original[mask_kept].copy()
identical_removed.reset_index(drop=True, inplace=True)

# ------------- Step 2: normalize DTM_PUB and mark rows --------------------
df_work = df_no_exact_dup.copy()
df_work['DTM_PUB_orig'] = df_work['DTM_PUB']  # keep original text for audit
df_work['DTM_PUB'] = df_work['DTM_PUB'].apply(normalize_month)
df_work['HAS_MONTH'] = df_work['DTM_PUB'].isin(valid_months)

# ------------- Step 3: handle title conflicts and choose which to keep ----
# We'll record for each TITLE: all rows, which kept, which dropped and why
grouped = df_work.groupby('TITLE', as_index=False)

kept_rows = []
conflict_rows = []  # rows dropped from titles that had >1 candidate

for title, group in grouped:
    if len(group) == 1:
        # no conflict, keep that single row
        row = group.iloc[0].to_dict()
        kept_rows.append(row)
    else:
        # conflict: prefer any row with a valid month
        with_month = group[group['HAS_MONTH']]
        if len(with_month) > 0:
            # If multiple with month, pick the first occurrence (preserves orig order)
            chosen = with_month.iloc[0]
            reason = "Picked row with month"
        else:
            # none have month: choose first and default to December later
            chosen = group.iloc[0]
            reason = "No months available; picked first (will default DTM_PUB->December)"
        chosen_dict = chosen.to_dict()
        chosen_dict['_selection_reason'] = reason
        kept_rows.append(chosen_dict)

        # Mark the dropped ones for audit
        dropped = group.drop(index=chosen.name)
        for _, dr in dropped.iterrows():
            dr_dict = dr.to_dict()
            dr_dict['_dropped_reason'] = f"Dropped in favor of row index {chosen.name}"
            conflict_rows.append(dr_dict)

# Build DataFrames
df_kept = pd.DataFrame(kept_rows).reset_index(drop=True)
df_dropped_conflicts = pd.DataFrame(conflict_rows).reset_index(drop=True)

# ------------- Step 4: finalize: set missing months to 'December' ----------
df_kept['DTM_PUB'] = df_kept['DTM_PUB'].fillna('December')

# ------------- Step 5: automatic checks/assertions -------------------------
# 1) No exact duplicates remain in final kept table (full-row duplicates)
assert not df_kept.duplicated().any(), "Assertion failed: final kept table contains exact duplicates."

# 2) TITLEs are unique in final kept table
duped_titles_final = df_kept['TITLE'][df_kept['TITLE'].duplicated()].unique().tolist()
if len(duped_titles_final) > 0:
    print("ERROR: Some TITLEs are duplicated in final kept table:", duped_titles_final)
else:
    print("OK: All TITLE values are unique in the final kept table.")

# 3) For every title that originally had >=1 row, ensure final has 1 row
orig_title_counts = df_original.groupby('TITLE').size().reset_index(name='orig_count')
final_title_counts = df_kept.groupby('TITLE').size().reset_index(name='final_count')
merged_counts = orig_title_counts.merge(final_title_counts, on='TITLE', how='left').fillna(0)
problems = merged_counts[merged_counts['final_count'] != 1]
if not problems.empty:
    print("WARNING: Some TITLEs did not end with exactly 1 row:")
    print(problems.head())
else:
    print("OK: Every TITLE ended with exactly 1 row in the final table.")

# 4) For titles where any original row had a month, final kept row should have a month (not December)
# Build map of titles that had any month originally
title_had_month = df_work.groupby('TITLE')['HAS_MONTH'].any().reset_index()
title_had_month.columns = ['TITLE', 'ORIG_HAD_MONTH']
check = df_kept.merge(title_had_month, on='TITLE', how='left')
# If ORIG_HAD_MONTH is True, final DTM_PUB must not be 'December' (unless original month was 'December' itself)
mask_wrong = (check['ORIG_HAD_MONTH'] == True) & (check['DTM_PUB'] == 'December')
if mask_wrong.any():
    print("WARNING: Some titles had an original month but final row ended with 'December':")
    print(check[mask_wrong][['TITLE', 'DTM_PUB', 'ORIG_HAD_MONTH']].head())
else:
    print("OK: Titles that originally had months preserved a month in the final row.")

# ------------- Step 6: Summary prints -------------------------------------
print("\nSummary:")
print(f" - Original rows: {len(df_original)}")
print(f" - Exact duplicates removed: {len(identical_removed)}")
print(f" - Titles with conflicts (originally >1 row): {df_work.groupby('TITLE').filter(lambda g: len(g)>1)['TITLE'].nunique()}")
print(f" - Rows dropped because of title conflict: {len(df_dropped_conflicts)}")
print(f" - Final kept rows: {len(df_kept)}")

# ------------- Step 7: Save audit Excel with multiple sheets ----------------
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df_kept.to_excel(writer, sheet_name='kept', index=False)
    identical_removed.to_excel(writer, sheet_name='identical_removed', index=False)
    df_dropped_conflicts.to_excel(writer, sheet_name='dropped_conflicts', index=False)
    df_original.to_excel(writer, sheet_name='original', index=False)

print(f"\n✅ Audit workbook saved: {output_file}")

# === OPTIONAL COMPARISON TO YOUR EXISTING CLEANED FILE ===
try:
    old = pd.read_excel("publications_unique_titles.xlsx")  # or .csv if you saved as CSV

    old_titles = set(old["TITLE"].astype(str).str.strip())
    new_titles = set(df_kept["TITLE"].astype(str).str.strip())  # ✅ fixed here

    only_in_old = old_titles - new_titles
    only_in_new = new_titles - old_titles

    print("\n=== COMPARISON TO publications_unique_titles.xlsx ===")
    print(f"Titles only in OLD file: {len(only_in_old)}")
    print(f"Titles only in NEW file: {len(only_in_new)}")

    if only_in_old:
        print("\nSample titles only in old file:")
        print(list(only_in_old)[:10])

    if only_in_new:
        print("\nSample titles only in new file:")
        print(list(only_in_new)[:10])

    if only_in_old or only_in_new:
        df_diff_old = old[old["TITLE"].isin(only_in_old)]
        df_diff_new = df_kept[df_kept["TITLE"].isin(only_in_new)]

        with pd.ExcelWriter("comparison_differences.xlsx", engine="openpyxl") as writer:
            df_diff_old.to_excel(writer, sheet_name="only_in_old", index=False)
            df_diff_new.to_excel(writer, sheet_name="only_in_new", index=False)

        print("📊 Differences saved in 'comparison_differences.xlsx'")

except FileNotFoundError:
    print("\nNo publications_unique_titles.xlsx found — skipping comparison.")
