import random
import math
import csv
import functools
from operator import add
from collections import Counter

csv_file = 'xy.csv'
players_out = []
exception_list = []
mod_list_first = {	
			}
team_mod = {
			}
max_team = {
			}
mod_list = mod_list_first

def import_players(file_name):
	players = [[] for _ in range(8)]
	with open(file_name,'r') as csvf:
		csvreader = csv.reader(csvf, delimiter=',')
		for row in csvreader:
			if (str(row[0]) not in players_out and int(row[2])>3600) or str(row[0]) in exception_list:
				stats = []
				stats.append(str(row[0])) #name
				if str(row[0]) in mod_list:
					stats.append(float(row[1]) * mod_list.get(row[0]))
				elif str(row[7]) in team_mod:
					stats.append(float(row[1]) * team_mod.get(row[7]))
				else:
					stats.append(float(row[1])) #points
				stats.append(int(row[2])) #salary
				stats.append(str(row[3])) #position
				stats.append(str(row[4])) #games played (if not 5)
				try :
					stats.append(float(row[5])) #actual points on day
				except ValueError:
					stats.append(float(0))
				except IndexError:
					stats.append(float(0))
				stats.append(float(row[6])) #dvp
				stats.append(str(row[7])) #team
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

def teamCount(team):
	temp_team = []
	for pos, players in team.items():
		for player in players:
			temp_team.append(player[7])
	counted_list = Counter(temp_team)
	for item in counted_list:
		if item in max_team and counted_list[item] > max_team[item]:
			return False
		if counted_list[item] > 2:
			return False
	return True


def isConsistent(team):
	temp_team = []
	for pos, players in team.items():
		for player in players:
			if player[0] in temp_team:
				return False
			else:
				temp_team.append(player[0])	
	if not teamCount(team):
		return False
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

num_cycles = 1
num_subcycles = 100
all_players = import_players(csv_file)
best_teams=[]
history = []
for i in range(num_cycles):
	print('Cycle ',i+1,' of', num_cycles)
	p = CreatePopulation(10000)
	fitness_history = [grade(p)]
	for j in range(num_subcycles):
		print('\tSubcycle ', j+1,' of ', num_subcycles, '...')
		p = evolve(p)
		fitness_history.append(grade(p))
		valid_teams = [ team for team in p if GetTeamSalary(team) <= 50000 and isConsistent(team)]
		valid_teams = sorted(valid_teams, key = GetTeamPointTotal, reverse = True)
		if len(valid_teams) > 0:
			for i in range(10):
				if GetTeamSalary(valid_teams[i]) <= 50000:
					#print(GetTeamSalary(valid_teams[i]))
					best_teams.append(valid_teams[i])
	for datum in fitness_history:
		history.append(datum)
	best_teams = sorted(best_teams, key = GetTeamPointTotal, reverse = True)

num_actual = 0

for i in range(49,-1,-1):
	print("Team Number : ",i)
	printTeam(best_teams[i])
	print(GetTeamSalary(best_teams[i]))
	print(GetTeamPointTotal(best_teams[i]))
	print("Actual point total",GetActualPointTotal(best_teams[i]))
	if (GetActualPointTotal(best_teams[i])>276.5):
		num_actual+=1
	print("number of 276.5: ", num_actual)

with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\lineup.csv', 'w') as csvf:
	csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
	for i in range(49,-1,-1):
		for pos,players in best_teams[i].items():
			for player in players:
				csvwriter.writerow(player)
		temp_list = []
		phrase = "salary is ", GetTeamSalary(best_teams[i])
		temp_list.append(phrase)
		phrase = "estimated point is ", GetTeamPointTotal(best_teams[i])
		temp_list.append(phrase)
		temp_list.append("-----------------------------------------")
		for item in temp_list:
			csvwriter.writerow(item)

print("\n\n")
player_list = list(best_teams[i].values() for i in range(50))
player_list = [item[0] for sublistone in player_list for sublisttwo in sublistone for item in sublisttwo]
counted_list = Counter(player_list) 
counted_list = [[item, counted_list[item]/float(50)] for item in counted_list]
counted_list = sorted(counted_list, key = lambda x:x[1],reverse = True)
for item in counted_list:
	print(item)