from pathlib import Path
import csv
import clean_string

dict = {'Luc Richard Mbah a Moute':'Luc Mbah a Moute',
		'Nene Hilario' : 'Nene'
}

dict_team = {'Was': 'Wsh'}

def format_sal(start_date, end_date):
	for j in range(start_date,end_date+1,1):
		for k in range(1,32,1):
			list = []
			current_path = Path('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\%s.%s\\salaries%s.%s.csv' % (str(j),str(k),str(j),str(k)))
			if current_path.is_file():
				with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data\\%s.%s\\salaries%s.%s.csv' % (str(j),str(k),str(j),str(k)), 'r') as csvf:
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

				with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries\\salaries%s.%s.format.csv' % (str(j),str(k)), 'w') as csvf:
					csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
					for row in copy_list:
						row[1] = clean_string.cleanstr(row[1])
						if row[1] in dict:
							row[1] = dict.get(row[1])
						if row[5] in dict_team:
							row[5] = dict_team.get(row[5])
						csvwriter.writerow(row)
					for row in new_list:
						row[1] = clean_string.cleanstr(row[1])
						if row[1] in dict:
							row[1] = dict.get(row[1])
						if row[5] in dict_team:
							row[5] = dict_team.get(row[5])
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
			if row[5] in dict_team:
				row[5] = dict_team.get(row[5])
			csvwriter.writerow(row)
		for row in new_list:
			row[1] = clean_string.cleanstr(row[1])
			if row[1] in dict:
				row[1] = dict.get(row[1])
			if row[5] in dict_team:
				row[5] = dict_team.get(row[5])
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
		with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict%s.csv' % str(i), 'r') as csvf:
			csvreader = csv.reader(csvf, delimiter=',', lineterminator='\n')
			for row in csvreader:
				if row[7]:
					if float(row[7])>0:
						list.append(row)
	for row in list:
		if not row[7]:
			row[7] = float(0)
	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data.csv', 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

def format_season():
	list = []
	filename = 'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\season.csv'
	with open(filename, 'r') as csvf:
		csvreader = csv.reader(csvf,delimiter=',',lineterminator='\n')
		for row in csvreader:
			temp_list = []
			temp_list.append(row[0])
			unpack = str(row[1])
			unpack = unpack.replace('{','')
			unpack = unpack.replace('}','')
			cnt = 0
			for i in range(unpack.count(',')+1):
				if i != unpack.count(','):
					temp_list.append(unpack[cnt:unpack.find(',',cnt)])
					cnt = unpack.find(',',cnt)+1
				else:
					temp_list.append(unpack[cnt:])
			list.append(temp_list)

	with open(filename,'w') as csvf:
		csvwriter = csv.writer(csvf,delimiter=',',lineterminator='\n')
		for row in list:
			csvwriter.writerow(row)

#format_season()
#format_sal_single(6)
#format_results_single(6)
format_sal(11,12)
#format_data(1,13)
#format_sal_single(3)
#format_results_single(3)