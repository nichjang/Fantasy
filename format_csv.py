import csv

def format_sal(start_date, end_date):
	for i in range(start_date,end_date+1,1):
		if i != 24:
			list = []
			print(i)
			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\11.%s\\salaries11.%s.csv' % (str(i),str(i)), 'r') as csvf:
				csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
				for row in csvreader:
					list.append(row)
			del list[0]
			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries11.%sformat.csv' % str(i), 'w') as csvf:
				csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
				for row in list:
					csvwriter.writerow(row)

def format_results(start_date, end_date):
	for i in range(start_date,end_date+1,1):
		if i != 24:
			list = []
			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\11.%s\\results11.%s.csv' % (str(i),str(i)), 'r', errors="ignore") as csvf:
				csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
				for row in csvreader:
					if row[7]:
						list.append(row)
			
			del list[0]
			for item in list:
				del item[:7]
				del item[1]

			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results11.%sformat.csv' % str(i), 'w') as csvf:
				csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
				for row in list:
					if row:
						csvwriter.writerow(row)

def format_data(start_date, end_date):
	list = []
	for i in range(start_date,end_date+1,1):
		if i != 24:
			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict%s.csv' % str(i), 'r') as csvf:
				csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
				for row in csvreader:
					list.append(row)
			
	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict.csv', 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

format_data(18,29)