import csv
import json

csvFilePath = 'FNGU.csv'
jsonFilePath = 'FNGU.json'

# Read the CSV and add the data to a dictionary
data = {}
with open(csvFilePath) as csvFile:
    csvReader = csv.DictReader(csvFile)
    for rows in csvReader:
        date = rows['Date']
        data[date] = rows

# Create a new JSON file and write the data to it
with open(jsonFilePath, 'w') as jsonFile:
    jsonFile.write(json.dumps(data, indent=4))

