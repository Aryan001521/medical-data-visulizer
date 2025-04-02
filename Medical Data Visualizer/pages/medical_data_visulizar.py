import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd 
import seaborn as sns

# Read the CSV and store it in a DataFrame
df = pd.read_csv(r"Medical Data Visualizer\medical_examination.csv.csv")

# Add an overweight column to the data. To determine if a person is overweight, first calculate their BMI by dividing their weight in kilograms by the square of their height in meters. If that value is > 25 then the person is overweight. Use the value 0 for NOT overweight and the value 1 for overweight.
# 1 = overweight, 0 = not overweight
df['overweight'] = np.where((df['weight']/np.square(df['height']/100))>25, 1, 0)

# Normalize data by making 0 always good and 1 always bad. If the value of cholesterol or gluc is 1, set the value to 0. If the value is more than 1, set the value to 1
df['cholesterol'] = np.where(df['cholesterol'] == 1, 0, 1)
df['gluc'] = np.where(df['gluc'] == 1, 0, 1)
# print(df.head())

# Draw the Categorical Plot in the draw_cat_plot function.
def draw_cat_plot():
    # Create a DataFrame for the cat plot using pd.melt with values from cholesterol, gluc, smoke, alco, active, and overweight in the df_cat variable.
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
   
    # Group and reformat the data in df_cat to split it by cardio. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    # onvert the data into long format and create a chart that shows the value counts of the categorical features using the following method provided by the seaborn library import: sns.catplot().
    figure =sns.catplot(x="variable",kind='count',hue='value',data=df_cat,col='cardio')
    figure.set_axis_labels('variable','Total')
    # plt.show()

    # Get the figure for the output and store it in the fig variable.
    fig = figure

    #  Do not modify the next two lines.
    fig.savefig('catplot.png')
    return fig 

# Draw the Heat Map in the draw_heat_map function.
def draw_heat_map():

    # Clean the data 
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) & 
        (df['weight'] <= df['weight'].quantile(0.975))
    ]
    
    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 12))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, vmin=0, vmax=0.25, fmt='.1f', linewidths=1, annot=True, mask=mask, cbar_kws={'shrink': 0.82})

    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
draw_heat_map()
draw_cat_plot()