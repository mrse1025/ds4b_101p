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




# 3.0 EXTENDING A CLASS ----

