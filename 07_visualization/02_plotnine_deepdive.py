# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plotnine Deep-Dive ----

# Imports
import mizani.formatters
import pandas as pd
import numpy as np
import matplotlib
import mizani 

from my_panda_extensions.database import collect_data
from my_panda_extensions.timeseries import summarize_by_time
import plotnine
from plotnine import *




# Matplotlib stylings


# Data
df = collect_data()
df


# 1.0 Scatter Plots ----
# - Great for Continuous vs Continuous

# Goal: Explain relationship between order line value
#  and quantity of bikes sold

#Step 1: Data Manipulation
quantity_total_price_by_order_df = df [['order_id',
                                        'quantity',
                                        'total_price']] \
        .groupby('order_id') \
        .sum()\
        .reset_index()

 #Step 2: Data Visualization
(
    ggplot(data=quantity_total_price_by_order_df, mapping=aes(x='quantity', y='total_price'))
    + geom_point(alpha=0.2)
    + labs(title='Order Line Value vs Quantity Sold', x='Quantity Sold', y='Order Line Value')
    + geom_smooth(method='lm', color='blue')
)

# 2.0 Line Plot ----
# - Great for time series

# Goal: Describe revenue by Month, expose cyclic nature

# Step 1: Data Manipulation
bike_sales_m_df= df\
   .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        rule = 'M',
        kind = 'timestamp')\
        .reset_index()


# Step 2: Plot
(
        ggplot(data = bike_sales_m_df, mapping=aes(x='order_date', y='total_price')
        )
        + geom_line()
        + geom_smooth(method = 'lm', color = 'blue', se = False)
        + geom_smooth(method = 'loess', color = 'red', se = False)
)


# 3.0 Bar / Column Plots ----
# - Great for categories

# Reorder categories by total_price
# Goal: Sales by Descriptive Category

# Step 1: Data Manipulation
bike_sales_cat2_df =df \
  .groupby('category_2')\
  .agg(
      {'total_price':np.sum}
  ) \
  .reset_index() \
  .sort_values('total_price', ascending = False) \
  .assign(
        category_2 = lambda x: pd.CategoricalIndex(x['category_2']).reorder_categories(
            df.groupby("category_2")["price"].median().sort_values().index
            
    )
)

# Aside: Categorical Data (pd.Categorical)
# - Used frequently in plotting to designate order of categorical data

# Step 2: Plot
(
    ggplot(mapping = aes('category_2', 'total_price'), 
           data = bike_sales_cat2_df) +
           geom_col(fill = "#2c3e50") +
           coord_flip() +
           theme_minimal()
)


# 4.0 Histogram / Density Plots ----
# - Great for inspecting the distribution of a variable

# Goal: Unit price of bicycles

# Histogram ----

# Step 1: Data Manipulation
#investigate the models 
unit_price_by_frame_df = df[['model', 'frame_material', 'price']] \
    .drop_duplicates ()

# Step 2: Visualize
g_canvas = ggplot(data = unit_price_by_frame_df, 
           mapping = aes("price", fill = "frame_material")) 

g2= g_canvas + geom_histogram(bins = 25, 
                          color = "white")

g1 = g_canvas + geom_histogram(bins = 25, 
                               color = "white", 
                               fill = "#2c3e50")
g2 + facet_grid(['frame_material'])

# Density ----
g3 = g_canvas +geom_density(alpha = 0.3)

g3 + facet_wrap("frame_material", ncol = 1)


# 5.0 Box Plot / Violin Plot ----
# - Great for comparing distributions

# Goal: Unit price of model, segmenting by category 2

# Step 1: Data Manipulation
unit_price_by_cat2_price = df[['model', 'category_2', 'price']] \
    .drop_duplicates() \
    .assign(
        category_2 = lambda x: pd.CategoricalIndex(x['category_2']).reorder_categories(
            df.groupby("category_2")["price"].median().sort_values().index
            
    )
)

# Step 2: Visualize

# Box Plot
(
    ggplot(aes('category_2', 'price'), unit_price_by_cat2_price)
    + geom_boxplot () 
    + coord_flip()
)


# Violin Plot & Jitter Plot
(
    ggplot(aes('category_2', 'price'), unit_price_by_cat2_price)
    + geom_violin()
    + geom_jitter(alpha = 0.2, color = 'red')
    + coord_flip()
)


# 6.0 Adding Text & Label Geometries----

# Goal: Exposing sales over time, highlighting outlier

# Data Manipulation
usd = mizani.formatters.currency_format(prefix = "$", big_mark = ",", precision= 0)
usd([100, 1000, 1e10])

bike_sales_y_df=df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        rule = 'Y'
     ) \
    .reset_index() \
    .assign(
        total_price_text = lambda x: usd(x['total_price'])
    )


# Adding text to bar chart
# Filtering labels to highlight a point

(
    ggplot(aes ('order_date', 'total_price'), bike_sales_y_df) \
    + geom_col(fill = "#2c3e50") 
    + geom_smooth(method = 'lm', se = False, color = 'dodgerblue')
    + geom_text(aes(label = 'total_price_text'), nudge_y = -3.2e5, color = "white"
    )
    + geom_label(
        label = "Major Demand", 
        color = "red",
        data = bike_sales_y_df[bike_sales_y_df.order_date.dt.year==2013], 
        nudge_y = 1.2e6,
        size = 10
    )
    + expand_limits(y = [0, 20e6])
    + scale_x_datetime(date_labels= "%Y")
    + scale_y_continuous(labels=usd)
    +theme_minimal()
    )


# 7.0 Facets, Scales, Themes, and Labs ----
# - Facets: Used for visualizing groups with subplots
# - Scales: Used for transforming x/y axis and colors/fills
# - Theme: Used to adjust attributes of the plot
# - Labs: Used to adjust title, x/y axis labels

# Goal: Monthly Sales by Categories

# Step 1: Format Data


# Step 2: Visualize








