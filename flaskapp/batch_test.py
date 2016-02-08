from cassandra.cluster import Cluster
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
import os, sys
import pandas as pd

# Variable
keySpace='projet'
table='wikipediadata'
#conf = SparkConf().setAppName("Récupération donnees - calcul scores")
#sc = SparkContext(conf=conf)
#sql = SQLContext(sc)

# init connect
def connect():
	cluster = Cluster()
	session = cluster.connect(keySpace)
	
	return session

# get period with cassandra api
def get_period(session, date_from, date_to):
	rows = session.execute('SELECT projectcode, page, views FROM ' + keySpace + '.' + table +' WHERE day >= ' + date_from + ' and day <= ' + date_to + 'LIMIT 10 ALLOW FILTERING ;')	
	return rows

#def get_period_with_spark(sql, date_from, date_to):
#	df = sql.sql('SELECT projectcode, page, views FROM ' + keySpace + '.' + table +' WHERE day >= ' + date_from + ' and day <= ' + date_to + 'LIMIT 10;')
#	return df

# Convertir date 
def convert_date(date_from, date_to):
	return


#session = cluster()
#get_period(session, date_from, date_time)
def main():
	date_to = None
	date_from = None
	if len(sys.argv) == 3:
		date_to = sys.argv[2]
		date_from = sys.argv[1]
	if (date_to is not None) and (date_from is not None):
		session = connect()
		rows = get_period(session, date_from, date_to)
			
		#print df
		#all_data = sc.parallelize(rows)
		#df = sql.createDataFrame(all_data, ['projectcode', 'page', 'views', 'day', 'hour'])	


		#print type(rows)
		for row in rows:
			score_ranking = 0 
			print row.projectcode, row.page, row.views 
			
	return
if __name__ == "__main__":
    main()
