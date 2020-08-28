"""
READING THE JUSTICE DEMOGRAPHIC:
    name: last name, first name
    childst: childhood location — state or country.
    childsur: Childhood environment.
    famses: family economic status. Ranked from 1 (lower class) to 5 (upper class)
    nomrelig: religion.
    race
    gender: 0 for male, 1 for female.
    lawschn: number of law schools attended.
    militbr: military branch the judge served in.
    agenom: age at time of nomination.
    ideo: Segal & Cover Ideology Score for the judge.


THE ALGORITHM:
	We first drop the name column.
	Second, we convert the categorical columns into continuous representations readable by the decision tree using StringIndexer and OneHotEncoder.
	Then, we convert the columns encoded as strings into integer and floating-point columns.
	We then use an assembler to combine the input features into a single vector column readable by the decision tree.
	Next, we split the dataset into a training and test set (70% training, 30% test).
	We construct the model based on the training set and use it to make predictions for the test set.
	The test set predictions are compared with the actual ideology scores using the root mean square error (RMSE).

With code from:
	https://towardsdatascience.com/apache-spark-mllib-tutorial-ec6f1cb336a9
	https://towardsdatascience.com/apache-spark-mllib-tutorial-7aba8a1dce6e
"""

import pyspark
from pyspark.context import SparkContext
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.feature import IndexToString, StringIndexer, OneHotEncoder, VectorAssembler

from pyspark.mllib.linalg import Vector as MLLibVector, Vectors as MLLibVectors
from pyspark.mllib.regression import LabeledPoint
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.sql.session import SparkSession
from pyspark.sql.types import DoubleType, IntegerType

# Credit for creating a context: https://stackoverflow.com/a/43231461
sc = SparkContext('local')
spark = SparkSession(sc)

# Read the CSV file
JudgeDemographics_File = ".\\Judge Demographics\\Demographics.csv"
JudgeDemographics = spark.read.format("csv").options(header='true').load(JudgeDemographics_File)

# CLEAN the Data
JudgeDemographics = JudgeDemographics.drop('name')

# Format the categorical columns to work with the decision tree

# Converts a categorical column of strings into a format in which each string value is replaced with an index
def index_column(JudgeDemographics, column_name):
	indexed_column = column_name + '_index'
	
	indexer = StringIndexer(inputCol=column_name,
		outputCol=indexed_column,
		stringOrderType='alphabetAsc')
	model = indexer.fit(JudgeDemographics)
	
	# Print information about the model
	# Credit: stackoverflow.com/a/43575554
	print('Column name: ' + indexed_column + " Number of entries: " + str(len(model.labels)))
	print(model.labels)
	
	return model.transform(JudgeDemographics).drop(column_name)

JudgeDemographics = index_column(JudgeDemographics, 'childst')
JudgeDemographics = index_column(JudgeDemographics, 'childsur')
JudgeDemographics = index_column(JudgeDemographics, 'nomrelig')
JudgeDemographics = index_column(JudgeDemographics, 'race')
JudgeDemographics = index_column(JudgeDemographics, 'militbr')

# Separate each categorical column into a continuous form
'''
ohe = OneHotEncoder(
	inputCols=['childst_index', 'childsur_index', 'nomrelig_index', 'race_index', 'militbr_index'],
	outputCols=['childst_ohe', 'childsur_ohe', 'nomrelig_ohe', 'race_ohe', 'militbr_ohe'])
ohe_model = ohe.fit(JudgeDemographics)
JudgeDemographics = ohe_model.transform(JudgeDemographics)'''

# Convert string columns into integer and double columns
# Credit: stackoverflow.com/a/32286450
JudgeDemographics = JudgeDemographics \
	.withColumn('famses', JudgeDemographics['famses'].cast(IntegerType())) \
	.withColumn('gender', JudgeDemographics['gender'].cast(IntegerType())) \
	.withColumn('lawschn', JudgeDemographics['lawschn'].cast(IntegerType())) \
	.withColumn('agenom', JudgeDemographics['agenom'].cast(IntegerType())) \
	.withColumn('ideo', JudgeDemographics['ideo'].cast(DoubleType()))

# Create a vector column, in which each cell contains all the features of a row
# https://spark.apache.org/docs/latest/ml-features.html#vectorassembler
assembler = VectorAssembler(
	inputCols=['famses',
		'gender',
		'lawschn',
		'agenom',
		'childst_index',
		'childsur_index',
		'nomrelig_index',
		'race_index',
		'militbr_index'],
	outputCol='features')
JudgeDemographics = assembler.transform(JudgeDemographics)

# Credit for converting dense vector into MLLibVector: stackoverflow.com/a/41076311
JudgeDemographics = JudgeDemographics.rdd.map(lambda row: LabeledPoint(
	row['ideo'],
	MLLibVectors.dense(row['features'].toArray())
))

# Split the data
(trainingData, testData) = JudgeDemographics.randomSplit([0.7, 0.3])

# Create a model from the training data
'''
dt = DecisionTree(featuresCol='features',
	labelCol='ideo',
	categoricalFeaturesInfo={
		4:23,	
		5:3,
		6:9,
		7:3,
		8:6
	})
model = Decision.fit(trainingData)'''
model = DecisionTree.trainRegressor(trainingData,
	categoricalFeaturesInfo={
		4:23,	
		5:3,
		6:9,
		7:3,
		8:6
	})

# Test the Model

#predictions = model.transform(testData)
predictions = model.predict(testData.map(lambda x: x.features))
labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
testMSE = labelsAndPredictions.map(lambda lp: (lp[0] - lp[1]) * (lp[0] - lp[1])).sum() /\
    float(testData.count())
print('Test Mean Squared Error = ' + str(testMSE))
print('Learned regression tree model:')
print(model.toDebugString())
'''
evaluator = RegressionEvaluator(labelCol='ideo', predictionCol='prediction', metricName='rmse')
rmse = evaluator.evaluate(predictions)
print("Root Mean Square Error: %.3f" % rmse)

# Print the model
print(model.toDebugString)'''