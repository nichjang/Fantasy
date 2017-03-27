class Player:
	def __init__(self,name,points,salary,position,gp,actualpoints,dvp,team):
		self.name = name
		self.points = points
		self.salary = salary
		self.position = position
		self.gp = gp
		self.actualpoints = actualpoints
		self.dvp = dvp
		self.team = team

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