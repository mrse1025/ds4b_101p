# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plot Automation ----

# Imports
import pandas as pd
import numpy as np
from plotnine import *
from mizani.formatters import *

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

# Function Development 
        

# Testing 










