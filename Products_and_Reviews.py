#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 23:52:30 2019

@author: loganguerry
"""

## ======================================= ##
## Pulling ASINs for only Ray-Ban products ##
## ======================================= ##

# load Amazon product metadata
loadedjson = open('Amazon_products_metadata.json', 'r')

# initiate dicts and counter variable (progress tracker in for loop)
allproducts = {}
listofcategories = {}
count = 0

# captures ASIN for every product listing
for aline in loadedjson:
    count += 1
    if count % 100000 == 0:
        print(count) # returns progress indicator
    aproduct = eval(aline)
    allproducts[aproduct['asin']] = aproduct 
    for categories in aproduct['categories']: # captures unique categories (brands)
        for acategory in categories:
            if acategory in listofcategories:
                listofcategories[acategory] += 1
            if acategory not in listofcategories:
                listofcategories[acategory] = 1


# subset only ASINs corresponding to Ray-Ban products       
allRBasins = set() # set - prevents duplicate values
count = 0 # initiating another progress indicator

for aproduct in allproducts:
    theproduct = allproducts[aproduct]
    count += 1
    if count % 100000 == 0:
        print(count/1503384)
    for categories in theproduct['categories']:
        for acategory in categories:
            if 'ray-ban'in acategory.lower():
                allRBasins.add(theproduct['asin'])


## ===================================== ##
## Joining Review Data for Ray-Ban ASINs ##
## ===================================== ##

# load review data
loadedjson = open('Amazon_reviews.json', 'r')

# capture only Ray-Ban reviews
allreviews = {}
count = 0 # progress indicator variable us in for loop below

for aline in loadedjson:
    count += 1
    if count % 100000 == 0:
        print(count)
    areview = eval(aline)
    theasin = areview['asin']
    thereviewer = areview['reviewerID']
    if theasin in allRBasins:
        thekey = '%s.%s' % (theasin,thereviewer)
        allreviews[thekey] = areview
        
len(allreviews) # check number of reviews 

# average number of reviews per product
len(allreviews)/len(allRBasins)

# write txt file with all Ray-Ban reviews
import json
json.dump(allreviews, open('Ray-Ban_reviews.json','w'))