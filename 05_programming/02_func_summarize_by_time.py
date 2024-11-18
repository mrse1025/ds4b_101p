# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 5 (Programming): Functions ----

# Imports

import pandas as pd
import numpy as np
from pandas.core import groupby

from my_panda_extensions.database import collect_data

df = collect_data()

# WHAT WE WANT TO STREAMLINE
freq = 'q'

df[['category_2', 'order_date', 'total_price']] \
    .groupby(['category_2', pd.Grouper(key = 'order_date', freq = freq),])\
    .agg(np.sum) \
    .unstack("category_2") \
    .reset_index()\
    .assign(order_date = lambda x: x['order_date'].dt.to_period())\
    .set_index('order_date') 

# BUILDING SUMMARIZE BY TIME

data = df

def summarize_by_time(data, 
                      date_column, 
                      value_column, 
                      groups = None, 
                      rule = "D", 
                      kind = "timestamp",
                      agg_func = np.sum,
                      *args,
                      **kwargs
                      ):
    #Checks
    if type(value_column) is not list:
        value_column = [value_column]
    #Body
    
    #Handle date column
    data = data.set_index(date_column)
    
    #Handle Groups
    if groups is not None:
        data = data.groupby(groups)
    
    #Handle resample
    data = data.resample(rule = rule, kind = kind)

    #Handle Aggregatio
    function_list = [agg_func] * len(value_column)
    agg_dict      = dict(zip(value_column, function_list))
    
    data = data.agg(
        func = agg_dict,
        *args, 
        **kwargs
    )
    
    return data

data = df

summarize_by_time(data, 
                  date_column = 'order_date', 
                  value_column= ['total_price', 'quantity'], 
                  groups = ['category_2'],
                  rule = "M", 
                  agg_func= [np.mean, np.sum]
                  )
    


# ADDING TO OUR TIME SERIES MODULE

