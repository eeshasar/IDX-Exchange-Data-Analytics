# IDX Exchange Data Analyst Internship
# Script: week2.py
# Purpose: Dataset structuring, validation, and EDA on sold and listings residential data
#
# Results - Sold:
# Rows: 412,131 | Columns: 84
# Property types confirmed: Residential only
# Columns >90% missing: 15 columns dropped
# ClosePrice median: $820,000 | mean: $1,192,897
# LivingArea median: 1,644 sqft | mean: 1,906 sqft
# DaysOnMarket median: 19 days | mean: 37.8 days
# Notable outliers: negative DaysOnMarket (48), extreme ClosePrice and LivingArea values
#
# Results - Listings:
# Rows: 574,969 | Columns: 84
# Property types confirmed: Residential only
# Columns >90% missing: 13 columns dropped
# Listprice median: $849,000 | mean: $1,320,359
# LivingArea median: 1,672 sqft | mean: 1,982 sqft
# DaysOnMarket median: 10 days | mean: 18.1 days
 
 
import pandas as pd
import os
import matplotlib.pyplot as plt
 
folder = '/Users/eeshasaraswat/Downloads/IDX Exchange Internship'
 
 
def drop_high_null_columns(df, threshold=0.90):
    null_pct = df.isnull().mean()
    cols_to_drop = null_pct[null_pct > threshold].index.tolist()
 
    print(f"Columns dropped (>{int(threshold*100)}% null): {len(cols_to_drop)}")
    for col in cols_to_drop:
        print(f"  {col}: {null_pct[col]:.1%} null")
 
    df_reduced = df.drop(columns=cols_to_drop)
    print(f"Columns before: {df.shape[1]}, after: {df_reduced.shape[1]}")
    return df_reduced
 
 
def plot_boxplots(df, columns, dataset_name):
    for col in columns:
        if col in df.columns:
            plt.figure(figsize=(6, 4))
            plt.boxplot(df[col].dropna(), vert=False)
            plt.title(f'{dataset_name} - {col} Distribution')
            plt.xlabel(col)
            plt.tight_layout()
            plt.savefig(os.path.join(folder, f'{dataset_name}_{col}_boxplot.png'))
            plt.show()
            
# SOLD
 
sold = pd.read_csv(os.path.join(folder, 'sold_combined_residential.csv'), low_memory=False)
 
print("Columns:", sold.columns.tolist())
print(sold.head())
print(f"Shape: {sold.shape[0]:,} rows, {sold.shape[1]} columns")
print(sold.dtypes)
 
print("\n Property Type Breakdown")
print(sold['PropertyType'].value_counts())
print("Unique property types:", sold['PropertyType'].unique())
 
sold = sold[sold['PropertyType'] == 'Residential']
print(f"After Residential filter: {sold.shape[0]:,} rows")
 
print("\n Null Count Summary")
null_counts = sold.isnull().sum()
null_pct = (null_counts / len(sold) * 100).round(2)
null_report = pd.DataFrame({'null_count': null_counts, 'null_pct': null_pct})
null_report = null_report[null_report['null_count'] > 0].sort_values('null_pct', ascending=False)
print(null_report.to_string())
 
print("\n Dropping Columns Above 90% Missing")
sold = drop_high_null_columns(sold)
 
print("\n Remaining Columns After Null Drop")
print(sold.columns.tolist())
 
print("\n Numeric Distribution Summary")
key_fields = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
for field in key_fields:
    if field in sold.columns:
        print(f"\n{field}:")
        print(sold[field].describe(percentiles=[.10, .25, .50, .75, .90, .95, .99]))
 
print("\n Boxplots for Key Numeric Fields")
plot_boxplots(sold, key_fields, 'sold')
 
print("\n Median and Mean ClosePrice")
print(f"Median ClosePrice: ${sold['ClosePrice'].median():,.0f}")
print(f"Mean ClosePrice:   ${sold['ClosePrice'].mean():,.0f}")
 
