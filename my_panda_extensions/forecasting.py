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
#Plotting 
from plotnine import *
from mizani.formatters import *
#from plydata.cat_tools import *


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
@pf.register_dataframe_method
#Plotting Function
def plot_forecast(
    data, 
    id_column, 
    date_column,
    facet_ncol = 1,
    facet_scales = 'free_y',
    date_labels = "%Y",
    date_breaks = "2 years",
    ribbon_alpha = 0.2,
    wspace = 0.25, 
    figure_size = (16, 8),
    title = "Forecast Plot",
    xlab = "Date",
    ylab = "Revenue"
):
    """Automates the forecast visualization
    Args:
        data (DataFrame): A pandas data frame that is the output
            of the arima_forecast() function.  
        id_column (str): [description]
        date_column (str): The timestamp column.
        facet_ncol (int, optional): Number of faceting columns. Defaults to 1.
        facet_scales (str, optional): One of None, "free", "free_y", "free_x". Defaults to "free_y".
        date_labels (str, optional): The strftime format for the x-axis date label. Defaults to "%Y".
        date_breaks (str, optional): Locations for the date breaks on the x-axis. Defaults to "1 year".
        ribbon_alpha (float, optional): The opacity of the confidence intervals. Defaults to 0.2.
        wspace (float, optional): The whitespace to include between subplots. Defaults to 0.25.
        figure_size (tuple, optional): The aspect ratio for the plot. Defaults to (16,8).
        title (str, optional): The plot title. Defaults to "Forecast Plot".
        xlab (str, optional): The x-axis label. Defaults to "Date".
        ylab (str, optional): The y-axis label. Defaults to "Revenue".
    Returns:
        [gglot]: Returns a plotnine ggplot object
    """
    #Data Wrangling
    df_prepped= data \
        .loc[:, [id_column, date_column, 'value', 'predictions', 'ci_lo', 'ci_hi']] \
        .melt(
            value_vars = ['value', 'predictions'], 
            id_vars = [id_column, date_column, 'ci_lo', 'ci_hi'],
            value_name = '.value'
        ) \
    .rename({'.value': 'value'}, axis = 1) 

    #Check for period convert to datetime64
    if df_prepped[date_column].dtype != 'datetime64[ns]':
        #Try changing to timestamp
        try:
            df_prepped[date_column] = df_prepped[date_column].dt.to_timestamp()
        except: 
            try:
                df_prepped[date_column]= pd.to_datetime(df_prepped[date_column])
            except:
                raise Exception("Could not aut convert 'date_column' datetime64.")
    
    #Preparing the plot
    g = ggplot(df_prepped, 
            mapping = aes(x = date_column, y = 'value', color = 'variable')) \
    + geom_line() \
    + geom_ribbon(mapping = aes(ymin = 'ci_lo', ymax = 'ci_hi'),
               alpha = ribbon_alpha, 
               color = None) \
    + facet_wrap(id_column, 
                scales = facet_scales, 
                ncol =facet_ncol) 
    g = g\
        + scale_x_datetime(date_labels= date_labels,
                             date_breaks= date_breaks) \
        + scale_y_continuous(labels = label_dollar(big_mark= ",", precision= 0)) \
        + scale_color_manual(values = ['red', '#2c3e50']
        ) 
    g = g \
       + theme_minimal() \
       + theme(
                legend_position= "none", 
            subplots_adjust={'wspace': wspace},
            figure_size= figure_size
        )\
       + labs( title = title, 
            x = xlab,
            y = ylab
        )

    return g
