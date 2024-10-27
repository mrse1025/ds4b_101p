# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_panda_extensions.database import collect_data

# DATA

df = collect_data()

# 1.0 DATE BASICS
df['order_date']

# Conversion
type("2011-01-07")

pd.to_datetime("2011-01-07").to_period(freq = "W").to_timestamp() #converts str to date, creates a period, converts to time stamp


# Accessing elements

# Months
df.order_date #time stamp data

df.order_date.dt.month #returns applicable months
df.order_date.dt.month_name() 
# Days
df.order_date.dt.day #returns numeric days in data set

#Year
df.order_date.dt.year

# DATE MATH
import datetime
today = datetime.date.today()

pd.to_datetime(today + pd.Timedelta(" 1 day"))

df.order_date + pd.Timedelta(365, "d")

#Duration Time Deltas
today = datetime.date.today()
one_year_from_today = today + pd.Timedelta(365, "d")

(one_year_from_today - today) / pd.Timedelta(30, "d")
pd.Timedelta(one_year_from_today - today) / np.timedelta64(1, "M")


# DATE SEQUENCES
#shows number of days given a specific frequency or start and end date with frequency.
pd.date_range(
    start = pd.to_datetime("2011-01"), 
    #periods = 10,
    end = pd.to_datetime("2011-12-31"),
    freq = "1W"
)


# PERIODS
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series


# Convert to Time Stamp
df.order_date.dt.to_period(freq = "D")
df.order_date.dt.to_period(freq = "M")
df.order_date.dt.to_period(freq = "Q")
df.order_date.dt.to_period(freq = "Y").dt.freq

df.order_date.dt.to_period(freq = "M").dt.to_timestamp()

# Get the Frequency



# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Using kind = "timestamp", single time series 
bike_sales_m_df = df[['order_date', 'total_price']] \
    .set_index("order_date") \
    .resample("MS", kind = "timestamp") \
    .sum()

bike_sales_m_df 

# Using kind = "period"
#Had issues with overlapping time stamp, needed pd.Grouper to set period. 

bike_sales_cat2_m_wide_df = df[['category_2','order_date', 'total_price']] \
    .groupby(['category_2', 
              pd.Grouper(key = 'order_date', freq = 'M',origin = 'start'),]) \
    .agg(np.sum) \
    .unstack("category_2") \
    .reset_index()\
    .assign(order_date = lambda x: x['order_date'].dt.to_period("M"))

bike_sales_cat2_m_wide_df  



# MEASURING CHANGE

# Difference from Previous Timestamp

#  - Single (No Groups)
#creates intermediate column and shows difference 
bike_sales_m_df \
    .assign(total_price_lag1 = lambda x: x['total_price'].shift(1)) \
    .assign(difference = lambda x: x.total_price - x.total_price_lag1) \
    .plot(y = 'difference')

#without generating intermediate columns, shows percent change

bike_sales_m_df \
    .apply(lambda x: (x- x.shift(1)) / x.shift(1)) \
    .plot()

#  - Multiple Groups: Key is to use wide format with apply

bike_sales_cat2_m_wide_df \
    .apply(lambda x: x - x.shift(1))\
    .plot()
    

#  - Difference from First Timestamp

bike_sales_m_df \
    .apply(lambda x: (x-x[0])) \
    .plot()

bike_sales_cat2_m_wide_df \
    .apply(lambda x: (x-x[0])) \
    .plot()


# CUMULATIVE CALCULATIONS

bike_sales_m_df \
    .resample('YS') \
    .sum() \
    .cumsum() \
    .reset_index() \
    .assign(order_date = lambda x: x.order_date.dt.to_period()) \
    .set_index("order_date") \
    .plot(kind = "bar")
    
bike_sales_cat2_m_wide_df \
    .set_index("order_date") \
    .resample('Y') \
    .sum() \
    .cumsum() \
    .plot(kind = "bar",stacked = True)

# ROLLING CALCULATIONS

# Single
#pd.Series.rolling(): window size; use the same unit measure from the data. 
# window size only, right aligns,
# center = True, center aligns the rolling average,
# min_periods, reduces the number of missing values, this creates a partial window 
bike_sales_m_df \
    .assign(
        total_price_roll12 = lambda x : x['total_price']\
            .rolling(
                window = 12, 
                center = True, 
                min_periods = 1
                ) \
            .mean()
    ) \
    .plot()

# Groups - Can't use assign(), we'll use merging

bike_sales_cat2_m_wide_df \
    .set_index('order_date') \
    .apply(
        lambda x: x.rolling(
            window = 24,
            center = True,
            min_periods = 1
        ) \
        .mean()
    ) \
    .rename(lambda x: x + "_roll_24", axis = 1) \
    .merge(
        bike_sales_cat2_m_wide_df,
        how = "right",
        left_index = True, 
        right_index = True
    ) \
    .plot()



