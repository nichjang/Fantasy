import csv
import clean_string

dict = {'Luc Richard Mbah a Moute':'Luc Mbah a Moute',
		'Nene Hilario' : 'Nene'
}

def format_sal(start_date, end_date):
	for j in range(start_date,end_date+1,1):
		if j != 24:
			list = []
			print(j)
			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\11.%s\\salaries11.%s.csv' % (str(j),str(j)), 'r') as csvf:
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

			with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries11.%sformat.csv' % str(j), 'w') as csvf:
				csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
				for row in list:
					row[1] = clean_string.cleanstr(row[1])
					if row[1] == 'Luc Richard Mbah a Moute':
						row[1] = 'Luc Mbah a Moute'
					csvwriter.writerow(row)
				for row in new_list:
					row[1] = clean_string.cleanstr(row[1])
					row[1] = abbrev(row[1])
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
			row[1] = clean_string.cleanstr(row[1])
			if row[1] in dict:
				row[1] = dict.get(row[1])
			csvwriter.writerow(row)
		for row in new_list:
			row[1] = clean_string.cleanstr(row[1])
			if row[1] in dict:
				row[1] = dict.get(row[1])
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
						row[0] = clean_string.cleanstr(row[0])
						if row[0] == 'Luc Richard Mbah a Moute':
							row[0] = 'Luc Mbah a Moute'
						csvwriter.writerow(row)

def format_results_single(start_date):
	list = []
	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\12.%s\\results12.%s.csv' % (str(start_date),str(start_date)), 'r', encoding='utf-8', errors="ignore") as csvf:
		csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
		for row in csvreader:
			if row[7]:
				list.append(row)

	del list[0]
	for item in list:
		del item[:7]
		del item[1]

	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results12.%sformat.csv' % str(start_date), 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			if row:
				row[0] = clean_string.cleanstr(row[0])
				if row[0] == 'Luc Richard Mbah a Moute':
					row[0] = 'Luc Mbah a Moute'
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

#format_sal_single(1)
#format_sal(18,29)
#format_data(18,29)