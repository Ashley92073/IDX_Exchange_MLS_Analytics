"""
Week 2-3 Deliverable A: Dataset Structuring and Validation
IDX Exchange Data Analyst Internship

This script:
1. Loads the combined listing and sold datasets
2. Documents unique PropertyType values found and the filtering logic applied
3. Produces a null-count / missing-value summary table for each dataset
4. Flags columns with >90% missing values
5. Produces a numeric distribution summary (min, max, mean, median, percentiles)
   for ClosePrice, LivingArea, and DaysOnMarket
6. Saves the filtered (Residential-only) dataset as a new CSV
"""

import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 150)

# ---------------------------------------------------------------
# Config: which files to process
# ---------------------------------------------------------------
DATASETS = {
    'listing': 'listing_combined.csv',
    'sold': 'sold_combined.csv',
}

NUMERIC_FIELDS_FOR_DISTRIBUTION = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
NULL_THRESHOLD = 0.90  # flag columns with >90% missing


def dedupe_columns(df):
    """
    The raw extraction scripts selected some fields twice (e.g. PropertyType,
    ListAgentFirstName, DaysOnMarket, Latitude, Longitude, CloseDate, ListPrice,
    LivingArea, BuyerOfficeName, UnparsedAddress), which pandas auto-renames on
    read (PropertyType.1, DaysOnMarket.1, etc). This drops the duplicated
    columns and keeps only the original field name.
    """
    dup_cols = [c for c in df.columns if c.endswith('.1')]
    if dup_cols:
        print(f"  Dropping {len(dup_cols)} duplicate-selected columns: {dup_cols}")
        df = df.drop(columns=dup_cols)
    return df


def run_eda(name, filepath):
    print("=" * 70)
    print(f"DATASET: {name.upper()}  ({filepath})")
    print("=" * 70)

    df = pd.read_csv(filepath, low_memory=False)
    df = dedupe_columns(df)

    # -----------------------------------------------------------
    # 1. Dataset understanding
    # -----------------------------------------------------------
    print(f"\n--- 1. Dataset Understanding ---")
    print(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    print("\nColumn dtypes:")
    print(df.dtypes.value_counts())

    # -----------------------------------------------------------
    # 2. Unique property types + filtering logic
    # -----------------------------------------------------------
    print(f"\n--- 2. PropertyType Values Found ---")
    if 'PropertyType' in df.columns:
        print(df['PropertyType'].value_counts(dropna=False))
    else:
        print("PropertyType column not found.")

    rows_before_filter = len(df)
    df_filtered = df[df['PropertyType'] == 'Residential'].copy()
    rows_after_filter = len(df_filtered)

    print(f"\nFiltering logic applied: df = df[df['PropertyType'] == 'Residential']")
    print(f"Rows before filter: {rows_before_filter}")
    print(f"Rows after filter:  {rows_after_filter}")
    print(f"Rows removed:       {rows_before_filter - rows_after_filter}")

    # -----------------------------------------------------------
    # 3. Missing value analysis (on the filtered dataset)
    # -----------------------------------------------------------
    print(f"\n--- 3. Missing Value Report (Residential-filtered) ---")
    null_counts = df_filtered.isnull().sum()
    null_pct = (null_counts / len(df_filtered) * 100).round(2)
    null_summary = pd.DataFrame({
        'null_count': null_counts,
        'null_pct': null_pct
    }).sort_values('null_pct', ascending=False)
    print(null_summary)

    high_null_cols = null_summary[null_summary['null_pct'] > NULL_THRESHOLD * 100]
    print(f"\nColumns with >{int(NULL_THRESHOLD*100)}% missing values ({len(high_null_cols)} found):")
    if len(high_null_cols) > 0:
        print(high_null_cols)
    else:
        print("None.")

    # -----------------------------------------------------------
    # 4. Numeric distribution summary
    # -----------------------------------------------------------
    print(f"\n--- 4. Numeric Distribution Summary ---")
    for field in NUMERIC_FIELDS_FOR_DISTRIBUTION:
        if field not in df_filtered.columns:
            print(f"\n{field}: column not found, skipping.")
            continue
        series = pd.to_numeric(df_filtered[field], errors='coerce')
        summary = series.describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
        print(f"\n{field}:")
        print(summary)

    # -----------------------------------------------------------
    # 5. Save filtered dataset
    # -----------------------------------------------------------
    out_path = f"{name}_residential_filtered.csv"
    df_filtered.to_csv(out_path, index=False, encoding='utf-8')
    print(f"\nSaved filtered dataset: {out_path} ({len(df_filtered)} rows)")

    return df_filtered, null_summary


if __name__ == '__main__':
    results = {}
    for name, path in DATASETS.items():
        results[name] = run_eda(name, path)

    # -----------------------------------------------------------
    # Suggested Intern Questions (answered using the SOLD dataset)
    # -----------------------------------------------------------
    if 'sold' in results:
        sold_df, _ = results['sold']
        print("\n" + "=" * 70)
        print("SUGGESTED INTERN QUESTIONS (based on sold_residential_filtered)")
        print("=" * 70)

        close_price = pd.to_numeric(sold_df['ClosePrice'], errors='coerce')
        list_price = pd.to_numeric(sold_df['ListPrice'], errors='coerce')

        print(f"\nMedian ClosePrice: {close_price.median():,.0f}")
        print(f"Average ClosePrice: {close_price.mean():,.0f}")

        dom = pd.to_numeric(sold_df['DaysOnMarket'], errors='coerce')
        print(f"\nDaysOnMarket distribution:\n{dom.describe()}")

        above_list = (close_price > list_price).mean() * 100
        below_list = (close_price < list_price).mean() * 100
        at_list = (close_price == list_price).mean() * 100
        print(f"\n% sold above list price: {above_list:.1f}%")
        print(f"% sold below list price: {below_list:.1f}%")
        print(f"% sold at list price:    {at_list:.1f}%")

        close_dt = pd.to_datetime(sold_df['CloseDate'], errors='coerce')
        listing_dt = pd.to_datetime(sold_df['ListingContractDate'], errors='coerce')
        date_issue = (close_dt < listing_dt).sum()
        print(f"\nRecords where CloseDate < ListingContractDate (date inconsistency): {date_issue}")

        if 'CountyOrParish' in sold_df.columns:
            county_median = sold_df.groupby('CountyOrParish')['ClosePrice'].apply(
                lambda x: pd.to_numeric(x, errors='coerce').median()
            ).sort_values(ascending=False)
            print(f"\nTop 10 counties by median ClosePrice:\n{county_median.head(10)}")