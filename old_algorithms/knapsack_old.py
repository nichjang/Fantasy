import csv

file_name = 'xy.csv'

nba_salary = 500
players = []
fantasy_points = []
salary = []
top_picks = []
top_picks_salaries = []

with open(file_name,'r') as x:
    reader = csv.reader(x, delimiter=',')
    for row in reader:
    	players.append(str(row[0]))
    	fantasy_points.append(float(row[1]))
    	salary.append(int(row[2]))

Matrix = [[0 for x in range(nba_salary)] for y in range(len(salary))]

for i in range(1,len(salary)):
	for j in range(nba_salary):
		if salary[i] <= j*100:
			if fantasy_points[i] + Matrix[i-1][int((j*100 - salary[i])/100)] > Matrix[i-1][j]:
				Matrix[i][j] = fantasy_opfaints[i] + Matrix[i-1][int((j*100 - salary[i])/100)]
			else:
				Matrix[i][j] = Matrix[i-1][j]
		else:
			Matrix[i][j] = Matrix[i-1][j]

i = len(salary) - 1
sal = nba_salary - 1

for x in range(10):
	team = []
	team_salary = []
	while (i > 0) and (sal > 0):
		if Matrix[i][sal] != Matrix[i-1][sal]:
			team.append(players[i])
			team_salary.append(salary[i])
			sal -= int(salary[i]/100)
			i -= 1
		else:
			i -= 1
	top_picks.append(team)
	top_picks_salaries.append(team_salary)
	nextmax = max(Matrix[len(salary)-1][:(-1 * (x+1))])
	i = len(salary) - 1
	sal = Matrix[len(salary) - 1].index(nextmax)
	print("sal = ",sal)

for x in range(len(top_picks)):
	for y in range(len(top_picks[x])):
		print(top_picks[x][y])
	sum_salary = 0
	for z in top_picks_salaries[x]:
		sum_salary += z
	print("salary = ",sum_salary)
	print("\n\n")