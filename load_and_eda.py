# Final Project
# first step of analysis and preparing data for further analysis
# Raushan Akayeva & Robert Kraemer
# load_and_eda.py
from os.path import exists
import os
import numpy as np
import logging
import argparse
import requests
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load data
def load_data(file_name, url=''):
    zip_file_name = file_name.replace('csv', 'zip')

    # check if file path exists
    if os.path.exists(file_name):
        return pd.read_csv(file_name)

    # if file path does not exist and zip file exists, extract zip
    if not os.path.exists(file_name) and os.path.exists(zip_file_name):
        with zipfile.ZipFile(zip_file_name, 'r') as my_zip:
            my_zip.extractall()
            return pd.read_csv(file_name)

    # if file path and zip dont exist, download file
    if not os.path.exists(file_name) and not os.path.exists(zip_file_name):
        if url is not None:
            index = url.find('kaggle')
            if index == -1:
                req = requests.get(url)
                file_name = req.url[url.rfind('/')+1:]
                with open(file_name, 'wb') as f:
                    for content in req.iter_content():
                        if content:
                            f.write(content)
                    return pd.read_csv(file_name)
            else:
                from kaggle.api.kaggle_api_extended import KaggleApi
                api = KaggleApi()
                api.authenticate()
                api.competition_download_file(url, unzip=True)
                return pd.read_csv(file_name)

# name columns of df
def name_columns(df, col_n):
    df.columns = col_n
    return df

# replace missing data value designators with None type
def replace_to(df, column_name, rep_val):
    if rep_val == 'mean':
        df[[column_name]] = df[[column_name]].fillna((df[[column_name]].mean()))
    else:
        df[[column_name]] = df[[column_name]].replace(rep_val, np.nan)
    return df

# plot exploratory data analysis based on type of plot designated
def plot_to_explore(df, file_name, plot_style, hue_col=""):
    if plot_style == 'hist':
        df.hist(figsize = (12,10),color = 'green', bins=30)
        plt.savefig(file_name)
    elif plot_style == 'pairplot':
        sns.pairplot(df, hue=hue_col)
        plt.savefig(file_name)
    elif plot_style == 'heatmap':
        correlation = df.corr()
        plt.figure(figsize = (12,10))
        sns.heatmap(correlation,annot = True)
        plt.savefig(file_name)
