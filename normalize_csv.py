import csv
import clean_string

list = []
filename = 'salaries11.19.csv'

with open(filename, 'r') as csvf:
	csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
	for row in csvreader:
		cleaned_string = clean_string.cleanstr(str(row[1]))
		row[1] = cleaned_string
		list.append(row)

with open(filename, 'w') as csvf:
	csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
	for row in list:
		csvwriter.writerow(row)