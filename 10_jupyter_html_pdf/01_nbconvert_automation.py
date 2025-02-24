# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 10 (Jupyter Automated Reporting, Part 2): NBConvert HTML & PDF ----

# IMPORTS ----
import glob  #finds files from folders
import pathlib
from tqdm import tqdm

from traitlets.config import Config
from nbconvert.preprocessors import TagRemovePreprocessor
from nbconvert.exporters import HTMLExporter, PDFExporter
from nbconvert.writers import FilesWriter


# 1.0 NBCONVERT CONFIG ----

# Configure our tag removal
# - https://nbconvert.readthedocs.io/en/latest/removing_cells.html

c = Config()

c.TemplateExporter.exclude_input = True
c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
c.TagRemovePreprocessor.remove_all_outputs_tags = ("remove_output",)
c.TagRemovePreprocessor.remove_input_tags = ("remove_input",)
c.TagRemovePreprocessor.enabled = True


# GET FILE LIST ----

# Get file list for conversion
files = glob.glob("09_jupyter_papermill/reports/sales_forecast*.ipynb")

files

file_path = pathlib.Path(files[0])
file_path.name
file_path.stem
file_path.parents[0]


# 2.0 HTML EXPORT ----



# Iterate through files ----



# 3.0 PDF EXPORT ----
# - REQUIRES MIKETEX: https://miktex.org/download
# Stack Overflow: https://stackoverflow.com/questions/59225719/latex-error-related-to-tcolorbox-sty-not-found


    