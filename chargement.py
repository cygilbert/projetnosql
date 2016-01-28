from cassandra.cluster import Cluster
import datetime
from pyspark import SparkContext, SparkConf
import os
import time
import datetime
import gzip


myKeySpace = "test_frompython"
myTable = "wikipediaData"
myPath = "/home/largo/workspace/telecom/basesnosql/data"
masterSpark = "local[1]"
formatFile = "pagecounts-%Y%m%d-%H%M%S.gz"


listFiles = []
for f in os.listdir(myPath):
        listFiles.append(f)

def initCluster():
	cluster = Cluster(['ec2-54-152-75-201.compute-1.amazonaws.com'])
	session = cluster.connect()
	#Creating the keyspace
	session.execute("CREATE KEYSPACE " + myKeySpace + " WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };")

	#Creating the table
	session.set_keyspace(myKeySpace)
	session.execute("create table " + myKeySpace + "." + myTable + " (date timestamp, page text, views bigint, weights bigint, lang text, PRIMARY KEY (date,page,lang)) ;")
	cluster.shutdown()
	return True


def process_data(inputFile):
	cluster = Cluster(['ec2-54-152-75-201.compute-1.amazonaws.com'])
	session = cluster.connect()
	session.set_keyspace(myKeySpace)
	date = datetime.datetime.strptime(inputFile, formatFile)
	fo=gzip.open(myPath + "/" + inputFile, 'r')
	for line in fo:
		#print (line)
		session.execute("INSERT INTO " + myTable + " (date, page,views,weights,lang) VALUES (%s,%s,%s,%s,%s)",(date,line.split(" ")[1],int(float(line.split(" ")[2])),int(float(line.split(" ")[3])),line.split(" ")[0]))
	cluster.shutdown()
		#print (line)
	#print(date)


#initCluster()
conf = SparkConf().setAppName("ProjetNoSQL").setMaster(masterSpark)
sc = SparkContext(conf=conf)

#Parallelize files from entry
distData = sc.parallelize(listFiles)
distData.foreach(process_data)







#Feeding data
#session.execute("INSERT INTO " + myTable + " (date, page,views,weights,lang) VALUES (%s,%s,%s,%s,%s)",("122222322","johnyhalliday",1232,123,"fr"))


#session = cluster.connect(myKeySpace)

