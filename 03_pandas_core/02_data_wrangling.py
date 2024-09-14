# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Week 2 (Data Wrangling): Data Wrangling ----

# IMPORTS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_panda_extensions.database import collect_data

# DATA
df = collect_data()


# 1.0 SELECTING COLUMNS

# Select by name
df[['order_date', 'order_id', 'order_line']]

#single [] is a series, [[]] is a dataframe

# Select by position
df.iloc[:, 0:3]

df.iloc[:, -3:]

# Select by text matching
df.filter(regex = "(^model)|(^cat)", axis= 1) #^ is starts with, or beginning and $ is ends with

df.filter(regex= "(price$)|(date$)", axis = 1)

# Rearranging columns
l = df.columns.tolist()
l.remove('model')
l
df[['model', *l]] #moving one column to the front after removing it 

#multiple approach, still removed one column at a time and move column to the front
l = df.columns.tolist()
l.remove('model')
l.remove('category_1')
l.remove('category_2')

df[['model', 'category_1', 'category_2', *l]]

l = df.columns.tolist()
l

cols_to_front= ['model', 'category_1', 'category_2']

#list comprehension
l2 = [col for col in l if col not in cols_to_front]

df[[*cols_to_front, *l2]]

# Select by data types

df.info()
#moving columns by data frame selection 

df1 = df.select_dtypes(include= object)  #with or without ''

df2 = df.select_dtypes(exclude = 'object')

pd.concat([df1, df2], axis = 1) #column binds data

df1 = df[['model', 'category_1', 'category_2']]

df2 = df.drop(['model', 'category_1', 'category_2'], axis = 1) #axis is defaulted to 0, meaning index, axis = 1 is column wise binding

pd.concat([df1, df2], axis =1)

# Dropping Columns (De-selecting)
df.drop(['model', 'category_1', 'category_2'], axis = 1)


# 2.0 ARRANGING ROWS ----
df.sort_values('total_price')

df.sort_values('order_date', ascending= False)

df['price'].sort_values(ascending= False)

# 3.0 FILTERING  ----

# Simpler Filters
df.order_date >= pd.to_datetime("2015-01-01")
df[df.order_date >= pd.to_datetime("2015-01-01")]

df[df.model == "Trigger Carbon 1"]

df[df.model.str.startswith("Trigger")]

df[df.model.str.contains("Carbon")]
# Query

price_threshold1 = 5000

price_threshold2 = 1000

df.query("(price >= @price_threshold1) | (price <= @price_threshold2)")
df.query(f"price >= {price_threshold1}")

# Filtering Items in a List
df['category_2'].unique()
df['category_2'].value_counts()
df[df['category_2'].isin(['Triathalon', 'Over Mountain'])]

df[ ~df['category_2'].isin(['Triathalon', 'Over Mountain'])]

# Slicing
#row-wise slicing

df[:5] #first 5, from 0 to 4
df.head(5)
df.tail(5)

# Index Slicing
df.iloc[0:5, [1,3,5]] #can slice row and column wise

df.iloc[0:5, :] #first 5 rows and all columns

df.iloc[ : , [1,3,5]] #all rows only columns 1, 3, 5 
 
# Unique / Distinct Values
df[['model', 'category_1', 'category_2', 'frame_material']]\
   .drop_duplicates()

df['model'].unique()
# Top / Bottom

df.nlargest(n = 20, columns= 'total_price')

df['total_price'].nlargest(n = 20)
df['total_price'].nsmallest(n=20)

# Sampling Rows

df.sample(n = 10, random_state= 123) #random state is same as set seed

df.sample(frac = 0.10, random_state= 123) #10% of data returned


# 4.0 ADDING CALCULATED COLUMNS (MUTATING) ----


# Method 1 - Series Notations
df2 = df.copy()

df2['new_col'] = df2['price'] *df2['quantity']
df2

df2['new_col_2'] = df2['model'].str.lower()
df2
# Method 2 - assign (Great for method chaining)
df.assign(frame_material = lambda x: x['frame_material'].str.lower())

df.assign(frame_material_lower = lambda x: x['frame_material'].str.lower())

df[['model', 'price']] \
   .drop_duplicates() \
   .assign(price = lambda x: np.log(x['price'])) \
   .set_index('model') \
   .plot(kind = 'hist') 
   

   
# Adding Flags (True/False) booleans

#text mining
"Supersix Evo Hi-Mod Team".lower().find("supersix") >=0


df.assign(flag_supersix = lambda x: x['model'].str.lower().str.contains("supersix"))

df['model'].str.lower().str.contains("supersix") 


# Binning
pd.cut(df.price, bins = 3, labels = ['low', 'medium', 'high']).astype("str")

df[['model', 'price']] \
   .drop_duplicates() \
   .assign(price_group = lambda x: pd.cut(x.price, bins = 3)) \
   .pivot(
      index = 'model',
      columns = 'price_group',
      values = 'price'
   ) \
   .style.background_gradient(cmap = 'Blues')
   
