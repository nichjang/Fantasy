import csv
import requests
from bs4 import BeautifulSoup

#dictionary mapping: key = team abbrev uppercase, value = team abbrev
def abbrev(name):
	return {
		'BKN': 'Bkn',
		'ORL': 'Orl',
		'OKC': 'OKC',
		'PHI': 'Phi',
		'NOP': 'NO',
		'CHA': 'Cha',
		'IND': 'Ind',
		'CLE': 'Cle',
		'MIN': 'Min',
		'ATL': 'Atl',
		'DET': 'Det',
		'SAC': 'Sac',
		'PHO': 'Pho',
		'LAC': 'LAC',
		'GSW': 'GS',
		'DEN': 'Den',
		'WAS': 'Wsh',
		'TOR': 'Tor',
		'LAL': 'LAL',
		'CHI': 'Chi',
		'HOU': 'Hou',
		'BOS': 'Bos',
		'MIA': 'Mia',
		'SAS': 'SA',
		'MIL': 'Mil',
		'NYK': 'NY',
		'UTA': 'Uta',
		'MEM': 'Mem',
		'DAL': 'Dal',
		'POR': 'Por'
	}[name]

def get_data(list, baseurl, dateurl, endurl):
	r = requests.get(str(baseurl + dateurl + endurl))
	soup = BeautifulSoup(r.content, 'html.parser')
	table = soup.find('ul', class_='lst lineup')
	for row in table.findAll('div', class_='blk crd lineup'):
		teams = row.find('div', class_='teams')
		teamnames = teams.findAll('span', class_='shrt')
		scores = row.find('div', class_='blk lineup-content drw')
		ou = scores.findAll('a')
		for i in range(2):
			sublist=[]
			sublist.append(abbrev(teamnames[i].get_text()))
			sublist.append(ou[i].get_text())
			list.append(sublist)

	for i in range(len(list)):
		if i%2==0:
			list[i].append(list[i+1][0])
		else:
			list[i].append(list[i-1][0])

def parse(date):
	baseurl = 'https://rotogrinders.com/lineups/nba?date='
	dateurl = '2016-12-' + str(date)
	endurl = '&site=draftkings'
	game = []
	filename = 'gameinfo.csv'

	print(baseurl+dateurl+endurl)
	get_data(game, baseurl, dateurl, endurl)
	with open(filename, 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for row in game:
			csvwriter.writerow(row)