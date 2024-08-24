# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Working with SQLAlchemy ----

# IMPORTS ----
import sqlalchemy as sql
import pandas as pd

# FUNCTION DEFINITION ----
def collect_data(conn_string = "sqlite:///00_database/bike_orders_database.sqlite"):
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
    
    #2.0 Combining & cleaning data
    
    return data_dict

collect_data()