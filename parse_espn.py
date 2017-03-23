#import sys
import requests
import csv
import clean_string
from bs4 import BeautifulSoup

#uprint is for debugging only (in case of printing encoding error)
"""def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)"""

positions = ['PG','SG','SF','PF','C', 'G','F','UTIL']
pagenums = [0,1,2,3,4,5,6,11]

baseurl = 'http://games.espn.com/fba/leaders?&slotCategoryId='
dateurl = '&scoringPeriodId='
endurl = '&seasonId=2017&startIndex='

"""
Input: Date to parse (in ESPN's date format,unsigned int)
Output: CSV file which details players that played on specified date,
along with relevant stats
"""
def parse_single(current_date):
	next_page = str(baseurl) + str(0) + str(dateurl) + str(current_date) + str(endurl) + str(0)
	list = []
	j = 0
	nextindex = 0
	while True:
		r = requests.get(next_page)
		soup = BeautifulSoup(r.content, 'html.parser')
		button = soup.find('div',class_='paginationNav')
		table = soup.find('table',class_='playerTableTable tableBody')
		tr_count = 0
		semaphore = 0
		for row in table.findAll('tr'):
			#discard first two tr
			tr_count += 1
			cells = [c.get_text() for c in row.findAll('td')]
			del cells[1:4]
			playername = clean_string.cleanstr(str(cells[0]))
			cells[0] = playername
			stringcells = clean_string.cleanstr(str(cells))
			if '--' in stringcells:
				semaphore = 1
				break

			if  tr_count > 2:
				if 'PLAYER' not in stringcells and '--' not in stringcells and len(stringcells) != 4:
					cells.append(positions[j])
					loc = stringcells.find(', ') + 2
					teamname = stringcells[ loc : stringcells.find(' ',loc+2)]
					if teamname == 'Nor':
						teamname = 'NO'
					cells.append(teamname)
					if 'DTD' in stringcells:
						stringcells = stringcells.replace('  DTD','')
						cells.append('DTD')
					elif '*' in stringcells:
						stringcells = stringcells.replace('*','')
						stringcells = stringcells.replace('  O','')
						cells.append('Out')
					else:
						cells.append('G')
					del(cells[1])
					list.append(cells)
				#elif 'PLAYER' in stringcells and j == 0 and nextindex == 0:
					#list.append(cells)

		if 'NEXT' in button.get_text() and semaphore == 0:
			nextindex += 50
			ending = endurl + str(nextindex)
			next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(current_date) + str(ending)
			print(next_page)
		else:
			if j+1 >= len(positions):
				print(next_page)
				break #exit loop
			else:
				j += 1
				nextindex = 0
				ending = endurl + str(0)
				next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(current_date) + str(ending)
				print(next_page)
	with open(r'C:\Users\Nicholas\Documents\GitHub\Fantasy\espn\data%s.csv'  % str(current_date), 'w') as csvf:
			csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
			for i in range(len(list)):
				list[i][0] = clean_string.cleanstr(list[i][0][:list[i][0].find(',')])
				csvwriter.writerow(list[i])

