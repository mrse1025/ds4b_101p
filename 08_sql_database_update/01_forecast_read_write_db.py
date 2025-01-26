# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 8 (SQL Database Update): Forecast Write and Read Functions ----

# IMPORTS ----
import sqlalchemy as sql
from sqlalchemy.types import String, Numeric
from sqlalchemy import Table, MetaData
import pandas as pd
import numpy as np


from my_panda_extensions.database  import collect_data
from my_panda_extensions.timeseries import summarize_by_time
from my_panda_extensions.forecasting import arima_forecast, plot_forecast

df = collect_data()

# WORKFLOW ----
# - Until Module 07: Visualization
arima_forecast_df = df \
    .summarize_by_time(
        date_column='order_date',
        value_column='total_price',
        groups = 'category_2',
        rule = 'M',
        agg_function = np.sum,
        wide_format = True,
        fill_na = 0
    ) \
    .arima_forecast(
        h = 12,
        sp = 1,
        suppress_warnings = True,
        alpha = 0.05
    )

arima_forecast_df \
    .plot_forecast(
        id_column='category_2',
        date_column='order_date',
        facet_ncol=3
    )
    

# DATABASE UPDATE FUNCTIONS ----


# 1.0 PREPARATION FUNCTIONS ----
arima_forecast_df \
    .rename (
        {
            'category_2': 'id',
            'order_date': 'date',
            'total_price': 'value'
        },
        axis = 1,
    )
data = arima_forecast_df
id_column = 'category_2'
date_column = 'order_date'


def prep_forecast_data_for_update(data, id_column, date_column):
    df = data.rename (
            {
                id_column: 'id',
                date_column: 'date'
            },
            axis = 1,
        )
    
    required_col_names = ['id', 'date', 'value', 'predictions', 'ci_lo', 'ci_hi']

    if not all (pd.Series(required_col_names).isin(df.columns)):
        col_text = ', '.join(required_col_names)
        raise Exception(f"Columns must contain : {col_text}")
    
    return(df)

prep_forecast_data_for_update(
    data = arima_forecast_df,
    id_column = "category_2",
    date_column = "order_date")

# 2.0 WRITE TO DATABASE ----
def write_forecast_to_database(
    data, id_column, date_column, 
    conn_string = 'sqlite:///00_database/bike_orders_database.sqlite',
    table_name = "forecast", 
    if_exists = "fail",
    **kwargs
):
    # Prepare data
    df = prep_forecast_data_for_update(
        data= data, 
        id_column= id_column, 
        date_column = date_column)
    
    # Check format for SQL DB
    df['date']= pd.to_datetime(df['date'])
    #df.info()
    sql_dtype = {
        'id' : String(),
        'date' : String(),
        'value' : Numeric(),
        'predictions' : Numeric(),
        'ci_lo' : Numeric(),
        'ci_hi' : Numeric()
    }
    # Connect to DB 
    engine = sql.create_engine(conn_string)
    conn = engine.connect()
    # Make table
    df.to_sql(
        con= conn,
        name = table_name,
        if_exists = if_exists,
        dtype = sql_dtype
        #**kwargs
    )
    conn.close()

    pass

write_forecast_to_database(
    data = arima_forecast_df, 
    id_column="category_2", 
    date_column="order_date",
    table_name = "forecast",
    if_exists = "replace"
)
forecast_table = Table( "forecast2", MetaData(),autoload_with= engine)
forecast_table.drop(engine))
# 3.0 READ FROM DATABASE ----
def read_forecast_from_database(
    conn_string = 'sqlite:///00_database/bike_orders_database.sqlite',
    table_name = "forecast", 
    **kwargs
):

    # Connect to DB
    engine = sql.create_engine(conn_string)
    conn = engine.connect()

    # Read from the table
    df =pd.read_sql(
        f"SELECT * FROM {table_name}",
        con = conn,
        parse_dates= ['date']
    )

    # Close the connection
    conn.close()
    # Return the results
    return df
    