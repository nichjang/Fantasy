import csv

file_name = 'xy.csv'

nba_salary = 50000
beam_size = 32

players = [[] for _ in range(8)]
with open(file_name,'r') as x:
	reader = csv.reader(x, delimiter=',')
	for row in reader:
		stats = []
		stats.append(str(row[0])) #name
		stats.append(float(row[1])) #points
		stats.append(int(row[2])) #salary
		stats.append(str(row[3])) #position
		if stats[3] == 'PG':
			players[0].append(stats)
		elif stats[3] == 'SG':
			players[1].append(stats)
		elif stats[3] == 'SF':
			players[2].append(stats)
		elif stats[3] == 'PF':
			players[3].append(stats)
		elif stats[3] == 'C':
			players[4].append(stats)
		elif stats[3] == 'G':
			players[5].append(stats)
		elif stats[3] == 'F':
			players[6].append(stats)
		elif stats[3] == 'UTIL':
			players[7].append(stats)

#add points/salary ratio
for x in range(len(players)):
	for y in range(len(players[x])):
		players[x][y].append(float(players[x][y][1]/players[x][y][2]))

#sort players by value
for x in players:
	x.sort(key = lambda x: x[4], reverse = True)

"""Use a Constrained Satisfaction Problem to model players.
Beam search OR Best-first search"""
def Consistent(player, chosen_players):
	global salary_max
	if player[2] > salary_max:
		return False
	for x in chosen_players:
		if player[3] == x[3]:
			return False
		if player[0] == x[0]:
			return False
	return True

def BeamSearch(position, level):
	global salary_max
	cur_players = position[level]
	for x in cur_players:
		print("currently looking at....",x,"level = ",level)
		if Consistent(x,chosen_players = best_team):
			best_team.append(x)
			salary_max -= x[2]
			if level == 7:
				return True
			else:
				if BeamSearch(position,level+1):
					return True
	
	print(best_team,"\n\n\n\n\n")
	if len(best_team)>0:
		salary_max += best_team[-1][2]
		del best_team[level-1]
	return False

salary_max = nba_salary
best_team = []

BeamSearch(players, level = 0)

total_sum = 0
total_points = 0
for x in best_team:
	print("position = ",x)
	total_sum += x[2]
	total_points += x[1]

print("total sum = ",total_sum,"\ntotal points = ",total_points)