# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 5 (Programming): Functions ----

# Imports

import pandas as pd
import numpy as np
from pandas.core import groupby
from pandas.core.series import Series

from my_panda_extensions.database import collect_data


df = collect_data()

# 1.0 EXAMINING FUNCTIONS ----

# Pandas Series Function
#?pd.Series.max
# ?np.max

df.total_price

df.total_price.max() #returns max total price

my_max = pd.Series.max

my_max(df.total_price)


# Pandas Data Frame Function
#?pd.DataFrame.aggregate

pd.DataFrame.aggregate(
    self = df[['total_price']],
    func = np.sum
)
#giving whole data set will try to perform func on all columns
#pass appropriate columns to func with [['']], double [[]] for series
#the above is the same as, df.aggregate(np.sum)
pd.DataFrame.aggregate(
    self = df[['total_price']],
    func = np.quantile,
    q = 0.5 #q is an argument for quantile, falls under kwargs
)

# 2.0 OUTLIER DETECTION FUNCTION ----
# - Works with a Pandas Series

x = df['total_price']
def detect_outliers(x, iqr_multipier = 1.5, how = "both") :
   
   #IQR Logic
    q75 = np.quantile(x, 0.75) #price for 75th quantile 
    q25 = np.quantile(x, 0.25) #price for  25th quantile 
    iqr = q75 -  q25 #inner quantile range
    
    lower_limit = q25 - iqr_multipier * iqr
    upper_limit = q75 + iqr_multipier * iqr
     
    outliers_upper = x >= upper_limit #logic for returning outliers 
    outliers_lower = x <= lower_limit
    
    if how == "both":
        outliers = outliers_upper | outliers_lower
    elif how == "lower":
        outliers = outliers_lower 
    else: 
        outliers = outliers_upper
        
    return outliers

detect_outliers(x, iqr_multipier= 0.1)

df[
    detect_outliers(
        df['total_price'], 
        iqr_multipier= 0.1,
        how = "lower")
]


# 3.0 EXTENDING A CLASS ----

