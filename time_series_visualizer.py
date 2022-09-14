import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data
df = pd.read_csv("fcc-forum-pageviews.csv", parse_dates = ['date'], index_col = "date")

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
low, high = df["value"].quantile([0.025, 0.975])
mask_pcount = df["value"].between(low, high, inclusive="both")
df = df[mask_pcount]

# Draw line plot
def draw_line_plot():

    fig, ax = plt.subplots(figsize = (20, 10))
    plt.plot(df, label = 'lineplots', color = 'r', linewidth = 1.0)
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig
    fig.savefig('line_plot.png')
    return fig

# Draw bar plot that show average daily page views for each month grouped by year. 
def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = pd.pivot_table(df,
                            values = 'value',
                            index = df.index.year,
                            columns = df.index.month,
                            aggfunc = np.mean
                          )
    ax = df_bar.plot(kind = 'bar');
    fig = ax.get_figure()
    fig.set_size_inches(20,10)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    
    handles, labels = ax.get_legend_handles_labels()
    labels = [datetime.date(1900, int(monthinteger), 1).strftime('%B') for monthinteger in labels]
    ax.legend(labels = labels).set_title("Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots    
    df_box = df.copy()
    df_box.reset_index(inplace = True)
    df_box['Year'] = pd.DatetimeIndex(df_box['date']).year
    df_box['Month'] = pd.DatetimeIndex(df_box['date']).month_name().str[:3]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
              'Sep', 'Oct', 'Nov', 'Dec']

    # Draw box plots using Seaborn    
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    sns.boxplot(x = df_box['Year'], y = df_box['value'].rename('Page Views'),
                ax = axes[0]).set(title = 'Year-wise Box Plot (Trend)')

    sns.boxplot(x = df_box['Month'], y = df_box['value'].rename('Page Views'),
                order = months,
                ax = axes[1]).set(title = 'Month-wise Box Plot (Seasonality)')

    # Save image and return fig
    fig.savefig('box_plot.png')
    return fig
