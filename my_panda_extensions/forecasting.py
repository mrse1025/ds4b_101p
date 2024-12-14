# Imports
import pandas as pd
import numpy as np

# Sktime Imports
from sktime.forecasting.arima import AutoARIMA
import pmdarima as pm #additional package needed to get arima to work
#Visualization plot_series(), *: means can add as many args as needed
from sktime.utils.plotting import plot_series

#for progress bars
from tqdm import tqdm

import pandas_flavor as pf

@pf.register_dataframe_method

# FUNCTION DEVELOPMENT ----
# - arima_forecast(): Generates ARIMA forecasts for one or more time series.

#1. supple parameters, data, h: how many months in the future, args/kwargs allow for additional
#items from arima function.
 
def arima_forecast(data, h, sp, alpha = 0.05, 
                   suppress_warnings = True, 
                   *args, **kwargs
                   ):
    """_summary_

    Generates ARIMA forecasts for one or more time series.
    Args:
        data (Pandas Data Frame): 
            Data must be in wide format. 
            Data must have a time-series index 
            that is a pandas period.
        h (int): 
            The forecast horizon
        sp (int): 
            The seasonal period
        alpha (float, optional): 
            Contols the confidence interval. 
            alpha = 1 - 95% (CI).
            Defaults to 0.05.
        suppress_warnings (bool, optional): 
            Suppresses ARIMA feedback during automated model training. 
            Defaults to True.
        args: Passed to sktime.forecasting.arima.AutoARIMA
        kwargs: Passed to sktime.forecasting.arima.AutoARIMA
    Returns:
        Pandas Data Frame:
            - A single time series contains columns: value, prediction, ci_lo, and ci_hi
            - Multiple time series will be returned stacked by group
    """
    #Checks: data is df, h and sp are integers
      
    if(type(data) is not pd.DataFrame):
        raise Exception("`data` must be a pandas data frame.")
    
    if(type(h) is not int): 
        raise Exception("`h` must be an integer.")
    
    if (type(sp) is not int):
        raise Exception("`sp` must be an integer.")
      
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
    
    ret = ret.iloc[:, cols_to_keep]

    return ret