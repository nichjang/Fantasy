import csv
import clean_string

filename1 = 'salaries11.19.csv'
filename2 = 'results11.19.csv'

def clean_salaries():
	list = []
	with open(filename1, 'r') as csvf:
		csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
		for row in csvreader:
			cleaned_string = clean_string.cleanstr(str(row[1]))
			row[1] = cleaned_string
			list.append(row)

	with open(filename1, 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

def clean_results():
	list = []
	with open(filename2, 'r') as csvf:
		csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
		for row in csvreader:
			cleaned_string = clean_string.cleanstr(str(row[0]))
			row[0] = cleaned_string
			list.append(row)

	with open(filename2, 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

clean_results()