# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 6 (Sktime): ARIMA Automation ----

# Imports

import pandas as pd
import numpy as np

from my_panda_extensions.database import collect_data
from my_panda_extensions.timeseries import summarize_by_time

# Sktime Imports
from sktime.forecasting.arima import AutoARIMA
import pmdarima as pm #additional package needed to get arima to work
#Visualization plot_series(), *: means can add as many args as needed
from sktime.utils.plotting import plot_series

#for progress bars
from tqdm import tqdm

# Work Flow
df = collect_data()

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


# FUNCTION DEVELOPMENT ----
# - arima_forecast(): Generates ARIMA forecasts for one or more time series.

#1. supple parameters, data, h: how many months in the future, args/kwargs allow for additional
#items from arima function.

data = bike_sales_cat2_m_df #set data argument for debugging function
 
def arima_forecast(data, h, sp, alpha = 0.05, 
                   suppress_warnings = True, 
                   *args, **kwargs
                   ):
    #Checks
    
    #Handling Inputs ----
    df = data 
    
    #For Loop ----
    model_results_dict = {}
    for col in tqdm(df.columns, mininterval=0):
    #Series Extraction
        y = df[col]
    #Modeling
        forecaster = AutoARIMA(
            sp = sp, 
            suppress_warnings = suppress_warnings, 
            *args, **kwargs
        )
        
        forecaster.fit(y)
        
    #Predictions & Conf Intervals
        predictions = forecaster.predict(fh = np.arange(1, h+1))
        predictions.index.name='order_date'
        predictions.name= predictions.name[1]
    
        predictions_conf_int = forecaster.predict_interval(
        fh =np.arange(1, h+1),
        coverage = alpha
    )
    # Combine into data frame
    
        ret= pd.concat([y,predictions, predictions_conf_int], axis = 1)
        ret.columns = ["value", "predictions", "ci_lo", "ci_hi"]
    
    #Update Dictionary
    model_results_dict[col] = ret


    #Stacking each dict element on top of each other; row-wise
    model_results_df = pd.concat(model_results_dict, axis = 0)
    
    #Handle Names
    nms = [*df.columns.names, *df.index.names]
    model_results_df.index.names =nms
    # Reset Index
    ret = model_results_df.reset_index()
    
    # Drop columns containing 'level'
    cols_to_keep = ~ret.columns.str.startswith("level_")
    
    ret = ret.iloc[:,cols_to_keep]

    return ret

fcast = arima_forecast(data, h = 12, sp=1)
fcast

arima_forecast(
    bike_sales_m_df,
    h = 12,
    sp = 1
)

arima_forecast(
    bike_sales_cat2_m_df, 
    h = 12, 
    sp = 1
)