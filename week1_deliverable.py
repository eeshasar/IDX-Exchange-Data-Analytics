# -*- coding: utf-8 -*-
import pandas as pd 
import os
folder = '/Users/eeshasaraswat/Downloads/IDX Exchange Internship' 
all_files = os.listdir(folder)
sold_files = [f for f in all_files if f.startswith('CRMLSSold') and f.endswith('.csv')]
listing_files = [f for f in all_files if f.startswith('CRMLSListing') and f.endswith('.csv')]
best_sold = []
for f in sold_files:
    if '_filled.csv' in f:
        best_sold.append(f)
    elif f.replace('.csv', '_filled.csv') not in sold_files:
        best_sold.append(f)
sold_dfs = []
for f in best_sold:
    df = pd.read_csv(os.path.join(folder, f))
    sold_dfs.append(df)
sold = pd.concat(sold_dfs)
print('Sold rows after combining:', len(sold))
listing_dfs = []
for f in listing_files:
    df = pd.read_csv(os.path.join(folder, f))
    listing_dfs.append(df)
listings = pd.concat(listing_dfs)
print('Listings rows after combining:', len(listings))
sold = sold[sold['PropertyType'] == 'Residential']
print('Sold rows after Residential filter:', len(sold))

listings = listings[listings['PropertyType'] == 'Residential']
print('Listings rows after Residential filter:', len(listings))

sold.to_csv(os.path.join(folder, 'sold_combined_residential.csv'), index=False)
listings.to_csv(os.path.join(folder, 'listings_combined_residential.csv'), index=False)
print('Done! Files saved.')
