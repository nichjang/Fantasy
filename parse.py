import sys
import requests
import csv
from urllib.parse import urljoin
from bs4 import BeautifulSoup

#uprint is for debugging only (in case of printing encoding error)
"""def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)"""

baseurl = 'http://games.espn.com/fba/leaders?&slotCategoryId='
indexurl = '&seasonTotals=true&seasonId=2017&startIndex='
next_page = 'http://games.espn.com/fba/leaders?&slotCategoryId=0&seasonTotals=true&seasonId=2017&startIndex=0'

list = []
positions = ['PG','SG','SF','PF','C','G','F']
j = 0
nextindex = 0


while True:
	r = requests.get(next_page)
	soup = BeautifulSoup(r.content,'html.parser')
	button = soup.find('div',class_='paginationNav')
	table = soup.find('table',class_='playerTableTable tableBody')

	for row in table.findAll('tr'):
		cells = [c.get_text() for c in row.findAll('td')]
		if 'PLAYER' not in str(cells) and '--' not in str(cells) and len(str(cells)) != 4:
			cells.append(positions[j])
			if 'DTD' in str(cells):
				cells.append('DTD')
			if '*' in str(cells):
				cells.append('Out')
			list.append(cells)
		elif 'PLAYER' in str(cells) and j == 0 and nextindex == 0:
			list.append(cells)

	print(button.get_text())
	if 'NEXT' in button.get_text():
		nextindex += 50
		ending = indexurl + str(nextindex)
		next_page = str(baseurl) +str(j) + str(ending)
		print(next_page)
	else:
		if j+1 == len(positions):
			break #exit loop
		else:
			j += 1
			nextindex = 0
			ending = indexurl + str(0)
			next_page = str(baseurl) +str(j) + str(ending)


with open('test1.csv', 'w') as csvf:
	csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
	for i in range(len(list)):
		csvwriter.writerow(list[i])




