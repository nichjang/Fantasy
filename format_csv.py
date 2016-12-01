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

			for row in list:
				if row[0].find('/',start_index, len(row[0])) > 0:
					copyrow = row
					del copyrow[0]
					copyrow.insert(0,row[0][row[0].find('/')+1:])
					row[0] = row[0][:row[0].find('/')]
					list.append(copyrow)
					if copyrow[0] == 'PG' or copyrow[0] == 'SG':
						g_copy = copyrow
						g_copy[0] = 'G'
						list.append(g_copy)
					if copyrow[0] == 'SF' or copyrow[0] == 'PF':
						f_copy = copyrow
						f_copy[0] = 'F'
						list.append(f_copy)
				if row[0] == 'PG' or row[0] == 'SG':
					g_copy = row
					g_copy[0] = 'G'
					list.append(g_copy)
				if row[0] == 'SF' or row[0] == 'PF':
					f_copy = row
					f_copy[0] = 'F'
					list.append(f_copy)
				util_copy = row
				util_copy[0] = 'UTIL'
				list.append(util_copy)

			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries11.%sformat.csv' % str(i), 'w') as csvf:
				csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
				for row in list:
					csvwriter.writerow(row)

def format_sal_single(date):
	list = []
	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\12.%s\\salaries12.%s.csv' % (str(date),str(date)), 'r') as csvf:
		csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
		for row in csvreader:
			list.append(row)
	del list[0]
	copy_list = [_ for _ in list]
	new_list = []

	for i in range(len(copy_list)):
		semaphore = 0
		if copy_list[i][0].find('/') > 0:
			temp_list = []
			copyrow = copy_list[i]
			temp_list.append(copyrow[0][copyrow[0].find('/')+1:])
			for row in copyrow[1:]:
				temp_list.append(row)
			new_list.append(temp_list)
			copyrow.insert(0,copyrow[0][:copyrow[0].find('/')])
			del copyrow[1]
			if temp_list[0] == 'PG' or temp_list[0] == 'SG':
				semaphore = 1
				temp_list_2 = []
				temp_list_2.append('G')
				for row in temp_list[1:]:
					temp_list_2.append(row)
				new_list.append(temp_list_2)
			if temp_list[0] == 'SF' or temp_list[0] == 'PF':
				semaphore = 1
				temp_list_2 = []
				temp_list_2.append('F')
				for row in temp_list[1:]:
					temp_list_2.append(row)
				new_list.append(temp_list_2)
		if (copy_list[i][0] == 'PG' or copy_list[i][0] == 'SG') and semaphore == 0:
			temp_list = []
			temp_list.append('G')
			for row in copy_list[i][1:]:
				temp_list.append(row)
			new_list.append(temp_list)
		if (copy_list[i][0] == 'SF' or copy_list[i][0] == 'PF') and semaphore == 0:
			temp_list = []
			temp_list.append('F')
			for row in copy_list[i][1:]:
				temp_list.append(row)
			new_list.append(temp_list)
		temp_list = []
		temp_list.append('UTIL')
		for row in copy_list[i][1:]:
			temp_list.append(row)
		new_list.append(temp_list)

	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries12.%sformat.csv' % str(date), 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in copy_list:
			csvwriter.writerow(row)
		for row in new_list:
			csvwriter.writerow(row)

format_sal_single(1)
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

	for row in list:
		if not row[2]:
			row[2] = float(0)
	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data.csv', 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

#format_data(18,29)