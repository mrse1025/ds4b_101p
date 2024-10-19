# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# IMPORTS
import pandas as pd
from my_panda_extensions.database import collect_data
from ydata_profiling import ProfileReport,profile_report

df = collect_data()
df


# PANDAS PROFILING

# Get a Profile
profile = ProfileReport(
    df = df
)

profile

# Sampling - Big Datasets

df.profile_report()

df.sample(frac = 0.5).profile_report() #reduce down dataset for faster processing

df.profile_report()
# Pandas Helper
#?pd.DataFrame.profile_report


# Saving Output
df.profile_report().to_file("04_time_series/profile_report.html") #use show preview to render output

# VSCode Extension - Browser Preview



