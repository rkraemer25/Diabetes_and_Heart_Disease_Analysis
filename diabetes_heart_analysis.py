# Final Project
# Raushan Akayeva & Robert Kraemer
# diabetes_heart_analysis.py

# import packages
from os.path import exists
import os
import logging
import argparse
import requests
import zipfile
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# import modules
import load_and_eda
import analysis_for_decision

file_diabetes = 'diabetes.csv'
file_heart = 'heart_failure_clinical_records_dataset.csv'
file_heart2 = 'processed.cleveland.data'
url_heart2 = 'http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'

def main():
    # create logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler('diabetes_heart_analysis.log', 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

    logging.debug('DEBUG LEVEL LOG')

    #implement parser
    parser = argparse.ArgumentParser(description='Exploratory analysis for each dataset and combined.')
    parser.add_argument('command', type=str, metavar="<command>",
                            help="choose step of analysis to run",
                            choices=["explore", "analysis"])
    parser.add_argument('-s', '--sort', dest='sort_column', choices=['diabetes', 'heart2'],#action='store_true',
                            help='sort the datasets by column')
    parser.add_argument('-c', '--csv',
                        dest='csv_file', metavar="<csvfile>", action='store',
                        help='output to csv file')
    parser.add_argument('-d', '--description', dest='description', choices=['diabetes', 'heart1', 'heart2'], help='print description on datasets')
    args = parser.parse_args()

    # run arguments
    run(args)

# runs program based on args
def run(args):
    # log args
    logging.debug(f"DEBUG: parsing arguments {args}")

    df1 = load_and_eda.load_data(file_diabetes)
    df2 = load_and_eda.load_data(file_heart)
    df3 = load_and_eda.load_data(file_heart2, url_heart2)

    l_columns = ['age', 'gender', 'chest_pain_type', 'BloodPressure',
                     'SerumCholestoral', 'blood_sugar', 'electrocardiog_results',
                     'maximum_heart_rate',
                     'exercise_induced_angina',  'oldpeak', 'slope',
                     'major_vessels', 'defect', 'diagnosis']

    ##third dataset
    #hasn't got column names so put column names to table
    load_and_eda.name_columns(df3, l_columns)

    ##first dataset
    #there are zeroes instead values
    #replace zeroes to null
    load_and_eda.replace_to(df1, "Glucose", 0)
    load_and_eda.replace_to(df1, "BloodPressure", 0)
    load_and_eda.replace_to(df1, "SkinThickness", 0)
    load_and_eda.replace_to(df1, "Insulin", 0)
    load_and_eda.replace_to(df1, "BMI", 0)


    #replace '?' signs in data to null
    for i in l_columns:
        load_and_eda.replace_to(df3, i, '?')

    # nulls can be replaced to mean value of that column
    load_and_eda.replace_to(df1, "BloodPressure", 'mean')

    if args.command == 'explore':
        logging.info("Running explore command...")
        # generate plots for exploring initial datasets
        ##first dataset
        load_and_eda.plot_to_explore(df1, "diabetes_hist.png", "hist")
        load_and_eda.plot_to_explore(df1, "diabetes_pairplot.png", "pairplot", "Outcome")
        load_and_eda.plot_to_explore(df1, "diabetes_heatmap.png", "heatmap")

        ##second dataset
        load_and_eda.plot_to_explore(df2, "heart1_hist.png", "hist")
        load_and_eda.plot_to_explore(df2, "heart1_pairplot.png", "pairplot", "DEATH_EVENT")
        load_and_eda.plot_to_explore(df2, "heart1_heatmap.png", "heatmap")

        ###third dataset
        load_and_eda.plot_to_explore(df3, "heart2_hist.png", "hist")
        load_and_eda.plot_to_explore(df3, "heart2_pairplot.png", "pairplot", "diagnosis")
        load_and_eda.plot_to_explore(df3, "heart2_heatmap.png", "heatmap")

    elif args.command == 'analysis':
        logging.info("Running analysis command...")
        # we need to find correlation between diabetes and heart diseases
        # first, drop unnesesary columns
        df1=df1.drop(['Pregnancies', 'SkinThickness', 'BMI', 'DiabetesPedigreeFunction', 'Age'], axis=1)
        df2=df2.drop(['age', 'anaemia', 'creatinine_phosphokinase',
                       'ejection_fraction',  'platelets',
                       'serum_creatinine', 'serum_sodium', 'sex', 'smoking', 'time'], axis=1)
        df3=df3.drop(['age', 'gender', 'chest_pain_type', 'exercise_induced_angina', 'oldpeak', 'slope', 'major_vessels', 'SerumCholestoral'], axis=1)
        #there are 3 kinds of heart diagnosis, change them to bool value so 1-has disease, 0-hasn't disease
        analysis_for_decision.change_diagnosis_to_bool(df3)

        #in this scatterplot we can observe that there is correlation between Insulin and Glucose and whether person has diabetes
        analysis_for_decision.scatterplot_analysis('Glucose', 'Insulin', 'Outcome', df1, "Glucose_Insulin_scatter.png")
        # here we see that a correlation between high Blood pressure and Glucose level exists
        analysis_for_decision.scatterplot_analysis('Glucose', 'BloodPressure', 'Outcome', df1, "Glucose_BloodPressure_scatter.png")
        # at this scatterplot we can see implicit correlation between insulin and blood pressure
        analysis_for_decision.scatterplot_analysis('Insulin', 'BloodPressure', 'Outcome', df1, "Insulin_BloodPressure_scatter.png")

        #at barplot the correlation between BloodPressure, blood_sugar and heart diseases is not explicit
        analysis_for_decision.barplot_analysis("blood_sugar", "BloodPressure", "diagnosis", df3, "blood_sugar_BloodPressure_diagnosis.png")
        analysis_for_decision.barplot_analysis("blood_sugar", "BloodPressure", "defect", df3, "blood_sugar_BloodPressure_defect.png")

    # print the output in CSV
    # append two datasets to one csv file
    if args.csv_file is not None:
        df1.describe().to_csv(args.csv_file)

    # print description on dataset
    if args.description == 'diabetes':
        print('DESCRIPTION ', 'diabetes')
        print(df1.head())
        print(df1.tail())
        print(df1.info())
        print(df1.isna().sum() / df1.shape[0])
    elif args.description == 'heart1':
        print('DESCRIPTION ', 'heart1')
        print(df2.head())
        print(df2.tail())
        print(df2.info())
        print(df2.isna().sum() / df2.shape[0])
    elif args.description == 'heart2':
        print('DESCRIPTION ', 'heart1')
        print(df3.head())
        print(df3.tail())
        print(df3.info())
        print(df3.isna().sum() / df3.shape[0])

    # sort dataset by columns
    if args.sort_column == 'diabetes':
        sorted_d = df1.sort_values(['BloodPressure'], ascending=True)
        print(sorted_d)
    elif args.sort_column == 'heart2':
        sorted_h = df3.sort_values(['BloodPressure'], ascending=True)
        print(sorted_h)

if __name__=="__main__":
    main()