pd.qcut(df.price, q =[0, 0.3, 0.66,1], labels = ['low', 'medium', 'high'])

pd.cut(df.price, bins = 3, labels = ['low', 'medium', 'high']).astype("str")

df[['model', 'price']] \
   .drop_duplicates() \
   .assign(price_group = lambda x: pd.qcut(x.price, q = 3)) \
   .pivot(
      index = 'model',
      columns = 'price_group',
      values = 'price'
   ) \
   .style.background_gradient(cmap = 'Blues')

# 5.0 GROUPING  ----

# 5.1 Aggregations (No Grouping)
df[['total_price']].sum().to_frame()
#selects on numeric cols
df \
   .select_dtypes(exclude = ['object']) \
   .drop('order_date', axis = 1) \
   .sum()
   
df \
   .select_dtypes(exclude = ['object']) \
   .drop('order_date', axis = 1) \
   .agg([np.sum, np.mean, np.std])
   
df.agg(
   {
      'quantity': np.sum, 
      'total_price': [np.sum, np.mean]
   }
)
# Common Summaries

df['model'].value_counts()

df[['model', 'category_1']].value_counts()

df.nunique()

df.isna()

df.isna().sum()


# 5.2 Groupby + Agg
df
df\
   .groupby(['city','state'])\
   .agg(dict(quantity    = np.sum,
             total_price = [np.sum, np.mean]))

# Get the sum and median by groups
summary_df_1 = df[['category_1','category_2', 'total_price']] \
   .groupby(['category_1', 'category_2']) \
   .agg([np.sum, np.mean])  \
   .reset_index()
   
summary_df_1

# Apply Summary Functions to Specific Columns
summary_df_2 = df[['category_1', 'category_2', 'total_price', 'quantity']] \
   .groupby(['category_1', 'category_2']) \
   .agg({
        'quantity' : np.sum, 
        'total_price': np.sum
        }
      ) \
   .reset_index()
   
summary_df_2

# Detecting NA
summary_df_1.columns #mulit-level index, this created tuples 
summary_df_1.isna().sum() #shows na's or 0 if none are missing
summary_df_1.isna().sum().index #on indicies and not as col counts

# 5.3 Groupby + Transform (Apply Function)
# - Note: Groupby + Assign does not work. No assign method for groups.
#time series analysis 
summary_df_3 = df[['category_2', 'order_date', 'total_price', 'quantity']]\
   .groupby(['category_2',pd.Grouper(key='order_date',freq='W',origin='start'),])\
   .agg(np.sum)\
   .reset_index()     
  
#Standardizes total price column    
summary_df_3 \
   .set_index('order_date') \
   .groupby('category_2') \
   .apply(lambda x: (x.total_price - x. total_price.mean()) / x.total_price.std()) \
   .reset_index() \
   .pivot(
      index = "order_date",
      columns = "category_2",
      values = "total_price"
   ) \
   .plot()
   
#Standardizing mulitple columns
summary_df_3  \
   .set_index(['order_date','category_2']) \
   .apply(lambda x:(x - x.mean())/ x.std()) \
   .reset_index()

# 5.4 Groupby + Filter (Apply Function)

df.tail(5)

summary_df_3 \
   .groupby('category_2') \
   .tail(5)
   
summary_df_3 \
   .groupby('category_2') \
   .apply(lambda x: x.iloc[10:20])

# 6.0 RENAMING ----

# Single Index
summary_df_2 \
   .rename(columns = dict(category_1 = "Category_1"))

summary_df_2 \
   .rename(columns = lambda x: x.replace("_", " ").title())
   
# Targeting specific columns
summary_df_2 \
   .rename(columns = {'total_price' : 'Revenue' })

# - Mult-Index

["_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()]

summary_df_1 \
   .set_axis(["_".join(col).rstrip("_") for col in summary_df_1.columns.tolist()], 
             axis = 1)

# 7.0 RESHAPING (MELT & PIVOT_TABLE) ----

# Aggregate Revenue by Bikeshop by Category 1 


# 7.1 Pivot & Melt 

# Pivot (Pivot Wider)


# Melt (Pivoting Longer)



# 7.2 Pivot Table (Pivot + Summarization, Excel Pivot Table)



# 7.3 Stack & Unstack ----

# Unstack - Pivots Wider 1 Level (Pivot)

# Stack - Pivots Longer 1 Level (Melt)


# 8.0 JOINING DATA ----


# Merge (Joining)


# Concatenate (Binding)

# Columns 


# Rows 



# 9.0 SPLITTING (SEPARATING) COLUMNS AND COMBINING (UNITING) COLUMNS

# Separate


# Combine



# 10.0 APPLY 
# - Apply functions across rows 



# 11.0 PIPE 
# - Functional programming helper for "data" functions





