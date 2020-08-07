"""
We will extract a certain number of justices and court cases from the full dataset to get our training dataset.
For each judge, we compare their demographics to their voting records and find if there is any correlation.
We will also calculate the agreement rate between any two judges on the same case, and look at what demographic factors
    affect the agreement rate.
"""
import os
import json


def openFile(caseDir):
    try:
        file = open(caseDir, 'r', encoding='utf-8')
        transcript = file.readline()
        file.close()
        return json.loads(transcript)
    except OSError:
        pass


def writeFile(caseDir, whatToWrite):
    try:
        file = open(caseDir, 'w', encoding='utf-8')
        file.write(json.dumps(whatToWrite))
        file.close()
    except OSError:
        pass


def createDir(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass


JUSTICES = 'justice.js'

MASTER = os.getcwd()
CASES = MASTER + '\\cases\\'  # Contains YEARLY folders which contain JSON case files.
JUDGESFolder = MASTER + '\\judges\\'
createDir(JUDGESFolder)

# Get the Years in CasesFolder
CasesFoldersYears = os.listdir(CASES)

counter = 1
for Year in CasesFoldersYears:
    try:
        CasesInYear = os.listdir(CASES + '\\' + Year)  # For each Year in CasesFolder, get the actual cases

        for nameOfTheCase in CasesInYear:

            caseDetails = openFile(CASES + '\\' + Year + '\\' + nameOfTheCase)  # Read the contents of the file
            if caseDetails:
                try:
                    wikiData = caseDetails['wikiData']  # WikiData contains the details of the persons involved
                    Majority = wikiData['JoinMajority'].split(',')  # Get the name of the judge
                    ''' 
                    JoinMajority = wikiData['JoinMajority'].split(',')
                    Concurrence = wikiData['Concurrence'].split(',')
                    JoinConcurrence = wikiData['JoinConcurrence'].split(',')
                    Concurrence2 = wikiData['Concurrence2'].split(',')
                    JoinConcurrence2 = wikiData['JoinConcurrence2'].split(',') '''

                    for judges in Majority:
                        if judges:
                            print(counter, Majority)
                            counter += 1
                            createDir(JUDGESFolder + judges)  # Create the directory
                            writeFile(JUDGESFolder + judges + '\\' + nameOfTheCase, caseDetails)  # Copy the file

                except KeyError:
                    pass

    except NotADirectoryError:
        continue

