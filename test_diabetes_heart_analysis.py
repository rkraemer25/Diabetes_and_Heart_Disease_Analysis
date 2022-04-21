# Final Project
# Raushan Akayeva & Robert Kraemer

# # # # # # # # # # # # # # # # # #
# test_diabetes_heart_analysis.py #
# # # # # # # # # # # # # # # # # #

"""Test modules for diabetes_heart_analysis.py"""

import os
import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from diabetes_heart_analysis import *
from load_and_eda import *
from analysis_for_decision import *

class test_load_and_eda(unittest.TestCase):
    def test_load_data(self):
        df = pd.read_csv('diabetes.csv')
        df1 = load_data('diabetes.csv')
        assert_frame_equal(df, df1)

        #before this test please rename cvs file as following and place zip file to directory
        df3 = pd.read_csv('heart_failure_clinical_records_dataset1.csv')
        df4 = load_data('heart_failure_clinical_records_dataset.csv')
        assert_frame_equal(df, df1)

    def test_name_columns(self):
        df = pd.read_csv('diabetes.csv')
        l = [1,2,3,4,5,6,7,8,9]
        self.assertEqual(name_columns(df, l).columns[0], 1)
        self.assertNotEqual(name_columns(df, l).columns[0], 2)

    def test_replace_to(self):
        df = pd.read_csv('diabetes.csv')
        self.assertFalse(0 in replace_to(df, "Glucose", 0)[["Glucose"]])

    def test_plot_to_explore(self):
        df = pd.read_csv('diabetes.csv')

        plot_to_explore(df, "unit_test_plot.png", "hist")
        self.assertTrue(os.path.exists("unit_test_plot.png"))

        plot_to_explore(df, "unit_test_plot1.png", "pairplot", "Outcome")
        self.assertTrue(os.path.exists("unit_test_plot1.png"))

        plot_to_explore(df, "unit_test_plot2.png", "heatmap")
        self.assertTrue(os.path.exists("unit_test_plot2.png"))

class test_analysis_for_decision(unittest.TestCase):
    def test_change_diagnosis_to_bool(self):
        file_heart2 = 'processed.cleveland.data'
        url_heart2 = 'http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data'
        df = load_data(file_heart2, url_heart2)
        l_columns = ['age', 'gender', 'chest_pain_type', 'BloodPressure',
                     'SerumCholestoral', 'blood_sugar', 'electrocardiog_results',
                     'maximum_heart_rate',
                     'exercise_induced_angina',  'oldpeak', 'slope',
                     'major_vessels', 'defect', 'diagnosis']
        name_columns(df, l_columns)
        for i in l_columns:
            replace_to(df, i, '?')
        df=df.drop(['age', 'gender', 'chest_pain_type', 'exercise_induced_angina', 'oldpeak', 'slope', 'major_vessels', 'SerumCholestoral'], axis=1)
        df = change_diagnosis_to_bool(df)
        self.assertFalse(2 in df[['diagnosis']])

    def test_scatterplot_analysis(self):
        df = pd.read_csv('diabetes.csv')
        scatterplot_analysis('Glucose', 'Insulin', 'Outcome', df, "unit_test_plot3.png")
        self.assertTrue(os.path.exists("unit_test_plot3.png"))

    def test_barplot_analysis(self):
        df = pd.read_csv('diabetes.csv')
        barplot_analysis('Glucose', 'Insulin', 'Outcome', df, "unit_test_plot4.png")
        self.assertTrue(os.path.exists("unit_test_plot4.png"))

if __name__ == '__main__':
    unittest.main()
