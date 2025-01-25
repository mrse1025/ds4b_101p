# IMPORTS ----
import sqlalchemy as sql
from sqlalchemy.types import String, Numeric
from sqlalchemy import Table, MetaData
import pandas as pd
import pandas_flavor as pf

#Collect Data ----

# FUNCTION DEFINITION ----
def collect_data(conn_string = "sqlite:///00_database/bike_orders_database.sqlite"):
    """
    Collects and combines the bike orders data.
    
    Args:
    conn_string(str, optional): A SQLalchemy connection string to find the database. Defaults to 
    "sqlite:///00_database/
    bike_order_database.sqlite".
    
    Returns:
    Datafram: A pandas data frame that combines all data from tables: 
    -orderlines: Trasacations data
    -bikes: Product data
    -bikeshops: Customer data
    
    """
    
    #Body
    
    #1.0 Connect to Database
    engine = sql.create_engine(conn_string)
    
    conn = engine.connect()
    
    #accessing the data
    table_names = ['bikes', 'bikeshops', 'orderlines']
    
    data_dict = {}
    for table in table_names: 
        data_dict[table] = pd.read_sql(f"SELECT * FROM {table}", con = conn)
    
    conn.close()
    
    #2.0 Combining data
    
    joined_df = pd.DataFrame(data_dict['orderlines']) \
        .merge(
            right = data_dict['bikes'],
            how = 'left', 
            left_on = 'product.id',
            right_on = 'bike.id'
        ) \
        .merge(
            right = data_dict['bikeshops'],
            how = "left",
            left_on = "customer.id", 
            right_on= "bikeshop.id"  
        )
            
    # 3.0 Cleaning data
    df = joined_df
    
    df['order.date'] = pd.to_datetime(joined_df['order.date'])
    
    temp_df = df['description'].str.split(" - ", expand= True)
    df['category.1'] = temp_df[0]
    df['category.2'] = temp_df[1]
    df['frame.material'] = temp_df[2]
    
    temp_df = df['location'].str.split(", ", expand = True)
    df['city'] = temp_df[0]
    df['state'] = temp_df[1]
    
    df['total.price'] = df['quantity'] * df['price']
    
    df.columns
    
    cols_to_keep_list = [
        'order.id', 'order.line', 'order.date',  
        'quantity', 'price', 'total.price', 
        'model','category.1', 'category.2','frame.material', 
        'bikeshop.name','city', 'state'
        ]
   
    df = df[cols_to_keep_list]
    
    df.columns = df.columns.str.replace(".", "_")
    
    df.info()
    
    return df

#Prep data
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

#Write to database
def write_forecast_to_database(
    data, id_column, date_column, 
    conn_string = 'sqlite:///00_database/bike_orders_database.sqlite',
    table_name = "forecast", 
    if_exists = "fail",
    **kwargs
):
    """Writes the forecast table to the database
    Args:
        data (DataFrame): An ARIMA forecast data frame
        id_column (str): A single column name specifying a unique identifier for the time series
        date_column (str): A single column name specifying the date column.
        conn_string (str, optional): A connection string to database to be updated. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".
        table_name (str, optional): Table name for the table to be created or modified. Defaults to "forecast".
        if_exists (str, optional): Used to determine how the table is updated if the table exists. Passed to pandas.to_sql(). Defaults to "fail".
        **kwargs: Additional arguments passed to pandas.to_sql().
    See also:
        - my_pandas_extensions.forecasting.arima_forecast()
    """
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

# Read from Database

def read_forecast_from_database(
    conn_string = 'sqlite:///00_database/bike_orders_database.sqlite',
    table_name = "forecast", 
    **kwargs
):
    """Read a forecast from the database
    Args:
        conn_string (str, optional): A slqalchemy connection string to find the database. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".
        table_name (str, optional): The SQL table containing the forecast. Defaults to "forecast".
    Returns:
        DataFrame: A pandas data frame with the following columns:
            - id: A unique identifier for the time series
            - date: A date column
            - value: The actual values
            - prediction: The predicted values
            - ci_lo: The lower confidence interval
            - ci_hi: the upper confidence interval
    """
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