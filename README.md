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
| m3.xlarge | 4 | 13 | 15 | 2 x 40 SSD | Yes | High |

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
KEYFILE=cluster.pem
chmod 400 $KEYFILE
MASTER_DNS=ec2-54-165-93-154.compute-1.amazonaws.com
WORKER_DNS=ec2-54-152-112-206.compute-1.amazonaws.com
ssh -i $KEYFILE ubuntu@$MASTER_DNS
ssh -i $KEYFILE ubuntu@$WORKER_DNS
```

### Charger les données
Cf. https://drive.google.com/file/d/0B9Ikx0xPv9gJczJEdlptVGNWcVU/view
```
AWS_ACCESS_KEY_ID=XXX
AWS_SECRET_ACCESS_KEY=XXX
wget http://s3.amazonaws.com/ec2-downloads/ec2-api-tools.zip
unzip ec2-api-tools.zip
export PATH=$PATH:/home/ubuntu/ec2-api-tools-1.7.5.1/bin
export EC2_HOME=/home/ubuntu/ec2-api-tools-1.7.5.1
ec2-create-volume --snapshot snap-f57dec9a -z us-east-1a -O $AWS_ACCESS_KEY_ID -W $AWS_SECRET_ACCESS_KEY
```

Noter le volume_id. Puis:
```
VOLUME_ID=vol-ce72716e 
INSTANCE_ID=i-dc691f55
ec2-attach-volume $VOLUME_ID -i $INSTANCE_ID -d /dev/sdf -O $AWS_ACCESS_KEY_ID -W $AWS_SECRET_ACCESS_KEY
```

### Config SPARK
On veut augmenter les ressources allouées à SPARK.   

On envoit le fichier de configuration à **tous** les noeuds et on 
relance les workers spark:
```
for DNS in $MASTER_DNS $WORKER_DNS
do
scp -i $KEYFILE spark-env.sh ubuntu@$DNS:/home/ubuntu/
ssh -i $KEYFILE ubuntu@$DNS sudo cp spark-env.sh /etc/dse/spark/
ssh -i $KEYFILE ubuntu@$DNS dsetool sparkworker restart
done
```





### Jupyter Notebook
Telechargement d'Anaconda (Accepter les divers termes) et installation sur **tous** les noeuds.
```
wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh
bash Anaconda2-2.4.1-Linux-x86_64.sh -b
echo export PATH=/home/ubuntu/anaconda2/bin/:$PATH >> /home/ubuntu/.bashrc
source ~/.bashrc
pip install cqlsh
```
Verifier la version de python
```
which python
which ipython
```
Si, le chemin ne liste pas ".../anaconda2/...", utilisez cette commande
```
source .bashrc
```
Creation d'un mote de passe, (copier le mdp: sha1:....)
```
ipython
In [1]:from IPython.lib import passwd
In [2]:passwd()
```
Creation de la config de jupyter
```
$ jupyter notebook --generate-config
```
Creation du certificat
```
$ mkdir certs
$ cd certs
$ sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
```
Accéder au config
```
$ cd ~/.jupyter/
$ vi jupyter_notebook_config.py
```
Ajouter ce texte dans le document(ne pas oublier le mdp et le port)

```
c = get_config()

# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook

# Notebook config
c.NotebookApp.certfile = u'/home/ubuntu/certs/mycert.pem' #location of your certificate file
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
c.NotebookApp.password = u'sha1:68c136a5b064...'  #the encrypted password we generated above
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = 8889
```

Creation du dossier de notebook
```
$ cd ~
$ mkdir Notebooks
$ cd Notebooks
```

Lancement du notebook (ecrivez https a lieu de http)
```
source ~/.bashrc
PYSPARK_WORKER_PYTHON=python PYSPARK_DRIVER_PYTHON=ipython PYSPARK_DRIVER_PYTHON_OPTS="notebook" nohup dse pyspark --driver-memory 4G  --executor-memory 3G &
```

Pour arrêter, killer le process dont on trouve l'ID par :
```
lsof nohup.out
```



Lancer le shell Cassandra :
```
export PATH=/usr/bin/:$PATH
cqlsh
```


Commandes Cassandra pour créer la table:
```
create keyspace projet WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };
use projet;
create table projet.wikidata (datetime timestamp, page text, projectcode text, views bigint, PRIMARY KEY (datetime, page, projectcode)) ;
```

Quitter le shell et re-binder le PATH python to Anaconda
```
exit
source /home/ubuntu/.bashrc
```
