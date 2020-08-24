"""
TITLE: LOOKING FOR BIAS IN SUPREME COURT JUSTICES

READING THE JUSTICE DEMOGRAPHIC:
    name: Last name, First name [Can appear multiple times]
    childst:  Nominee’s Childhood Location—State or Country
    childsur: Childhood env.
    famses: Family Economic Status
    nomrelig: Religion
    race
    gender
    lawschn: Number of Law Schools attended
    militbr: Military Branch Service
    agenom: Age at time of nomination
    ideo: Segal & Cover Score of the Nominee’s Ideology


THE ALGORITHM:
    We will extract a certain number of justices and court cases from the full dataset to get our training dataset.
    For each judge, we compare their demographics to their voting records and find if there is any correlation.
    We will also calculate the agreement rate between any two judges on the same case,
        and look at what demographic factors affect the agreement rate.

ENCOUNTERED PROBLEMS:
    Correlating the demographics with the cases.
"""
import os
import numpy
import pandas
import openpyxl
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

"""Accuracy = accuracy_score(numpy.array([0.1, 0.078, 0.2, 0.0005], dtype=int),
                          numpy.array([0.343, 0.45, 0.2, 0.001], dtype=int))
print(Accuracy)"""
def AccuracyScore(true, predicted):
    return 0

def ConfusionMatrix(true, predicted):
    return []


#  DATA SET
JudgeDemographics_File = ".\\Judge Demographics\\Demographics.csv"

# READ the CSV file: Returns a dictionary # where the keys/columns are the headers of the excel table
JudgeDemographics = pandas.read_csv(JudgeDemographics_File)

# CLEANING the Data
JudgeDemographics = JudgeDemographics.dropna()  # Removes rows will NULL points, if any.
JudgeDemographics.pop('name')

# Classifying categorical features as such
childst_label_encoder = LabelEncoder()
JudgeDemographics['childst'] = childst_label_encoder.fit_transform(JudgeDemographics['childst'])

childsur_label_encoder = LabelEncoder()
JudgeDemographics['childsur'] = childsur_label_encoder.fit_transform(JudgeDemographics['childsur'])

nomrelig_label_encoder = LabelEncoder()
JudgeDemographics['nomrelig'] = nomrelig_label_encoder.fit_transform(JudgeDemographics['nomrelig'])

race_label_encoder = LabelEncoder()
JudgeDemographics['race'] = race_label_encoder.fit_transform(JudgeDemographics['race'])

gender_label_encoder = LabelEncoder()
JudgeDemographics['gender'] = gender_label_encoder.fit_transform(JudgeDemographics['gender'])

militbr_label_encoder = LabelEncoder()
JudgeDemographics['militbr'] = militbr_label_encoder.fit_transform(JudgeDemographics['militbr'])

# PREREQUISITE to Training: Get the Independent & Dependent Features
YFeatures = ['ideo']
YData = JudgeDemographics[YFeatures].copy()  # Dependent Feature
# print(YData)

XFeatures = JudgeDemographics.columns.drop(YFeatures)
XData = JudgeDemographics[XFeatures].copy()  # Independent Features
# print(XData)

# TRAINING the Model: Grow the tree
XTrain, XTest, YTrain, YTest = train_test_split(XData, YData, test_size=0.3)
decisionTreeRegressor = DecisionTreeRegressor(max_depth=3)
decisionTreeRegressor.fit(XTrain, YTrain)

# TESTING the Model
YPredicted = decisionTreeRegressor.predict(XTest)
YPredicted = numpy.array(YPredicted, dtype=float)
print(YPredicted)
YTest = YTest[YFeatures].values
YTestValues = []
for values in YTest:
    YTestValues.append(values[0])
YTestValues = numpy.array(YTestValues, dtype=float)
print(YTestValues)
Accuracy = AccuracyScore(YTestValues, YPredicted)  # Does not support float
ConfusionMatrix = ConfusionMatrix(YTestValues, YPredicted)