print("\n DaysOnMarket Distribution")
print(f"Median DaysOnMarket: {sold['DaysOnMarket'].median()}")
print(f"Mean DaysOnMarket:   {sold['DaysOnMarket'].mean():.1f}")
print(f"Negative DaysOnMarket count: {(sold['DaysOnMarket'] < 0).sum():,}")
 
print("\n Sold Above vs Below List Price")
if 'ListPrice' in sold.columns:
    above = (sold['ClosePrice'] >= sold['ListPrice']).sum()
    below = (sold['ClosePrice'] < sold['ListPrice']).sum()
    print(f"Sold at or above list price: {above:,} ({above/len(sold)*100:.1f}%)")
    print(f"Sold below list price:       {below:,} ({below/len(sold)*100:.1f}%)")
 
print("\n Date Consistency Check")
if 'CloseDate' in sold.columns and 'ListingContractDate' in sold.columns:
    sold['CloseDate'] = pd.to_datetime(sold['CloseDate'], errors='coerce')
    sold['ListingContractDate'] = pd.to_datetime(sold['ListingContractDate'], errors='coerce')
    date_issues = (sold['CloseDate'] < sold['ListingContractDate']).sum()
    print(f"Listings where close date is before listing date: {date_issues:,}")
 
print("\n Top 10 Counties by Median ClosePrice")
if 'CountyOrParish' in sold.columns:
    county_median = sold.groupby('CountyOrParish')['ClosePrice'].median().sort_values(ascending=False)
    print(county_median.head(10))
 
sold.to_csv(os.path.join(folder, 'sold_week2.csv'), index=False)
print("\nDone! sold_week2.csv saved.")
 
# LISTINGS
 
listings = pd.read_csv(os.path.join(folder, 'listings_combined_residential.csv'), low_memory=False)
 
print("\n\nColumns:", listings.columns.tolist())
print(listings.head())
print(f"Shape: {listings.shape[0]:,} rows, {listings.shape[1]} columns")
print(listings.dtypes)
 
print("\n Property Type Breakdown")
print(listings['PropertyType'].value_counts())
print("Unique property types:", listings['PropertyType'].unique())
 
listings = listings[listings['PropertyType'] == 'Residential']
print(f"After Residential filter: {listings.shape[0]:,} rows")
 
dupe_cols = [c for c in listings.columns if c.endswith('.1')]
print(f"Dropping duplicate columns: {dupe_cols}")
listings = listings.drop(columns=dupe_cols)

print("\n Null Count Summary")
null_counts_l = listings.isnull().sum()
null_pct_l = (null_counts_l / len(listings) * 100).round(2)
null_report_l = pd.DataFrame({'null_count': null_counts_l, 'null_pct': null_pct_l})
null_report_l = null_report_l[null_report_l['null_count'] > 0].sort_values('null_pct', ascending=False)
print(null_report_l.to_string())
 
print("\n Dropping Columns Above 90% Missing")
listings = drop_high_null_columns(listings)
 
print("\n Remaining Columns After Null Drop")
print(listings.columns.tolist())
 
print("\n Numeric Distribution Summary")
key_fields_l = ['ListPrice', 'LivingArea', 'DaysOnMarket']
for field in key_fields_l:
    if field in listings.columns:
        print(f"\n{field}:")
        print(listings[field].describe(percentiles=[.10, .25, .50, .75, .90, .95, .99]))
 
print("\n Boxplots for Key Numeric Fields")
plot_boxplots(listings, key_fields_l, 'listings')
 
print("\n Median and Mean ListPrice")
print(f"Median ListPrice: ${listings['ListPrice'].median():,.0f}")
print(f"Mean ListPrice:   ${listings['ListPrice'].mean():,.0f}")
 
print("\n Top 10 Counties by Median ListPrice")
if 'CountyOrParish' in listings.columns:
    county_median_l = listings.groupby('CountyOrParish')['ListPrice'].median().sort_values(ascending=False)
    print(county_median_l.head(10))
 
listings.to_csv(os.path.join(folder, 'listings_week2.csv'), index=False)
print("\nDone! listings_week2.csv saved.")
