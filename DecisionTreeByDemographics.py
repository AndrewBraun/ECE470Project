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

# https://stackoverflow.com/a/43231461
import pyspark
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
from pyspark.ml import Pipeline
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.feature import StringIndexer
from pyspark.ml.feature import OneHotEncoder
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

sc = SparkContext('local')
spark = SparkSession(sc)

#  DATA SET
JudgeDemographics_File = ".\\Judge Demographics\\Demographics.csv"

# READ the CSV file
JudgeDemographics = spark.read.format("csv").options(header='true').load(JudgeDemographics_File)

# CLEANING the Data
JudgeDemographics = JudgeDemographics.drop('name')

# Classifying categorical features as such
#childst
#childsur
#nomrelig
#race
#militbr

childst_indexer = StringIndexer(inputCol='childst', outputCol='childst_index')
childst_indexer_model = childst_indexer.fit(JudgeDemographics)
JudgeDemographics = childst_indexer_model.transform(JudgeDemographics)

childsur_indexer = StringIndexer(inputCol='childsur', outputCol='childsur_index')
childsur_indexer_model = childsur_indexer.fit(JudgeDemographics)
JudgeDemographics = childsur_indexer_model.transform(JudgeDemographics)

nomrelig_indexer = StringIndexer(inputCol='nomrelig', outputCol='nomrelig_index')
nomrelig_indexer_model = nomrelig_indexer.fit(JudgeDemographics)
JudgeDemographics = nomrelig_indexer_model.transform(JudgeDemographics)

race_indexer = StringIndexer(inputCol='race', outputCol='race_index')
race_indexer_model = race_indexer.fit(JudgeDemographics)
JudgeDemographics = race_indexer_model.transform(JudgeDemographics)

militbr_indexer = StringIndexer(inputCol='militbr', outputCol='militbr_index')
militbr_indexer_model = militbr_indexer.fit(JudgeDemographics)
JudgeDemographics = militbr_indexer_model.transform(JudgeDemographics)

ohe = OneHotEncoder(inputCols=['childst_index', 'childsur_index', 'nomrelig_index', 'race_index', 'militbr_index'], outputCols=['childst_ohe', 'childsur_ohe', 'nomrelig_ohe', 'race_ohe', 'militbr_ohe'])
ohe_model = ohe.fit(JudgeDemographics)
JudgeDemographics = ohe_model.transform(JudgeDemographics)

JudgeDemographics.show()
exit()

feature_columns = JudgeDemographics.columns[:-1]
assembler = VectorAssembler(inputCols=feature_columns, outputCol='features')

# TRAINING the Model: Grow the tree
(trainingData, testData) = JudgeDemographics.randomSplit([0.7, 0.3])

dtr = DecisionTreeRegressor(featuresCol='features', labelCol='ideo')

pipeline = Pipeline(stages=[assembler, dtr])

model = pipeline.fit(trainingData)

# TESTING the Model
predictions = model.transform(testData)

evaluator = RegressionEvaluator(labelCol='ideo', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(predictions)
print("Root Mean Square Error: " + str(rmse))

# Print the model
print(model.stages[1])