"""
Input: Date to parse (in ESPN's date format,unsigned int)
Output: CSV files which details players that played on specified date,
along with relevant stats
*Note this function parses all dates from beginning to input date*
"""
def parse_beginning(current_date):
	next_page = str(baseurl) + str(0) + str(dateurl) + str(1) + str(endurl) + str(0)
	for i in range(1,current_date+1,1):
		list = []
		j = 0
		nextindex = 0
		while True:
			r = requests.get(next_page)
			soup = BeautifulSoup(r.content, 'html.parser')
			button = soup.find('div',class_='paginationNav')
			table = soup.find('table',class_='playerTableTable tableBody')
			tr_count = 0
			semaphore = 0

			for row in table.findAll('tr'):
				#discard first two tr
				tr_count += 1
				cells = [c.get_text() for c in row.findAll('td')]
				del cells[1:4]
				playername = clean_string.cleanstr(str(cells[0]))
				cells[0] = playername
				stringcells = clean_string.cleanstr(str(cells))
				if '--' in stringcells:
					semaphore = 1
					break

				if  tr_count > 2:
					if 'PLAYER' not in stringcells and '--' not in stringcells and len(stringcells) != 4:
						cells.append(positions[j])
						loc = stringcells.find(', ') + 2
						teamname = stringcells[ loc : stringcells.find(' ',loc+2)]
						if teamname == 'Nor':
							teamname = 'NO'
						cells.append(teamname)
						if 'DTD' in stringcells:
							stringcells = stringcells.replace('  DTD','')
							cells.append('DTD')
						elif '*' in stringcells:
							stringcells = stringcells.replace('*','')
							stringcells = stringcells.replace('  O','')
							cells.append('Out')
						else:
							cells.append('G')
						del(cells[1])
						list.append(cells)
					#elif 'PLAYER' in stringcells and j == 0 and nextindex == 0:
						#list.append(cells)

			if 'NEXT' in button.get_text() and semaphore == 0:
				nextindex += 50
				ending = endurl + str(nextindex)
				next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(i) + str(ending)
				print(next_page)
			else:
				if j+1 >= len(positions):
					next_page = str(baseurl) + str(0) + str(dateurl) + str(i+1) + str(endurl) + str(0)
					print(next_page)
					break #exit loop
				else:
					j += 1
					nextindex = 0
					ending = endurl + str(0)
					next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(i) + str(ending)
					print(next_page)

		with open(r'C:\Users\Nicholas\Documents\GitHub\Fantasy\espn\data%s.csv'  % str(i), 'w') as csvf:
			csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
			for i in range(len(list)):
				list[i][0] = clean_string.cleanstr(list[i][0][:list[i][0].find(',')])
				csvwriter.writerow(list[i])

"""
Input: Dates to parse (in ESPN's date format,unsigned int)
Output: CSV files which details players that played on specified date,
along with relevant stats
*Note this function parses all dates from first input date to second input date*
"""
def parse_between(first_date,current_date):
	next_page = str(baseurl) + str(0) + str(dateurl) + str(1) + str(endurl) + str(0)
	for i in range(first_date,current_date+1,1):
		list = []
		j = 0
		nextindex = 0
		while True:
			r = requests.get(next_page)
			soup = BeautifulSoup(r.content, 'html.parser')
			button = soup.find('div',class_='paginationNav')
			table = soup.find('table',class_='playerTableTable tableBody')
			tr_count = 0
			semaphore = 0

			for row in table.findAll('tr'):
				#discard first two tr
				tr_count += 1
				cells = [c.get_text() for c in row.findAll('td')]
				del cells[1:4]
				playername = clean_string.cleanstr(str(cells[0]))
				cells[0] = playername
				stringcells = clean_string.cleanstr(str(cells))
				if '--' in stringcells:
					semaphore = 1
					break

				if  tr_count > 2:
					if 'PLAYER' not in stringcells and '--' not in stringcells and len(stringcells) != 4:
						cells.append(positions[j])
						loc = stringcells.find(', ') + 2
						teamname = stringcells[ loc : stringcells.find(' ',loc+2)]
						if teamname == 'Nor':
							teamname = 'NO'
						cells.append(teamname)
						if 'DTD' in stringcells:
							stringcells = stringcells.replace('  DTD','')
							cells.append('DTD')
						elif '*' in stringcells:
							stringcells = stringcells.replace('*','')
							stringcells = stringcells.replace('  O','')
							cells.append('Out')
						else:
							cells.append('G')
						del(cells[1])
						list.append(cells)
					#elif 'PLAYER' in stringcells and j == 0 and nextindex == 0:
						#list.append(cells)

			if 'NEXT' in button.get_text() and semaphore == 0:
				nextindex += 50
				ending = endurl + str(nextindex)
				next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(i) + str(ending)
				print(next_page)
			else:
				if j+1 >= len(positions):
					next_page = str(baseurl) + str(0) + str(dateurl) + str(i+1) + str(endurl) + str(0)
					print(next_page)
					break #exit loop
				else:
					j += 1
					nextindex = 0
					ending = endurl + str(0)
					next_page = str(baseurl) + str(pagenums[j]) + str(dateurl) + str(i) + str(ending)
					print(next_page)

		with open(r'C:\Users\Nicholas\Documents\GitHub\Fantasy\espn\data%s.csv'  % str(i), 'w') as csvf:
			csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
			for i in range(len(list)):
				list[i][0] = clean_string.cleanstr(list[i][0][:list[i][0].find(',')])
				csvwriter.writerow(list[i])

if __name__ == "__main__":
	parse_between(123,148)