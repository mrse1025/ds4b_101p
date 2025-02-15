# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 9 (Jupyter Automated Reporting): Papermill Automation ----

# IMPORTS ----
import pandas as pd
import numpy as np

import papermill as pm
import pathlib
import os

from my_panda_extensions.database import read_forecast_from_database


# COLLECT DATA ----
df = read_forecast_from_database()



# 1.0 SELECTING REPORT ID'S ----
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

id_sets[0]

# 2.0 SETUP DIRECTORY ----

# Make the report directory if doesn't already exist
directory = '09_jupyter_papermill/reports/'

dir_path = pathlib.Path(directory)

dir_path.absolute()
dir_path.name

#os.mkdir(dir_path) 

os.path.isdir(dir_path)
os.path.isdir("test")

dir_exists = os.path.isdir(dir_path)

if not dir_exists:
    print("Making directory at {str(dir_path.absolute())}")
    os.mkdir(dir_path)


# 3.0 MAKE JUPYTER TEMPLATE ----
# - Convert Analysis to a Papermill Template
# - Parameterize key variables:
#   - ids
#   - title
#   - data: Note that data will be passed as json

# 4.0 PAPERMILL ----

# Iterating without a loop
#Key variables 

i = 3
template_path = pathlib.Path("09_jupyter_papermill/template/jupyter_report_template.ipynb")

output_path = pathlib.Path(f"09_jupyter_papermill/reports/sales_report_{i}.ipynb")

params = {
    'ids': id_sets[i],
    'title': f"Sales Report {i}",
    'data': df.to_json()
}

#data_from_json = pd.read_json('C:/Users/mrse1025/OneDrive/Desktop/ds4b_101p/00_data_raw/data.json')

# Iterating with for-loop and enumerate()
pm.execute_notebook(
    input_path=template_path,
    output_path=output_path,
    parameters=params,
    report_mode=True
)



