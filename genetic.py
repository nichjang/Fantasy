import random
import math
import csv
import functools
from operator import add
from collections import Counter

csv_file = 'xy.csv'
players_out = []
exception_list = []
mod_list_first = {}
team_mod = {}
max_team = {}
min_team = {}
mod_list = mod_list_first

class Player:
	def __init__(self,name,points,salary,position,gp,actualpoints,dvp,team):
		self.name = name;
		self.points = points;
		self.salary = salary;
		self.position = position;
		self.gp = gp;
		self.actualpoints = actualpoints;
		self.dvp = dvp;
		self.team = team;

	def __str__(self):
		return '{} {} {} {} {} {} {} {}'.format(self.name,self.points,self.salary,self.position,self.gp,self.actualpoints,self.dvp,self.team)

	def GetSalary(self):
		return self.salary

	def GetPoints(self):
		return self.points

	def GetActualPoints(self):
		return self.actualpoints

	def GetTeam(self):
		return self.team

	def GetName(self):
		return self.name

	def GetList(self):
		return [self.name,self.points,self.salary,self.position,self.gp,self.actualpoints,self.dvp,self.team]

def import_players(file_name):
	players = [[] for _ in range(8)]
	with open(file_name,'r') as csvf:
		csvreader = csv.reader(csvf, delimiter=',')
		for row in csvreader:
			if (str(row[0]) not in players_out and int(row[2])>3600) or str(row[0]) in exception_list:
				name = str(row[0])
				salary = int(row[2])
				position = str(row[3])
				gp = str(row[4])
				dvp = float(row[6])
				team = str(row[7])
				try:
					actualpoints = float(row[5])
				except (ValueError,IndexError):
					actualpoints = float(0)
				if name in mod_list:
					points = float(row[1]) * mod_list.get(name)
				elif team in team_mod:
					points =  float(row[1]) * team_mod.get(team)
				else:
					points = float(row[1])
				
				if position == 'PG':
					players[0].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'SG':
					players[1].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'SF':
					players[2].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'PF':
					players[3].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'C':
					players[4].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'G':
					players[5].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'F':
					players[6].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
				elif position == 'UTIL':
					players[7].append(Player(name,points,salary,position,gp,actualpoints,dvp,team))
	return players

def CreateRandomTeam():
	team = {
	'PG' : random.choice(all_players[0]),
	'SG' : random.choice(all_players[1]),
	'SF' : random.choice(all_players[2]),
	'PF' : random.choice(all_players[3]),
	'C' : random.choice(all_players[4]),
	'G' : random.choice(all_players[5]),
	'F' : random.choice(all_players[6]),
	'UTIL' : random.choice(all_players[7])
	}
	return team

def GetActualPointTotal(team):
	total_points = 0
	for pos, player in team.items():
		total_points += player.GetActualPoints()
	return total_points

def GetTeamPointTotal(team):
	total_points = 0
	for pos, player in team.items():
		total_points += player.GetPoints()
	return total_points

def GetTeamSalary(team):
	total_salary = 0
	for pos, player in team.items():
		total_salary += player.GetSalary()
	return total_salary

def printTeam(team):
	for pos, player in team.items():
		print(player)

def CreatePopulation(count):
	return [CreateRandomTeam() for i in range(0,count)]

def teamCount(team):
	temp_team = []
	for pos, player in team.items():
		temp_team.append(player.GetTeam())
	counted_list = Counter(temp_team)
	for item in counted_list:
		if item in max_team and counted_list[item] > max_team[item]:
			return False
		if item in min_team and counted_list[item]< min_team[item]:
			return False
	return True


def isConsistent(team):
	temp_team = []
	for pos, player in team.items():
		if player.GetName() in temp_team:
			return False
		else:
			temp_team.append(player.GetName())	
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
	'PG' : players[0],
	'SG' : players[1],
	'SF' : players[2],
	'PF' : players[3],
	'C' : players[4],
	'G' : players[5],
	'F' : players[6],
	'UTIL' : players[7]
}

def breed(mother, father):
	positions = ['PG','SG','SF','PF','C','G','F','UTIL']
	
	mother_list = [mother['PG'], mother['SG'], mother['SF'], mother['PF'], mother['C'], mother['G'], mother['F'], mother['UTIL']]
	#mother_list = [item for sublist in mother_lists]
	father_list = [father['PG'],father['SG'], father['SF'], father['PF'], father['C'], father['G'], father['F'], father['UTIL']] 
	#father_list = [item for sublist in father_lists]

	index = random.choice([1,2,3,4,5,6,7])
	child1 = listToTeam(mother_list[0:index] + father_list[index:])
	child2 = listToTeam(father_list[0:index] + mother_list[index:])
		
	return [child1, child2]

def mutate(team):
	positions = ['PG','SG','SF','PF','C','G','F','UTIL']
	
	random_pos = random.choice(positions)
	if random_pos == 'PG':
		team['PG'] = random.choice(all_players[0])
	if random_pos == 'SG':
		team['SG'] = random.choice(all_players[1])
	if random_pos == 'SF':
		team['SF'] = random.choice(all_players[2])
	if random_pos == 'PF':
		team['PF'] = random.choice(all_players[3])
	if random_pos == 'C':
		team['C'] = random.choice(all_players[4])
	if random_pos == 'G':
		team['G'] = random.choice(all_players[5])
	if random_pos == 'F':
		team['F'] = random.choice(all_players[6])
	if random_pos == 'UTIL':
		team['UTIL'] = random.choice(all_players[7])

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

def ExecuteRun(cycles,subcycles,top_teams):
	num_cycles = cycles
	num_subcycles = subcycles
	global all_players
	all_players = import_players(csv_file)
	best_teams=[]
	best_teams_n = []
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
			for i in range(min(top_teams,len(valid_teams))):
				if GetTeamSalary(valid_teams[i]) <= 50000:
					best_teams.append(valid_teams[i])
		for datum in fitness_history:
			history.append(datum)
		best_teams = sorted(best_teams, key = GetTeamPointTotal, reverse = True)
		for item in best_teams:
			if item not in best_teams_n and GetTeamSalary(item)<=50000:
				best_teams_n.append(item)

	num_actual = 0

	for i in range(top_teams-1,-1,-1):
		print("Team Number : ",i)
		printTeam(best_teams_n[i])
		print(GetTeamSalary(best_teams_n[i]))
		print(GetTeamPointTotal(best_teams_n[i]))
		print("\n")

	with open('C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\lineup.csv', 'w') as csvf:
		csvwriter = csv.writer(csvf, delimiter=',', lineterminator='\n')
		for i in range(top_teams-1,-1,-1):
			for pos,player in best_teams_n[i].items():
				csvwriter.writerow(player.GetList())
			temp_list = []
			phrase = "salary is ", GetTeamSalary(best_teams_n[i])
			temp_list.append(phrase)
			phrase = "estimated point is ", GetTeamPointTotal(best_teams_n[i])
			temp_list.append(phrase)
			temp_list.append("-----------------------------------------")
			for item in temp_list:
				csvwriter.writerow(item)

	player_list = list(list(best_teams_n[i].values()) for i in range(top_teams))
	player_list = [item.GetName() for sublist in player_list for item in sublist]
	counted_list = Counter(player_list) 
	counted_list = [[item, counted_list[item]/float(top_teams)] for item in counted_list]
	counted_list = sorted(counted_list, key = lambda x:x[1],reverse = True)
	for item in counted_list:
		print(item)

all_players = []
ExecuteRun(1,100,50)