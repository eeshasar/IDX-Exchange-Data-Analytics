# IDX Exchange Data Analyst Internship
# Script: week2.py
# Purpose: Dataset structuring, validation, and EDA on sold residential data
# Results:
# Rows: 412,131 | Columns: 84
# Property types confirmed: Residential only
# Columns >90% missing: 16 columns flagged
# ClosePrice median: $820,000 | mean: $1,192,897
# LivingArea median: 1,644 sqft | mean: 1,906 sqft
# DaysOnMarket median: 19 days | mean: 38 days
# Notable outliers: negative DaysOnMarket, extreme ClosePrice and LivingArea values

import pandas as pd
import os

folder = '/Users/eeshasaraswat/Downloads/IDX Exchange Internship'
sold = pd.read_csv(os.path.join(folder, 'sold_combined_residential.csv'))
print(sold.shape)
print(sold.dtypes)
print(sold['PropertyType'].unique())

missing = sold.isnull().sum()
missing_pct = (missing / len(sold)) * 100
missing_report = pd.DataFrame({'missing_count': missing, 'missing_pct': missing_pct})
missing_report = missing_report[missing_report['missing_pct'] > 90]
print(missing_report)
numeric_cols = ['ClosePrice', 'LivingArea', 'DaysOnMarket']
print(sold[numeric_cols].describe(percentiles=[0.25, 0.5, 0.75, 0.95]))
sold.to_csv(os.path.join(folder, 'sold_week2.csv'), index=False)
print('Done! sold_week2.csv saved.')