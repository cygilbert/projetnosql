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
MASTER_DNS=ec2-54-210-109-141.compute-1.amazonaws.com
ssh -i $KEYFILE ubuntu@$MASTER_DNS
```

### Charger les données
```
Cf. https://drive.google.com/file/d/0B9Ikx0xPv9gJczJEdlptVGNWcVU/view
wget http://s3.amazonaws.com/ec2-downloads/ec2-api-tools.zip
unzip ec2-api-tools.zip
export PATH=$PATH:/home/ubuntu/ec2-api-tools-1.7.5.1/bin
export EC2_HOME=/home/ubuntu/ec2-api-tools-1.7.5.1
ec2-create-volume --snapshot snap-f57dec9a -z us-east-1a -O *** -W  ***
```
On note: 
vol-7e8989de 

```
ec2-attach-volume vol-7e8989de -i i-2c1e69a5 -d /dev/sdf -O *** -W *** 
```

### IPython
http://blog.insightdatalabs.com/jupyter-on-apache-spark-step-by-step/
```
sudo apt-get update
sudo pip install ipython[notebook]
echo "export AWS_ACCESS_KEY_ID=***" >> /home/ubuntu/.profile
echo "export AWS_SECRET_ACCESS_KEY=***" >> /home/ubuntu/.profile
source /home/ubuntu/.profile
PYSPARK_DRIVER_PYTHON=ipython 
PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --port=8880" pyspark --master $SPARK_MASTER
```


http://blog.cloudera.com/blog/2014/08/how-to-use-ipython-notebook-with-apache-spark/
```
sudo apt-get install python-markupsafe python-zmq python-singledispatch -y
sudo apt-get install python-jsonschema -y
sudo pip install backports_abc certifi
sudo pip install ipython
export SPARK_HOME=/usr/share/dse/spark/
export PYSPARK_SUBMIT_ARGS='--master spark://172.31.15.112:7077' 
ipython profile create pyspark
IPYTHON_CONFIG=/home/ubuntu/.ipython/profile_pyspark/ipython_config.py
echo "c = get_config()" >> $IPYTHON_CONFIG
echo "c.NotebookApp.ip = '*'" >> $IPYTHON_CONFIG
echo "c.NotebookApp.open_browser = False" >> $IPYTHON_CONFIG
echo "c.NotebookApp.port = 8880" >> $IPYTHON_CONFIG
echo "PWDFILE='~/.ipython/profile_pyspark/nbpasswd.txt'" >> $IPYTHON_CONFIG
echo "c.NotebookApp.password = open(PWDFILE).read().strip()" >> $IPYTHON_CONFIG
vim ~/.ipython/profile_pyspark/ipython_config.py
python -c 'from IPython.lib import passwd; print passwd()' > ~/.ipython/profile_pyspark/nbpasswd.txt
ipython notebook --profile=pyspark
```

```
FILE=00-pyspark-setup.py
~/.ipython/profile_pyspark/startup/
scp -i $KEYFILE $FILE ubuntu@$MASTER_DNS:/home/ubuntu/.ipython/profile_pyspark/startup/
```

### Zeppelin

#### Install & build
```
sudo apt-get install node git openjdk-7-jdk npm libfontconfig -y
wget http://apache.crihan.fr/dist/maven/maven-3/3.3.9/binaries/apache-maven-3.3.9-bin.tar.gz
sudo tar -zxf apache-maven-3.3.9-bin.tar.gz -C /usr/local/
sudo ln -s /usr/local/apache-maven-3.3.9/bin/mvn /usr/local/bin/mvn
sudo ln –s /usr/local/bin/nodejs /usr/local/bin/node
sudo ln -s /usr/bin/nodejs /usr/bin/node
export MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=1024m"
git clone https://github.com/apache/incubator-zeppelin.git
cd incubator-zeppelin
node --version
mvn --version
mvn clean package -DskipTests -Pcassandra-spark-1.4 -Ppyspark 
echo "export SPARK_HOME=/usr/share/dse/spark/" >> ./conf/zeppelin-env.sh
```

#### Launch
```
./bin/zeppelin-daemon.sh start
```

Puis se connecter à **http://$MASTER_DNS:8080/**

### Lancer simplement PySpark
```
IPYTHON=1 dse pyspark
```

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


                                                     
