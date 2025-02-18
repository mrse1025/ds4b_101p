# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 9 (Jupyter Automated Reporting, Part 1): Run Reports, Version 1 ----

# IMPORTS ----
import pandas as pd
import numpy as np

import papermill as pm
import pathlib
import os

import string

from my_panda_extensions.database import read_forecast_from_database

# COLLECT DATA ----

df = read_forecast_from_database()


# SELECTING REPORT ID'S ----
ids = df['id'].unique()
ids = pd.Series(ids)
ids_total = ids[ids.str.startswith('Total')]
ids_cat_1 = ids[ids.str.startswith('Category 1')]
ids_cat_2 = ids[ids.str.startswith('Category 2')]
ids_bikeshop = ids[ids.str.startswith('Bikeshop')]
id_sets = [
    list(ids_total),
    list(ids_cat_1),
    list(ids_cat_2),
    list(ids_bikeshop)
]

id_sets



# REPORT TITLES ----
titles = [
    "Sales Forecast: Total Revenue",
    "Sales Forecast: Category 1",
    "Sales Forecast: Category 2",
    "Sales Forecast: Bikeshop"
]

titles

# 1.0 HANDLING PATHS ----

# 1.1 TEMPLATE INPUT PATH ----

def get_template_path(path = '09_jupyter_papermill/template/jupyter_report_template.ipynb'):
    return pathlib.Path(path)

get_template_path()



# 1.2 REPORT OUTPUT PATH ----
directory = "reports/"

report_title = titles[0]

report_title.lower().replace(' ', '_')

string.punctuation
file_name = report_title \
    .translate(
        str.maketrans("","", string.punctuation)
    ) \
    .lower() \
    .replace(' ', '_')

out_path = pathlib.Path(f'{directory}/{file_name}.ipynb')




# 2.0 BUILD REPORTING FUNCTION ----
# - Basic Reporting Function: Version 1
def run_reports(data, id_sets= None, report_titles = None, directory = 'reports/'):

    # Make directory if not created
    dir_path = pathlib.Path(directory)

    directory_exists = os.path.isdir(dir_path)

    if not directory_exists:
        print(f"Making directory at {str(dir_path.absolute())}")
        os.mkdir(dir_path)

    # Make the papermill reports
    for i, id_set in enumerate(id_sets):
    
    # input filename
        input_path = get_template_path()

    # output path
        report_title = report_titles[i]
    
        file_name = report_title \
        .translate(
            str.maketrans("","", string.punctuation)
        ) \
        .lower() \
        .replace(' ', '_')
        
        output_path = (f'{directory}/{file_name}.ipynb') 

        #Parameters
        params = {
        'ids': id_set,
        'title': report_title,
        'data': data.to_json()
        }

        # Papermill Execute
        pm.execute_notebook(
        input_path = input_path,
        output_path = output_path,
        parameters= params,
        report_mode= True
        )

    
    pass

from my_panda_extensions.reporting import run_reports

run_reports(data = df, 
            id_sets = id_sets, 
            report_titles=titles,
            directory = '09_jupyter_papermill/reports/'
)

i = 1