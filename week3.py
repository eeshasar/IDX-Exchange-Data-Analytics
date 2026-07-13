# IDX Exchange Data Analyst Internship
# Script: week3.py
# Purpose: Enrich sold and listings residential datasets with the national 30-year
# fixed mortgage rate (FRED MORTGAGE30US), resampled from weekly to monthly,
# and joined on a year_month key.
#
# Results:
# Sold: 412,131 rows, 69 columns before merge -> 71 columns after merge
# Sold unmatched rate rows after merge: 0
# Listings: 574,969 rows, 60 columns before merge -> 62 columns after merge
# Listings unmatched rate rows after merge: 0
 
 
import pandas as pd
import os
 
folder = '/Users/eeshasaraswat/Downloads/IDX Exchange Internship'
 
 
def add_mortgage_rates(df, date_column):
    # Step 1: fetch mortgage rate data from FRED
    url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"
    mortgage = pd.read_csv(url, parse_dates=['observation_date'])
    mortgage.columns = ['date', 'rate_30yr_fixed']
 
    # Step 2: resample weekly rates to monthly averages
    mortgage['year_month'] = mortgage['date'].dt.to_period('M')
    mortgage_monthly = (
        mortgage.groupby('year_month')['rate_30yr_fixed']
        .mean()
        .reset_index()
    )
 
    # Step 3: create matching year_month key on the MLS dataset
    df['year_month'] = pd.to_datetime(df[date_column], errors='coerce').dt.to_period('M')
 
    # Step 4: merge
    df_with_rates = df.merge(mortgage_monthly, on='year_month', how='left')
 
    # Step 5: validate merge completeness
    unmatched = df_with_rates['rate_30yr_fixed'].isnull().sum()
    print(f"Unmatched rate rows: {unmatched:,}")
 
    return df_with_rates
 
 
# SOLD
 
sold = pd.read_csv(os.path.join(folder, 'sold_week2.csv'), low_memory=False)
print(f"Sold shape before merge: {sold.shape[0]:,} rows, {sold.shape[1]} columns")
 
print("\n Merging Mortgage Rates onto Sold (keyed on CloseDate)")
sold_with_rates = add_mortgage_rates(sold, 'CloseDate')
print(f"Sold shape after merge: {sold_with_rates.shape[0]:,} rows, {sold_with_rates.shape[1]} columns")
 
print("\n Preview")
print(sold_with_rates[['CloseDate', 'year_month', 'ClosePrice', 'rate_30yr_fixed']].head())
 
sold_with_rates.to_csv(os.path.join(folder, 'sold_week3.csv'), index=False)
print("\nDone! sold_week3.csv saved.")
 
# LISTINGS
 
listings = pd.read_csv(os.path.join(folder, 'listings_week2.csv'), low_memory=False)
print(f"\n\nListings shape before merge: {listings.shape[0]:,} rows, {listings.shape[1]} columns")
 
print("\n Merging Mortgage Rates onto Listings (keyed on ListingContractDate)")
listings_with_rates = add_mortgage_rates(listings, 'ListingContractDate')
print(f"Listings shape after merge: {listings_with_rates.shape[0]:,} rows, {listings_with_rates.shape[1]} columns")
 
print("\n Preview")
print(listings_with_rates[['ListingContractDate', 'year_month', 'ListPrice', 'rate_30yr_fixed']].head())
 
listings_with_rates.to_csv(os.path.join(folder, 'listings_week3.csv'), index=False)
print("\nDone! listings_week3.csv saved.")
 