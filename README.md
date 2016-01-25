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
### Option lancement cluster
<pre>
--clustername projet --totalnodes 5 --version community
</pre>

### Commandes utiles
Se connecter en ssh
<pre>
KEYFILE=ChallengeMaster.pem
MASTER_DNS=ec2-52-90-82-183.compute-1.amazonaws.com
ssh -i $KEYFILE ubuntu@$MASTER_DNS
</pre>

Uploader un script python
<pre>
KEYFILE=ChallengeMaster.pem
MASTER_DNS=ec2-52-90-82-183.compute-1.amazonaws.com
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


                                                     
