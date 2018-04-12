
import re
import os
import csv
import time

inputDirectory = "_1986_2017/"
outputDirectory = "FieldData/"
if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

countSuccess = 0
countFail = 0
fails = []

for filename in os.listdir(inputDirectory):
    if filename.endswith("_1986_2017.txt"):
        print("\n PARSING: " + os.path.join(inputDirectory, filename))

        # retrieve the length of time-series
        fileText = ""
        with open(inputDirectory + filename, "r") as fileHandle:
            fileText = fileHandle.read()
            fieldDataCount = len(re.findall(r"fieldData ", fileText))
            print(str(fieldDataCount) + " date/time points collected.")

        # retrieve the security name
        outputFileName = ""
        with open(inputDirectory + filename, "r") as fileHandle:
            for line in fileHandle:
                if line.strip().startswith("security = "):
                    securityName = line.strip().split("\"")[1]
                    outputFileName = securityName + "FieldData.csv"
                    break
            if outputFileName == "":
                outputFileName = "unresolvedSecurity_" + filename
                countFail += 1.0
                fails.append("unresolvedSecurity: " + filename)

        # retrieve the variable list
        fileText = ""
        with open(inputDirectory + filename, "r") as fileHandle:
            fileText = fileHandle.read()
            try:
                firstRow = re.search('fieldData = {[\s\w=.\-]+}', fileText).group()
            except:
                countFail += 1.0
                fails.append("unparsedValue: " + securityName)
                continue

            variableNames = re.findall("[a-zA-Z_]+", firstRow)
            print(str(len(variableNames)-2) + " attributes/features retrieved.")

            # loop through each variable (date/time as first var.) and parse values
            countSuccess += 1.0
            with open(outputDirectory + outputFileName, "w", newline='') as fw:
                csvWriter = csv.writer(fw)

                for variable in variableNames[1:]:
                    values = re.findall(variable + " = ([0-9.\-]+)", fileText)
                    values.insert(0, variable)
                    csvWriter.writerow(values)

print('\n' + str(len(os.listdir(outputDirectory))) + " files processed to csv file(s).")
print("Success:", int(countSuccess), "; Fail:", int(countFail), ".")
print(str(fails))
