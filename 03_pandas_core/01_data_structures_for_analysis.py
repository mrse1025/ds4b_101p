# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 3 (Pandas Core): Data Structures ----

# IMPORTS ----
import pandas as pd
import numpy as np

from my_panda_extensions.database import collect_data 

df = collect_data()

df

# 1.0 HOW PYTHON WORKS - OBJECTS

# Objects: everything in python is an object. Object and classes have methods and attributes
type(df)


# Objects have classes
#class = dataframe 
type(df).mro()

# Objects have attributes
df.shape #this gives the attributes
df.columns #lists column names, this is an attribute of the dataset 

# Objects have methods
df.query("model == 'Jekyll Carbon 2'")



# 2.0 KEY DATA STRUCTURES for analysis

# - PANDAS DATA FRAME
type(df) #pandas core dataframe

# - PANDAS SERIES

type(df['order_date']) #pandas core series


# - NUMPY
type(df['order_date'].values).mro()#numpy array

# -Data Types

type(df['price'].values).mro()
df['price'].values.dtype
df['order_date'].values.dtype



# 3.0 DATA STRUCTURES - PYTHON

# Dictionaries {}

d = {'a' :1}
type(d)

d.keys()
d.values()

d['a']


# Lists []
l = [1, "A", [2, "B"]]
l[0]
l[1]
l[2]

list(d.values())

list(d.values())[0]


# Tuples immutable object, descriptor 
type(df.shape).mro()
t = (10, 20)
t[0]
t[1]
# Base Data Types
1.5
type(1.5).mro
1
type(1).mro
df.total_price #int64 is how many bytes it takes up
df.total_price.dtype
df.total_price.values

type(df['model'].values[0])



# Casting
model = "Jekyll Carbon 2"
price = 6070

f"The first model is: {model}, cost is {price}"

#with coersion 
str(price) + " this is the price of the first model"

int("50%".replace("%", ""))

#Casting things to list: shows low level to higher level objects (pandas series/dataframes)
type(range(1, 50)).mro()
#range is a generator
list(range(1,50)) #needs to go one passed the end point to include both start and end values
r = list(range(1, 51))
np.array(r)
pd.Series(r)
pd.Series(r).to_frame() #shows 0 indexing

# Converting Column Data Types

df['order_date'].astype('str') #converts to object class

df['order_date'].astype('str').str.replace("-", "/")

