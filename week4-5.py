# IDX Exchange Data Analyst Internship
# Script: week4.py
# Purpose: Clean and prepare the sold and listings residential datasets
# (built on Week 3 outputs, which already include the mortgage rate merge).
# Converts date fields to datetime, checks for redundant columns, ensures
# numeric fields are properly typed, flags (does not delete) invalid numeric
# values, flags date consistency violations, and flags geographic data
# quality issues.

 
import pandas as pd
 
sold = pd.read_csv("sold_week3.csv", low_memory=False)
listings = pd.read_csv("listings_week3.csv", low_memory=False)
 
print("Starting row counts")
print(f"  Sold: {len(sold):,} rows, {sold.shape[1]} columns")
print(f"  Listings: {len(listings):,} rows, {listings.shape[1]} columns")
 
# Step 1: convert date fields to datetime
 
date_fields = [
    "CloseDate",
    "PurchaseContractDate",
    "ListingContractDate",
    "ContractStatusChangeDate",
]
 
print("\nDate field conversion")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    for field in date_fields:
        if field in df.columns:
            before_nulls = df[field].isnull().sum()
            df[field] = pd.to_datetime(df[field], errors="coerce")
            after_nulls = df[field].isnull().sum()
            print(
                f"  [{name}] {field}: converted to datetime, now dtype {df[field].dtype} "
                f"(nulls before: {before_nulls}, after: {after_nulls}, "
                f"newly unparseable: {after_nulls - before_nulls})"
            )
        else:
            print(f"  [{name}] {field}: not present in dataset, skipped")
 
# Step 2: check for redundant columns and drop 
# Drops columns where every row has the same value

print("\nRedundant column check (constant-value columns)")

for df, name in [(sold, "sold"), (listings, "listings")]:
    constant_cols = [col for col in df.columns if df[col].nunique(dropna=False) <= 1]
    if constant_cols:
        print(f"  [{name}] Dropping constant-value columns: {constant_cols}")
        df.drop(columns=constant_cols, inplace=True)
    else:
        print(f"  [{name}] No constant-value columns found")
 
# Step 3: ensure numeric fields are properly typed
 
numeric_fields = [
    "ClosePrice",
    "ListPrice",
    "OriginalListPrice",
    "LivingArea",
    "LotSizeAcres",
    "BedroomsTotal",
    "BathroomsTotalInteger",
    "DaysOnMarket",
    "YearBuilt",
]
 
print("\nNumeric field type check")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    for field in numeric_fields:
        if field in df.columns:
            before_dtype = df[field].dtype
            before_nulls = df[field].isnull().sum()
            df[field] = pd.to_numeric(df[field], errors="coerce")
            after_nulls = df[field].isnull().sum()
            print(
                f"  [{name}] {field}: {before_dtype} -> {df[field].dtype} "
                f"(nulls before: {before_nulls}, after: {after_nulls})"
            )
        else:
            print(f"  [{name}] {field}: not present in dataset, skipped")
 
# Step 4: handle missing values in retained fields
# Documents % missing per field rather than dropping or guessing values
 
print("\nMissing value summary for core numeric fields (retained, not modified)")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    print(f"  [{name}]")
    for field in numeric_fields:
        if field in df.columns:
            pct_missing = df[field].isnull().mean() * 100
            print(f"    {field}: {pct_missing:.2f}% missing")
 
# Step 5: flag invalid numeric values
 
print("\nInvalid numeric value flags")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    if "ClosePrice" in df.columns:
        df["invalid_close_price_flag"] = df["ClosePrice"] <= 0
        print(f"  [{name}] invalid_close_price_flag: {df['invalid_close_price_flag'].sum()} rows")
 
    if "LivingArea" in df.columns:
        df["invalid_living_area_flag"] = df["LivingArea"] <= 0
        print(f"  [{name}] invalid_living_area_flag: {df['invalid_living_area_flag'].sum()} rows")
 
    if "DaysOnMarket" in df.columns:
        df["invalid_days_on_market_flag"] = df["DaysOnMarket"] < 0
        print(f"  [{name}] invalid_days_on_market_flag: {df['invalid_days_on_market_flag'].sum()} rows")
 
    if "BedroomsTotal" in df.columns:
        df["invalid_bedrooms_flag"] = df["BedroomsTotal"] < 0
        print(f"  [{name}] invalid_bedrooms_flag: {df['invalid_bedrooms_flag'].sum()} rows")
 
    if "BathroomsTotalInteger" in df.columns:
        df["invalid_bathrooms_flag"] = df["BathroomsTotalInteger"] < 0
        print(f"  [{name}] invalid_bathrooms_flag: {df['invalid_bathrooms_flag'].sum()} rows")
 
# Step 6: date consistency checks
 
 
# Step 7: geographic data checks
 
 
# Save cleaned datasets
 
print("\nFinal row counts (no rows deleted in this step, only flagged)")
print(f"  Sold: {len(sold):,} rows, {sold.shape[1]} columns")
print(f"  Listings: {len(listings):,} rows, {listings.shape[1]} columns")
 
sold.to_csv("sold_week4.csv", index=False)
listings.to_csv("listings_week4.csv", index=False)
 
print("\nSaved sold_week4.csv and listings_week4.csv")
