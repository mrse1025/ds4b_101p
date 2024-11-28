import pandas as pd
import numpy as np
import pandas_flavor as pf

@pf.register_dataframe_method
def summarize_by_time(data, 
                      date_column, 
                      value_column, 
                      groups = None, 
                      rule = "D", 
                      kind = "timestamp",
                      agg_func = np.sum,
                      wide_format = True,
                      fillna = 0,
                      *args,
                      **kwargs
                      ):
    """
    Applies one or more aggregating functions by Pandas Timestamp to one or more numeric column.
    Args:
        data (DataFrame): Pandas data frame with data column and value column
        date_column (str): The name of a single date or datetime column to be aggregated by. Must be datetime64 
        value_column (str, list): The names of one or more value columns to be aggregated by.
        groups (str, list, optional): One or more column names representing groups to aggregate by. Defaults to None.
        rule (str, optional): A panda frequency (offset) such as D for Daily or MS for Month start. Defaults to D.
        kind (str, optional): _description_. Defaults to "timestamp".
        agg_func (function, list, optional): One or more aggregating functions such as np.su. Defaults to np.sum.
        wide_format (bool, optional): Whether or not to return the "wide" format. Defaults to True
        fillna (int, optional): Values to fill in missing data. Defaults to 0. If missing values are desired use np.nan
        *args, **kwargs: arguments passed to pd.DataFrame.agg()

    Raises:
        TypeError: Checks that DataFrame was passed in

    Returns:
        [DataFrame]: Returns data frame that is summarized by time. 
    """
    
    #Checks
    
    if(type(data) is not pd.DataFrame):
        raise TypeError("`data` is not Pandas Data Frame.")
    
    if type(value_column) is not list:
        value_column = [value_column]
    #Body
    
    #Handle date column
    data = data.set_index(date_column)
    
    #Handle Groups
    if groups is not None:
        data = data.groupby(groups)
    
    #Handle resample
    data = data.resample(rule = rule, kind = kind)

    #Handle Aggregatio
    function_list = [agg_func] * len(value_column)
    agg_dict      = dict(zip(value_column, function_list))
    
    data = data.agg(
        func = agg_dict,
        *args, 
        **kwargs
    )
    
    #Handle Pivot Wider
    if wide_format: 
        if groups is not None: 
            data = data.unstack(groups)
            if(kind == 'period'):
                data.index = data.index.to_period() 
    data = data.fillna(fillna)
    
    return data