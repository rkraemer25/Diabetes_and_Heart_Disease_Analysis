# Final Project Proposal

## Group Members

- Raushan Akayeva
- Robert Kraemer

## Analysis Objective

To perform data analysis to discover the relationship between
diabetes and heart failure/disease.

## Datasets that will be utilized
Please download zip archives to same directory from following sources

* Dataset 1 ->  https://www.kaggle.com/uciml/pima-indians-diabetes-database  
  - rename it as diabetes.zip
* Dataset 2 -> https://www.kaggle.com/andrewmvd/heart-failure-clinical-data  
  - rename it as heart_failure_clinical_records_dataset.zip
* Dataset 3 -> http://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data
   - will be downloaded automatically

If these zip archives didn't dowloaded, kaggle module needed to be installed and kaggle.json token must be refreshed at root/Users/username/.kaggle directory.

## Python functionality group will be exploring with analysis

We are using three different datasets coming from kaggle and one from uci archive.
The first dataset contains data on levels of diabetes within the Pima Indian
community. The second and third datasets contain data on heart failure and
heart disease. We seek to perform an exploratory analysis on each of these
datasets independently, to then bring them together to determine the likelihood
of heart failure within the Pima community given whether or not the subjects
are diabetic. For functionality, we plan to use command-line parsing using
argparse, logging using the logging module, unit testing of functions using the
unittest module, graphical output with matplotlib, and data output using csv
module. We plan to explore the NumPy and Pandas modules for numerical data
processing. We also seek to explore and learn more about new module seaborn to
aid in the data visualization of our analysis.

## Analysis Conclusion

When analyzing the datasets we found a correlation between blood sugar, insulin,
and glucose levels, with blood pressure using heat maps. Looking at our final
plots, we are able to see that the influence of blood sugar on blood pressure
was not significant designator for diagnosis of heart disease/failure in the
pima community. 

## Usage

python3 diabetes_heart_analysis.py \<command\> [-h] [-s {diabetes,heart2}] [-c <csvfile>] [-d {diabetes,heart1,heart2}]

### Dependencies
Package dependencies listed in requirements.txt

### [command]
- **explore**: run exploratory data analysis on datasets
- **analysis**: run combined analysis for datasets

### [optional arguments]
- **-s**: sort the datasets by column
- **-c**: output to csv file
- **-d**: print description on dataset
