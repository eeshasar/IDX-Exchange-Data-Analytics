# -*- coding: utf-8 -*-
import pandas as pd 
import os
os.chdir('/Users/eeshasaraswat/Downloads/IDX Exchange Internship')
sold1 = pd.read_csv('CRMLSSold202601.csv')
sold2 = pd.read_csv('CRMLSSold202602.csv')
sold3 = pd.read_csv('CRMLSSold202603.csv')
sold4 = pd.read_csv('CRMLSSold202604.csv')
sold5 = pd.read_csv('CRMLSSold202605.csv')
list1 = pd.read_csv('CRMLSListing202601.csv')
list2 = pd.read_csv('CRMLSListing202602.csv')
list3 = pd.read_csv('CRMLSListing202603.csv')
list4 = pd.read_csv('CRMLSListing202604.csv')
list5 = pd.read_csv('CRMLSListing202605.csv')
sold = pd.concat([sold1, sold2, sold3, sold4, sold5])
print('Sold rows after combining:', len(sold))
listings = pd.concat([list1, list2, list3, list4, list5])
print('Listings rows after combining:', len(listings))
sold = sold[sold['PropertyType'] == 'Residential']
print('Sold rows after Residential filter:', len(sold))
listings = listings[listings['PropertyType'] == 'Residential']
print('Listings rows after Residential filter:', len(listings))
sold.to_csv('sold_combined_residential.csv', index=False)
listings.to_csv('listings_combined_residential.csv', index=False)
print('Done! Files saved.')