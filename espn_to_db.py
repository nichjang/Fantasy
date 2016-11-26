import psycopg2

def import_dates():
	cur.execute("TRUNCATE espnseason;")
	for i in range(current_date-12,current_date+1,1):
		print("Executing from date ",i,"...")
		cur.execute("TRUNCATE espnseason_copy;")
		statement = "COPY espnseason_copy(Player,Minutes,FGMFGA,FGPercent,FTM,FTPercent,ThreePM,REB,AST,STL,Block,PTS,Position,Team,Status) FROM \'C:\\Users\\Nicholas\\Documents\\GitHub\\Fantasy\\espn\\data{}.csv\' DELIMITER \',\' CSV;".format(i)
		cur.execute(statement)
		cur.execute("SELECT transfer_data()")

def last_five():
	cur.execute("TRUNCATE espnlastfive;")
	cur.execute("SELECT averagefive();")

current_date = 24
conn  = psycopg2.connect(database = "postgres", user = "postgres", password = "test")
conn.set_client_encoding('Latin1')
cur = conn.cursor()
import_dates()
last_five()
conn.commit()
conn.close()