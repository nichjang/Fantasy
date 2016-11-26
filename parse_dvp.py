import requests
import csv
from bs4 import BeautifulSoup

#uprint is for debugging only (in case of printing encoding error)
"""def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
	enc = file.encoding
	if enc == 'UTF-8':
		print(*objects, sep=sep, end=end, file=file)
	else:
		f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
		print(*map(f, objects), sep=sep, end=end, file=file)"""

baseurl = 'http://www.rotowire.com/daily/nba/defense-vspos.htm?site=DraftKings&statview=last5'
endurl = ['&pos=SG','&pos=G','&pos=SF','&pos=PF','&pos=F','&pos=C','na']
next_page = str(baseurl)
list = []

#dictionary mapping: key = team, value = team abbrev
def abbrev(name):
	return {
		'Brooklyn Nets': 'Bkn',
		'Orlando Magic': 'Orl',
		'Oklahoma City Thunder': 'OKC',
		'Philadelphia 76ers': 'Phi',
		'New Orleans Pelicans': 'NO',
		'Charlotte Hornets': 'Cha',
		'Indiana Pacers': 'Ind',
		'Cleveland Cavaliers': 'Cle',
		'Minnesota Timberwolves': 'Min',
		'Atlanta Hawks': 'Atl',
		'Detroit Pistons': 'Det',
		'Sacramento Kings': 'Sac',
		'Phoenix Suns': 'Pho',
		'Los Angeles Clippers': 'LAC',
		'Golden State Warriors': 'GS',
		'Denver Nuggets': 'Den',
		'Washington Wizards': 'Wsh',
		'Toronto Raptors': 'Tor',
		'Los Angeles Lakers': 'LAL',
		'Chicago Bulls': 'Chi',
		'Houston Rockets': 'Hou',
		'Boston Celtics': 'Bos',
		'Miami Heat': 'Mia',
		'San Antonio Spurs': 'SA',
		'Milwaukee Bucks': 'Mil',
		'New York Knicks': 'NY',
		'Utah Jazz': 'Uta',
		'Memphis Grizzlies': 'Mem',
		'Dallas Mavericks': 'Dal',
		'Portland Trail Blazers': 'Por'
	}[name]

for i in range(7):
	while True:
		r = requests.get(next_page)
		soup = BeautifulSoup(r.content,'html.parser')
		table = soup.find('tbody')

		for row in table.findAll('tr'):
			cells = [c.get_text() for c in row.findAll('td')]
			stringcells = str(cells[0])
			cells[0] = abbrev(stringcells)
			del cells[4:]
			del cells[2]
			cells.append(opponent(stringcells))
			list.append(cells)
		break;
	next_page = str(baseurl) + str(endurl[i])

for i in range(7):
	dvp_percents = []
	sum = 0.0
	for j in range(1,31):
		dvp_percents.append(list[(i*30)+j-1][2])
		sum += float(list[(i*30)+j-1][2])
	sum /= 30
	print(sum)
	for j in range(1,31):
		list[(i*30)+j-1][2] = (float(dvp_percents[j-1])-sum)/sum


with open('dvp.csv', 'w') as csvf:
	csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
	for i in range(len(list)):
		csvwriter.writerow(list[i])