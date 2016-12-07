import psycopg2
import parse_espn
import parse_dvp
import parse_game
import format_csv

def truncate_everything():
	cur.execute("TRUNCATE espnseason;")
	cur.execute("TRUNCATE espnlastfive;")
	cur.execute("TRUNCATE espnseason_copy;")
	cur.execute("TRUNCATE gameinfo;")
	cur.execute("TRUNCATE linear_scores;")
	cur.execute("TRUNCATE results;")
	cur.execute("TRUNCATE dvp;")
	cur.execute("TRUNCATE currentdk;")

def import_dates(current_date):
	for i in range(current_date,current_date-13,-1):
		print("Executing from date ",i,"...")
		cur.execute("TRUNCATE espnseason_copy;")
		statement = "COPY espnseason_copy(Player,Minutes,FGMFGA,FGPercent,FTM,FTPercent,ThreePM,REB,AST,STL,Block,PTS,Position,Team,Status) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\espn\\data{}.csv\' DELIMITER \',\' CSV;".format(i)
		cur.execute(statement)
		cur.execute("SELECT transfer_data()")

def import_dates_all(current_date):
	for i in range(current_date,0,-1):
		print("Executing from date ",i,"...")
		cur.execute("TRUNCATE espnseason_copy;")
		statement = "COPY espnseason_copy(Player,Minutes,FGMFGA,FGPercent,FTM,FTPercent,ThreePM,REB,AST,STL,Block,PTS,Position,Team,Status) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\espn\\data{}.csv\' DELIMITER \',\' CSV;".format(i)
		cur.execute(statement)
		cur.execute("SELECT transfer_data()")

def last_five():
	cur.execute("SELECT averagefive();")

def execute_range():
	espn_date = 25
	game_date_start = 18
	game_date_end = 29

	for cur_date in range(game_date_start,game_date_end+1,1):
		if cur_date != 24:
			truncate_everything()
			parse_game.parse(cur_date)
			import_dates(cur_date+7)
			last_five()
			cur.execute("COPY gameinfo(team,teampoints,teamagainst) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\gameinfo.csv\' DELIMITER ',' CSV")
			cur.execute("COPY currentdk(position,name,salary,gameinfo,avgpoints,teamabbrev) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries\\salaries11.%s.format.csv\' DELIMITER ',' CSV" % str(cur_date))
			cur.execute("COPY dvp(team,position,dvp_percent) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\dvp.csv\' DELIMITER ',' CSV")
			cur.execute("COPY results(player,actualpoints) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results\\results11.%s.csv\' DELIMITER ',' CSV" % str(cur_date))
			cur.execute("SELECT update_salary()")
			cur.execute("SELECT update_game()")
			cur.execute("SELECT update_results()")
			conn.commit()
			cur.execute("COPY (SELECT distinct(player),threepm,reb,ast,stl,block,pts,actualpoints,teampoints,teamagainstpoints,dvp FROM espnlastfive WHERE salary > 2999) TO \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict%s.csv' With CSV DELIMITER ',';" % str(cur_date))
	conn.close()

#These functions only need to be executed once
"""
parse_espn.parse_single(espn_date) #only if necessary
parse_dvp.parse()
parse_game.parse(game_date)
format_csv.format_sal(game_date_start,game_date_end)
format_csv.format_results(game_date_start,game_date_end)
"""
def all_dates():
	truncate_everything()
	import_dates_all(38)
	conn.commit()
	#cur.execute("COPY (SELECT distinct(player),dkp,teampoints,teamagainstpoints,dvp FROM espnlastfive WHERE salary > 2999) TO \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict.csv' With CSV DELIMITER ',';")
	conn.close()

def execute_once():
	cur_date = 35

	truncate_everything()
	#parse_game.parse(cur_date)
	parse_game.parse('06')
	import_dates(cur_date+7)
	last_five()
	cur.execute("COPY gameinfo(team,teampoints,teamagainst) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\gameinfo.csv\' DELIMITER ',' CSV")
	#cur.execute("COPY currentdk(position,name,salary,gameinfo,avgpoints,teamabbrev) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries11.%sformat.csv\' DELIMITER ',' CSV" % str(cur_date))
	cur.execute("COPY currentdk(position,name,salary,gameinfo,avgpoints,teamabbrev) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries\\salaries12.6.format.csv\' DELIMITER ',' CSV")
	cur.execute("COPY dvp(team,position,dvp_percent) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\dvp.csv\' DELIMITER ',' CSV")
	#cur.execute("COPY results(player,actualpoints) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results11.%sformat.csv\' DELIMITER ',' CSV" % str(cur_date))
	cur.execute("COPY results(player,actualpoints) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results\\results12.6.csv\' DELIMITER ',' CSV")
	cur.execute("SELECT update_salary()")
	cur.execute("SELECT update_results()")
	cur.execute("SELECT update_game()")
	cur.execute("SELECT stddev()")
	conn.commit()
	#cur.execute("COPY (SELECT distinct(player),threepm,reb,ast,stl,block,pts,teampoints,teamagainstpoints,dvp FROM espnlastfive WHERE salary > 2999) TO \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\data_predict.csv' With CSV DELIMITER ',';")
	cur.execute("COPY (SELECT player,dkp,salary,position,gp,actualpoints,stddev FROM espnlastfive WHERE salary>2999) TO \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\xy.csv' With CSV DELIMITER ',';")
	conn.close()

conn  = psycopg2.connect(database="postgres", user="postgres", password="test")
conn.set_client_encoding('Latin1')
cur = conn.cursor()
execute_once()
