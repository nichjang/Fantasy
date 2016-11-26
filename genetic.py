import random
import math
import csv
import functools
from operator import add

csv_file = 'xy.csv'

def import_players(file_name):
	players = [[] for _ in range(8)]
	with open(file_name,'r') as x:
		reader = csv.reader(x, delimiter=',')
		for row in reader:
			stats = []
			stats.append(str(row[0])) #name
			stats.append(float(row[1])) #points
			stats.append(int(row[2])) #salary
			stats.append(str(row[3])) #position
			stats.append(str(row[4])) #games played (if not 5)
			stats.append(float(row[5])) #actual points on day
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
	return players

def CreateRandomTeam():    
	team = {
	'PG' : random.sample(all_players[0],1),
	'SG' : random.sample(all_players[1],1),
	'SF' : random.sample(all_players[2],1),
	'PF' : random.sample(all_players[3],1),
	'C' : random.sample(all_players[4],1),
	'G' : random.sample(all_players[5],1),
	'F' : random.sample(all_players[6],1),
	'UTIL' : random.sample(all_players[7],1)
	}
	return team
def GetActualPointTotal(team):
	total_points = 0
	for pos, players in team.items():
		for player in players:
			total_points += player[5]
	return total_points

def GetTeamPointTotal(team):
	total_points = 0
	for pos, players in team.items():
		for player in players:
			total_points += player[1]
	return total_points

def GetTeamSalary(team):
	total_salary = 0
	for pos, players in team.items():
		for player in players:
			total_salary += player[2]
	return total_salary

def printTeam(team):
	for pos, players in team.items():
		for player in players:
			print(player)

def CreatePopulation(count):
	return [CreateRandomTeam() for i in range(0,count)]

def isConsistent(team):
	temp_team = []
	for pos, players in team.items():
		for player in players:
			if player[0] in temp_team:
				return False
			else:
				temp_team.append(player[0])	
	return True

def fitness(team):
	points = GetActualPointTotal(team)
	salary = GetTeamSalary(team)
	if not isConsistent:
		return 0
	if salary > 50000:
		return 0
	return points

def grade(pop):
	summed = functools.reduce(add, (fitness(team) for team in pop))
	return summed / (len(pop) * 1.0)

def listToTeam(players):
	return {
	'PG' : [players[0]],
	'SG' : [players[1]],
	'SF' : [players[2]],
	'PF' : [players[3]],
	'C' : [players[4]],
	'G' : [players[5]],
	'F' : [players[6]],
	'UTIL' : [players[7]]
}

def breed(mother, father):
	positions = ['PG','SG','SF','PF','C','G','F','UTIL']
	
	mother_lists = [mother['PG'] + mother['SG'] + mother['SF'] + mother['PF'] + mother['C'] + mother['G'] + mother['F'] + mother['UTIL']]
	mother_list = [item for sublist in mother_lists for item in sublist]
	father_lists = [father['PG'] + father['SG'] + father['SF'] + father['PF'] + father['C'] + father['G'] + father['F'] + father['UTIL']] 
	father_list = [item for sublist in father_lists for item in sublist]

	index = random.choice([1,2,3,4,5,6,7])
	child1 = listToTeam(mother_list[0:index] + father_list[index:])
	child2 = listToTeam(father_list[0:index] + mother_list[index:])
		
	return[child1, child2]

def mutate(team):
	positions = ['PG','SG','SF','PF','C','G','F','UTIL']
	  
	random_pos = random.choice(positions)
	if random_pos == 'PG':
		team['PG'] = [random.choice(all_players[0])]
	if random_pos == 'SG':
		team['SG'] = [random.choice(all_players[1])]
	if random_pos == 'SF':
		team['SF'] = [random.choice(all_players[2])]
	if random_pos == 'PF':
		team['PF'] = [random.choice(all_players[3])]
	if random_pos == 'C':
		team['C'] = [random.choice(all_players[4])]
	if random_pos == 'G':
		team['G'] = [random.choice(all_players[5])]
	if random_pos == 'F':
		team['F'] = [random.choice(all_players[6])]
	if random_pos == 'UTIL':
		team['UTIL'] = [random.choice(all_players[7])]

	return team

def evolve(pop, retain=0.25, random_select=0.025, mutate_chance=0.015):
	graded = [(fitness(team),team) for team in pop]
	graded.reverse()
	graded = [item[1] for item in graded]
	retain_length = int(len(graded)*retain)
	parents = graded[:retain_length]

	# randomly add other individuals to promote genetic diversity
	for individual in graded[retain_length:]:
		if random_select > random.random():
			parents.append(individual)

	# mutate some individuals
	for individual in parents:
		if mutate_chance > random.random():
			individual = mutate(individual)

	# crossover parents to create children
	parents_length = len(parents)
	desired_length = len(pop) - parents_length
	children = []
	while len(children) < desired_length:
		male = random.randint(0, parents_length-1)
		female = random.randint(0, parents_length-1)
		if male != female:
			male = parents[male]
			female = parents[female]
			babies = breed(male,female)
			for baby in babies:
				children.append(baby)
	parents.extend(children)
	return parents

num_cycles = 1000
all_players = import_players(csv_file)
best_teams=[]
history = []
p = CreatePopulation(10000)
fitness_history = [grade(p)]
for i in range(num_cycles):
	print('Cycle ', i+1,' of ', num_cycles, '...')
	p = evolve(p)
	fitness_history.append(grade(p))
	valid_teams = [ team for team in p if GetTeamSalary(team) <= 50000 and isConsistent(team)]
	valid_teams = sorted(valid_teams, key = GetActualPointTotal, reverse = True)
	if len(valid_teams) > 0:
		for x in range(10):
			best_teams.append(valid_teams[x])
for datum in fitness_history:
	history.append(datum)
best_teams = sorted(best_teams, key = GetActualPointTotal, reverse = True)

for i in range(25,-1,-1):
	print("Team Number : ",i)
	printTeam(best_teams[i])
	print(GetTeamSalary(best_teams[i]))
	print(GetTeamPointTotal(best_teams[i]))
	print("Actual point total",GetActualPointTotal(best_teams[i]))