# Projet NoSQL
## Réflexion préliminaires
- Le choix de la base se fonde sur le type de requête à effectuer. 
Dans notre cas, il s'agit de sélectionner des dates contigües :
 **cassandra** / **hbase** sont bien adaptées au stockage séquentiel.

## Format de la base
1 fichier log / heure, sur trois mois.

|datetime | projectcode | pagnename | pageviews | bytes |
|---|---|---|---|---|
|xxx      | en          | Barack_Obama | 997 | 123091092|

## Schéma

Page Web / Notebook ---Requête (date)---> base (150 Go) ---30 jours (~13Go, traitement Spark)--> Page Web / Notebook
                      
## Plan d'action
1. Installation 
2. Chargement des données
3. ...

## Commandes AWS
### nom AMI datastax
ami-711ca91a
machine test :  5 x m3x2Large
### Instance type
|Instance Type | ECUs | vCPUsMemory (GiB)GiB | Instance Storage (GB)GB | EBS-Optimized Available | Network Performance |
| --- | --- | --- | --- | --- | --- |
| m3.2xlarge | 26 | 8 | 30 | 2 x 80 | Yes | High |

### Option lancement cluster
```
--clustername projet --totalnodes 5 --version enterprise --username ***@telecom-paristech.fr --password ***  --analyticsnodes 5 --cfsreplicationfactor 2
```

### Security groups
Cf. http://docs.datastax.com/en/datastax_enterprise/4.8/datastax_enterprise/install/installAMIsecurity.html
Ajouter 8080 pour Zeppelin


### Commandes utiles
Se connecter en ssh
```
KEYFILE=ProjetNoSQL.pem
chmod 400 $KEYFILE
MASTER_DNS=ec2-54-164-158-165.compute-1.amazonaws.com
ssh -i $KEYFILE ubuntu@$MASTER_DNS
```

### Zeppelin

#### Install & build
```
sudo apt-get install node git openjdk-7-jdk npm libfontconfig -y
wget http://www.eu.apache.org/dist/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.tar.gz
sudo tar -zxf apache-maven-3.3.3-bin.tar.gz -C /usr/local/
sudo ln -s /usr/local/apache-maven-3.3.3/bin/mvn /usr/local/bin/mvn
sudo ln –s /usr/loca/bin/nodejs /usr/local/bin/node
git clone https://github.com/apache/incubator-zeppelin.git
cd incubator-zeppelin
node --version
mvn --version
export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=1024m"
mvn clean package -DskipTests -Pcassandra-spark-1.4 -Ppyspark 
```

#### Launch
```
./bin/zeppelin-daemon.sh start
```

Puis se connecter à **http://localhost:8080/**
Uploader un script python
<pre>
FILE=add_key.py
scp -i $KEYFILE $FILE ubuntu@$MASTER_DNS:/home/ubuntu/
</pre>


Importer les données (**todo : commande  s3**):
<pre>
wget http://dumps.wikimedia.org/other/pagecounts-raw/2011/2011-01/pagecounts-20110101-000000.gz
gunzip pagecounts-20110101-000000.gz
python add_key.py
</pre>


Lancer le shell Cassandra :
<pre>
cqlsh
</pre>


Commandes Cassandra :
<pre>
create keyspace tp_nosql WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };
use tp_nosql;
create table wikipediadata (date timestamp, page text, views bigint, weights bigint, lang text, PRIMARY KEY (date,page)) ;
COPY tp_nosql.wikipediadata (dadte, lang, page, views, weights) FROM pagecounts-20110101-000000 WITH DELIMITER = ' ';
COPY music.imported_songs from 'songs-20140603.csv' WITH DELIMITER = ' ';
</pre>


                                                     
