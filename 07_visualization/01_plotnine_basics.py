# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plot Anatomy ----

# Imports
import pandas as pd
import numpy as np
 
from my_panda_extensions.database import collect_data
from my_panda_extensions.timeseries import summarize_by_time
from my_panda_extensions.forecasting import arima_forecast

from plotnine import * #all functions are imported
import plotnine
from plotnine.geoms import geom_col

from mizani.formatters import dollar, dollar_format
# Data

df = collect_data()

# VISUALIZATION ----

# Step 1: Data Summarization
bike_sales_y_df = df \
    .summarize_by_time(
        date_column =  'order_date',
        value_column = 'total_price',
        rule = 'Y',
        kind = 'timestamp'
    ) \
    .reset_index()

# Step 2: Plot ----
# - Canvas: Set up column mappings
# - Geometries: Add geoms
# - Format: Add scales, labs, theme

    #Canvas
g = (
    ggplot(bike_sales_y_df, aes(x = 'order_date', y = 'total_price'))
    + geom_col(fill = '#2C3E50')
    + geom_smooth(
        method = 'lm', 
        se = False,
        color =  "dodgerblue")
    + expand_limits(y = [0, 20e6])
    + scale_y_continuous(
        labels = dollar_format(big_mark = ",", digits= 0)
    )
    + scale_x_datetime(date_lables ="%Y", date_breaks = "2 years")
    + labs(
        title = "Revenue by Year", 
        x = "",
        y = "Revenue"
    )
    +theme_minimal()
)
g

# Saving a plot ----
g.save(filename = "07_visualization/bike_sales_y.jpg")


# What is a plotnine plot? ----

