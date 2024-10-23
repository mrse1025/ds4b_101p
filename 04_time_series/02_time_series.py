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

# Get the Frequency



# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Using kind = "timestamp"


# Using kind = "period"



# MEASURING CHANGE

# Difference from Previous Timestamp

#  - Single (No Groups)



#  - Multiple Groups: Key is to use wide format with apply




#  - Difference from First Timestamp




# CUMULATIVE CALCULATIONS



# ROLLING CALCULATIONS

# Single

# Groups - Can't use assign(), we'll use merging




