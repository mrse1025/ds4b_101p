# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 8 (SQL Database Update): Forecast Automation ----

# IMPORTS ----
import pandas as pd
import numpy as np

from my_panda_extensions.database import (
    collect_data,
    write_forecast_to_database,
    read_forecast_from_database,
    prep_forecast_data_for_update
)

from my_panda_extensions.timeseries import summarize_by_time
from my_panda_extensions.forecasting import arima_forecast, plot_forecast
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="white")

df = collect_data()

# 1.0 SUMMARIZE AND FORECAST ----


# 1.1 Total Revenue ----
forecast_1_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        rule = "M",
        kind = 'timestamp'
    ) \
    .arima_forecast(
        h = 12, 
        sp = 12
    ) \
    .assign(id = "Total Revenue")\
    .prep_forecast_data_for_update(
        id_column = "id",
        date_column = "order_date"
    )

forecast_1_df \
    .plot_forecast(
        id_column = "id",
        date_column = "date"
    )

# 1.2 Revenue by Category 1 ----
forecast_2_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = "total_price",
        groups = "category_1",
        rule = "M",
        kind = "timestamp"
    ) \
    .arima_forecast(
        h = 12, 
        sp = 12
    )

forecast_2_df= forecast_2_df \
    .prep_forecast_data_for_update(
        id_column = "category_1",
        date_column = "order_date"
    )

#concatenate by stacking forecast 1 with forecast 2
pd.concat([forecast_1_df, forecast_2_df], axis = 0) \
    .plot_forecast(
        id_column = "id",
        date_column = "date"
    )    

# 1.3 Revenue by Category 2 ----
forecast_3_df = df \
    .summarize_by_time(
        date_column = "order_date",
        value_column = "total_price",
        groups = "category_2",
        rule = "M",
        kind = "timestamp"
    ) \
    .arima_forecast(
        h = 12, 
        sp = 12
    )

forecast_3_df= forecast_3_df \
    .prep_forecast_data_for_update(
        id_column = "category_2",
        date_column = "order_date"
    )

pd.concat([forecast_1_df, forecast_2_df, forecast_3_df], axis = 0) \
    .plot_forecast(
        id_column = "id",
        date_column = "date",
        facet_ncol = 3
    )

# 1.4 Revenue by Customer ----


# 2.0 UPDATE DATABASE ----


# 2.1 Write to Database ----


# 2.2 Read from Database ----
