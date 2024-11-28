# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): Introduction to Forecasting ----

# Imports

import pandas as pd
import numpy as np

from my_panda_extensions.database import collect_data
from my_panda_extensions.timeseries import summarize_by_time 

df = collect_data()

# Sktime Imports
from sktime.forecasting.arima import AutoARIMA
import pmdarima as pm #additional package needed to get arima to work
#Visualization plot_series(), *: means can add as many args as needed
from sktime.utils.plotting import plot_series

# 1.0 DATA SUMMARIZATIONS ----
bike_sales_m_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = 'total_price',
        rule = "M" 
    )
    
bike_sales_cat2_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups = 'category_2', 
        rule = "M"
    )

# 2.0 SINGLE TIME SERIES FORECAST ----
bike_sales_m_df.plot()

bike_sales_m_df

y = bike_sales_m_df['total_price'] #converts to pandas series

h = 24
forecaster = AutoARIMA(sp = 12) #AutoARIMA is not good at determining if data has seasonality

forecaster.fit(y)
#predictions
forecaster.predict(fh = np.arange(1,h+1))


#Adding confidence intervals
predictions = forecaster.predict(fh= np.arange(1,h+1))

predictions_ci = forecaster.predict_interval(fh = np.arange(1, h+1), coverage=0.80)
predictions_ci.columns =['lower','upper']
predictions
lower = predictions_ci[['lower']]
upper = predictions_ci[['upper']]




plot_series(y,
            predictions,
            lower,
            upper
)

# 3.0 MULTIPLE TIME SERIES FORCAST (LOOP) ----


