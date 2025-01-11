# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plot Automation ----

# Imports
import pandas as pd
import numpy as np
from plotnine import *
from mizani.formatters import *
#from plydata.cat_tools import *

from my_panda_extensions.database import collect_data
from my_panda_extensions.timeseries import summarize_by_time
from my_panda_extensions.forecasting import arima_forecast

# Workflow until now
df = collect_data()
arima_forecast_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups = 'category_1',
        rule = 'M',
        kind = 'timestamp',
        wide_format = True
    ) \
    .arima_forecast(
        h = 12, 
        sp = 1
    )
# 1.0 FORECAST VISUALIZATION ----

# Step 1: Data preparation for Plot
df_prepped= arima_forecast_df \
    .melt(
        id_vars = ['order_date', 'category_1', 'ci_lo', 'ci_hi'],
        value_vars = ['value', 'predictions'], 
        value_name = '.value'
    ) \
    .rename({'.value': 'value'}, axis = 1)


# Step 2: Plotting
ggplot(df_prepped, mapping = aes(x = 'order_date', y = 'value', color = 'variable')) \
 + geom_line() \
 + geom_ribbon(mapping = aes(ymin = 'ci_lo', ymax = 'ci_hi'),
               alpha = 0.2, 
               color = None) \
 + facet_wrap('~category_1', scales = 'free_y', ncol =1 ) \
 + scale_x_datetime(labels = date_format('%Y')) \
 + scale_y_continuous(labels = label_dollar(big_mark= ",", precision= 0)) \
 + scale_color_manual(values = ['red', '#2c3e50']) \
 + theme_minimal() \
 + theme(
     legend_position= "none", 
     subplots_adjust={'wspace': 0.25},
     figure_size= (16, 8)
 ) \
 + labs( title = "Forecast Plot", 
        x = "Date",
        y = "Revenue")



# 2.0 PLOTTING AUTOMATION ----
# - Make plot_forecast()

data = arima_forecast_df
id_column = 'category_2'
date_column = 'order_date'
required_columns = [id_column, date_column, 'value', 'predictions', 'ci_lo', 'ci_hi']

# Function Development 
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
    figure_size = (16, 8)
):
    #Data Wrangling
    df_prepped= data \
        .loc[:, required_columns] \
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
       + labs( title = "Forecast Plot", 
            x = "Date",
            y = "Revenue"
        )

    return g

# Testing 

arima_forecast_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups = 'category_2',
        rule = 'M',
        kind = 'timestamp',
        wide_format = True
    ) \
    .arima_forecast(
        h = 12, 
        sp = 1
    )

# plot_forecast(data = arima_forecast_df, 
#                 id_column = 'category_2', 
#                 date_column = 'order_date',
#                 facet_ncol= 1,
#                 facet_scales= None,
#                 date_breaks= "2 year",
#                 figure_size= (8,8))

from my_panda_extensions.forecasting import plot_forecast
arima_forecast_df.plot_forecast(
                id_column = 'category_2', 
                date_column = 'order_date', 
                facet_ncol= 3)









