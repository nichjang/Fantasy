import psycopg2
import parse_espn
import parse_dvp
import parse_game
import format_csv

//Truncates all tables in database
def truncate_everything():
	cur.execute("TRUNCATE espnseason;")
	cur.execute("TRUNCATE espnlastfive;")
	cur.execute("TRUNCATE espnseason_copy;")
	cur.execute("TRUNCATE gameinfo;")
	cur.execute("TRUNCATE linear_scores;")
	cur.execute("TRUNCATE results;")
	cur.execute("TRUNCATE dvp;")
	cur.execute("TRUNCATE currentdk;")

//Imports previous 13 dates into espnseason database	
def import_dates(current_date):
	for i in range(current_date,current_date-13,-1):
		print("Executing from date ",i,"...")
		cur.execute("TRUNCATE espnseason_copy;")
		statement = "COPY espnseason_copy(Player,Minutes,FGMFGA,FGPercent,FTM,FTPercent,ThreePM,REB,AST,STL,Block,PTS,Position,Team,Status) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\espn\\data{}.csv\' DELIMITER \',\' CSV;".format(i)
		cur.execute(statement)
		cur.execute("SELECT transfer_data()")
		
//Imports all previous dates into espnseason database
def import_dates_all(current_date):
	for i in range(current_date,0,-1):
		print("Executing from date ",i,"...")
		cur.execute("TRUNCATE espnseason_copy;")
		statement = "COPY espnseason_copy(Player,Minutes,FGMFGA,FGPercent,FTM,FTPercent,ThreePM,REB,AST,STL,Block,PTS,Position,Team,Status) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\espn\\data{}.csv\' DELIMITER \',\' CSV;".format(i)
		cur.execute(statement)
		cur.execute("SELECT transfer_data()")

//Executes function averagefive() which averages the 5 most recent games
def last_five():
	cur.execute("SELECT averagefive();")

//Imports salary and game info for a certain day, then uses ESPN information to output a list of projected player points and salaries
def execute_once():
	cur_date = 35

	truncate_everything()
	parse_game.parse('06')
	import_dates(cur_date+7)
	last_five()
	cur.execute("COPY gameinfo(team,teampoints,teamagainst) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\gameinfo.csv\' DELIMITER ',' CSV")
	cur.execute("COPY currentdk(position,name,salary,gameinfo,avgpoints,teamabbrev) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\salaries\\salaries12.6.format.csv\' DELIMITER ',' CSV")
	cur.execute("COPY dvp(team,position,dvp_percent) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\dvp.csv\' DELIMITER ',' CSV")
	cur.execute("COPY results(player,actualpoints) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\results\\results12.6.csv\' DELIMITER ',' CSV")
	cur.execute("SELECT update_salary()")
	cur.execute("SELECT update_results()")
	cur.execute("SELECT update_game()")
	cur.execute("SELECT stddev()")
	conn.commit()
	cur.execute("COPY (SELECT player,dkp,salary,position,gp,actualpoints,stddev FROM espnlastfive WHERE salary>2999) TO \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\xy.csv' With CSV DELIMITER ',';")
	conn.close()

conn  = psycopg2.connect(database="postgres", user="postgres", password="test")
conn.set_client_encoding('Latin1')
cur = conn.cursor()
execute_once()
