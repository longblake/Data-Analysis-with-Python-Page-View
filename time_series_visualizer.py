import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#fix for error that arose in boxplot 
if not hasattr(np, 'float'):
    np.float = float

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col="date", parse_dates=True)
print(df)

value = df.columns[0]

# Calculate the exact percentile values
lower_bound = df[value].quantile(0.025)
upper_bound = df[value].quantile(0.975)

# Filter the dataframe 
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]
cleaned_df = df

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(18, 6))
    ax.plot(cleaned_df.index, cleaned_df[value], ls="-", color="r")
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = cleaned_df.copy()

    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month
    grouped = df_bar.groupby(['Year', 'Month'])[value].mean().unstack()
    month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                  'July', 'August', 'September', 'October', 'November', 'December']
    grouped = grouped.reindex(columns=range(1, 13))
    grouped.columns = month_names[:len(grouped.columns)]

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(7,6))
    grouped.plot(kind="bar", ax=ax)
    ax.set_xlabel('Years')
    ax.set_ylabel('Average Page Views')
    ax.legend(title="Months", loc='upper left', fontsize='small', framealpha=0.7)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = cleaned_df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]   
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Draw box plotrs 
    fig, axes = plt.subplots(1, 2, figsize=(18, 6))

    # Plot 1
    sns.boxplot(x='year', y=value, data=df_box, ax=axes[0])
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

   # Plot 2
    sns.boxplot(x='month', y=value, data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
