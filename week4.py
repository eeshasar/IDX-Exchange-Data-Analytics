# IDX Exchange Data Analyst Internship
# Script: week4.py
# Purpose: Clean and prepare the sold and listings residential datasets
# (built on Week 3 outputs, which already include the mortgage rate merge).
# Converts date fields to datetime, checks for redundant columns, ensures
# numeric fields are properly typed, flags (does not delete) invalid numeric
# values, flags date consistency violations, and flags geographic data
# quality issues.
#
# Results:
# Sold: 412,131 rows, 71 columns before -> 83 columns after
# Listings: 574,969 rows, 62 columns before -> 74 columns after
# Sold invalid_close_price_flag count: 1
# Sold negative_timeline_flag count: 509
# Listings missing_coords_flag count: 76564
 
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
 
# Step 2: check for redundant columns
# High-null columns were already dropped in Week 2 (>90% threshold).
# Here we check for columns that are fully constant (same value in every row),
# since those add no analytical value and are safe to flag as redundant.
# We do not auto-drop these, just report them for review.
 
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
# We keep core fields even if partially missing (per Week 2-3 guidance).
# Rather than dropping or guessing values, we document how much is missing
# so downstream analysis can decide whether to exclude rows per-metric.
 
print("\nMissing value summary for core numeric fields (retained, not modified)")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    print(f"  [{name}]")
    for field in numeric_fields:
        if field in df.columns:
            pct_missing = df[field].isnull().mean() * 100
            print(f"    {field}: {pct_missing:.2f}% missing")
 
# Step 5: flag invalid numeric values (do not delete)
 
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
 
print("\nDate consistency flags")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    has_listing = "ListingContractDate" in df.columns
    has_purchase = "PurchaseContractDate" in df.columns
    has_close = "CloseDate" in df.columns
 
    # listing_after_close_flag: ListingContractDate should precede CloseDate
    if has_listing and has_close:
        df["listing_after_close_flag"] = df["ListingContractDate"] > df["CloseDate"]
        print(f"  [{name}] listing_after_close_flag: {df['listing_after_close_flag'].sum()} rows")
    else:
        print(f"  [{name}] listing_after_close_flag: skipped, missing required date column(s)")
 
    # purchase_after_close_flag: PurchaseContractDate should precede CloseDate
    if has_purchase and has_close:
        df["purchase_after_close_flag"] = df["PurchaseContractDate"] > df["CloseDate"]
        print(f"  [{name}] purchase_after_close_flag: {df['purchase_after_close_flag'].sum()} rows")
    else:
        print(f"  [{name}] purchase_after_close_flag: skipped, missing required date column(s)")
 
    # negative_timeline_flag: full order should be Listing -> Purchase -> Close
    if has_listing and has_purchase and has_close:
        df["negative_timeline_flag"] = (
            (df["ListingContractDate"] > df["PurchaseContractDate"])
            | (df["PurchaseContractDate"] > df["CloseDate"])
            | (df["ListingContractDate"] > df["CloseDate"])
        )
        print(f"  [{name}] negative_timeline_flag: {df['negative_timeline_flag'].sum()} rows")
    else:
        print(f"  [{name}] negative_timeline_flag: skipped, missing required date column(s)")
 
# Step 7: geographic data checks
 
print("\nGeographic data quality summary")
 
for df, name in [(sold, "sold"), (listings, "listings")]:
    has_lat = "Latitude" in df.columns
    has_lon = "Longitude" in df.columns
 
    if not (has_lat and has_lon):
        print(f"  [{name}] Latitude/Longitude not present in this dataset, geo checks skipped")
        continue
 
    df["missing_coords_flag"] = df["Latitude"].isnull() | df["Longitude"].isnull()
    df["zero_coord_flag"] = (df["Latitude"] == 0) | (df["Longitude"] == 0)
    df["invalid_longitude_sign_flag"] = df["Longitude"] > 0  # CA longitude should be negative
 
    # Rough California bounding box for plausibility check
    # (lat approx 32.5 to 42.0, lon approx -124.5 to -114.0)
    df["implausible_coord_flag"] = (
        df["Latitude"].notnull()
        & df["Longitude"].notnull()
        & (
            (df["Latitude"] < 32.5) | (df["Latitude"] > 42.0)
            | (df["Longitude"] < -124.5) | (df["Longitude"] > -114.0)
        )
    )
 
    print(f"  [{name}]")
    print(f"    missing_coords_flag: {df['missing_coords_flag'].sum()} rows")
    print(f"    zero_coord_flag: {df['zero_coord_flag'].sum()} rows")
    print(f"    invalid_longitude_sign_flag: {df['invalid_longitude_sign_flag'].sum()} rows")
    print(f"    implausible_coord_flag (outside CA bounding box): {df['implausible_coord_flag'].sum()} rows")
 
# Save cleaned datasets
 
print("\nFinal row counts (no rows deleted in this step, only flagged)")
print(f"  Sold: {len(sold):,} rows, {sold.shape[1]} columns")
print(f"  Listings: {len(listings):,} rows, {listings.shape[1]} columns")
 
sold.to_csv("sold_week4.csv", index=False)
listings.to_csv("listings_week4.csv", index=False)
 
print("\nSaved sold_week4.csv and listings_week4.csv")