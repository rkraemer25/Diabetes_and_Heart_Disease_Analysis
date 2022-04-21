# Final Project
# Raushan Akayeva & Robert Kraemer

# analysis_for_decision.py   #

import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# change diagnosis column in df3 to bool
def change_diagnosis_to_bool(df):
    df[['diagnosis']] = df[['diagnosis']].replace(2, 1)
    df[['diagnosis']] = df[['diagnosis']].replace(3, 1)
    df[['diagnosis']] = df[['diagnosis']].replace(4, 1)
    return df

# create scatterplot for final analysis
def scatterplot_analysis(x_axis, y_axis, decision, df, file_name):
    sns.scatterplot(x=x_axis, y= y_axis, hue = decision, data=df)
    plt.savefig(file_name)

# create barplot for decision analysis
def barplot_analysis(x_axis, y_axis, decision, df, file_name):
    sns.barplot(x=x_axis, y=y_axis, hue=decision, data=df)
    plt.savefig(file_name)
