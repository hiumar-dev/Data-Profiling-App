# import libraries
import pandas as pd 
import seaborn as sns 
from ydata_profiling import ProfileReport
# read the data
df = sns.load_dataset("diamonds")

# profile report
profile = ProfileReport(df, title="Profiling Report of Diamonds Dataset")
profile.to_file("diamonds_data_profiling.html")
profile.to_notebook_iframe()