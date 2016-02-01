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
```bash
--clustername projet --totalnodes 5 --version enterprise --username ***@telecom-paristech.fr --password ***  --analyticsnodes 5 --cfsreplicationfactor 2
```

### Security groups
Cf. http://docs.datastax.com/en/datastax_enterprise/4.8/datastax_enterprise/install/installAMIsecurity.html
Ajouter 8080 pour Zeppelin


### Variables utiles
On les définit dans un fichier **projet-env.sh** qui a cette forme:
```bash
KEYFILE=ProjetNoSQL.pem
chmod 400 $KEYFILE
MASTER_DNS=ec2-54-165-93-154.compute-1.amazonaws.com
WORKER1_DNS=ec2-54-152-112-206.compute-1.amazonaws.com
WORKER2_DNS=
WORKER3_DNS=
WORKER4_DNS=
```

Par ailleurs on configure le fichier **spark-env.sh** que l'on aura au préalable éventuellement téléchargé depuis l'un des noeuds:
```bash
scp -i $KEYFILE ubuntu@$MASTER_DNS:/etc/dse/spark/spark-env.sh spark-env.sh.template
```

On modifie / ajoute les lignes suivantes (on veut augmenter les ressources allouées à Spark) :
```bash
export SPARK_WORKER_INSTANCES=3
export SPARK_WORKER_MEMORY="3G"
export SPARK_WORKER_CORES=1
export SPARK_DRIVER_MEMORY="2G"
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export PYSPARK_WORKER_PYTHON=/home/ubuntu/anaconda2/bin/python
export PYSPARK_PYTHON=/home/ubuntu/anaconda2/bin/python
export PYSPARK_DRIVER_PYTHON=/home/ubuntu/anaconda2/bin/ipython
export PYSPARK_DRIVER_PYTHON_OPTS="notebook"
```

### Commandes utiles
Se connecter en ssh
```bash
source projet-env.sh
ssh -i $KEYFILE ubuntu@$MASTER_DNS
ssh -i $KEYFILE ubuntu@$WORKER1_DNS
ssh -i $KEYFILE ubuntu@$WORKER3_DNS
```



### Config SPARK
On veut augmenter les ressources allouées à SPARK.   

On envoit le fichier de configuration à **tous** les noeuds et on 
relance les workers spark:
```bash
for DNS in $MASTER_DNS $WORKER1_DNS $WORKER2_DNS $WORKER3_DNS $WORKER4_DNS
do
scp -i $KEYFILE spark-env.sh ubuntu@$DNS:/home/ubuntu/
ssh -i $KEYFILE ubuntu@$DNS sudo mv /etc/dse/spark/spark-env.sh spark-env.sh /etc/dse/spark/spark-env.sh.original 
ssh -i $KEYFILE ubuntu@$DNS sudo cp spark-env.sh /etc/dse/spark/
ssh -i $KEYFILE ubuntu@$DNS dsetool sparkworker restart
done
```



### Jupyter Notebook
Telechargement d'Anaconda et installation sur **tous** les noeuds.
```bash
for DNS in $MASTER_DNS $WORKER1_DNS $WORKER2_DNS $WORKER3_DNS $WORKER4_DNS
do
ssh -i $KEYFILE ubuntu@$DNS wget https://3230d63b5fc54e62148e-c95ac804525aac4b6dba79b00b39d1d3.ssl.cf1.rackcdn.com/Anaconda2-2.4.1-Linux-x86_64.sh
ssh -i $KEYFILE ubuntu@$DNS bash Anaconda2-2.4.1-Linux-x86_64.sh -b
ssh -i $KEYFILE ubuntu@$DNS 'echo export PATH=/home/ubuntu/anaconda2/bin:$PATH >> /home/ubuntu/.bashrc'
ssh -i $KEYFILE ubuntu@$DNS "~/anaconda2/bin/pip install cassandra-driver"
done
```

Sur le noeud MASTER, effectuer les commandes suivantes pour paramétrer Jupyter.


Se connecter au MASTER:
```bash
ssh -i $KEYFILE ubuntu@$MASTER_DNS
```

Verifier la version de python
```bash
which python
which ipython
```

Si, le chemin ne liste pas ".../anaconda2/...", utilisez cette commande
```bash
source .bashrc
```

Creation d'un mote de passe, (copier le mdp: sha1:....)
```bash
ipython
```

```python
from IPython.lib import passwd
passwd()
exit
```

Creation de la config de jupyter
```bash
jupyter notebook --generate-config
```

Creation du certificat
```bash
mkdir certs
cd certs
sudo openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
```

Accéder au config
```bash
cd ~/.jupyter/
vim jupyter_notebook_config.py
```

Ajouter ce texte dans le document(ne pas oublier le mdp et le port)

```python
c = get_config()

# Kernel config
c.IPKernelApp.pylab = 'inline'  # if you want plotting support always in your notebook

# Notebook config
c.NotebookApp.certfile = u'/home/ubuntu/certs/mycert.pem' #location of your certificate file
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False  #so that the ipython notebook does not opens up a browser by default
c.NotebookApp.password = u'sha1:55c7434ac834:516251f1633a2abb54d1ac671e878f609b9a3548'  #the encrypted password we generated above
# It is a good idea to put it on a known, fixed port
c.NotebookApp.port = 8889
```

On clone le repository git pour faciliter la synchronisation
```bash
cd
git clone https://github.com/cygilbert/projetnosql.git
cd projetnosql
```

Lancement du notebook (écrivez https a lieu de http)
```bash
nohup dse pyspark --driver-memory 1G  --executor-memory 3G &
```

Pour arrêter, killer le process dont on trouve l'ID par :
```bash
lsof nohup.out
kill 6351
```

Pour lancer un script:
```bash
SCRIPT=/home/ubuntu/projetnosql/load_data.py
nohup dse spark-submit --driver-memory 2G  --executor-memory 3G  $SCRIPT &
```

### Updating replication factor
Lancer cqlsh
```bash
cqlsh
```

Mettre à jour le keyspace :
```sql
ALTER KEYSPACE "projet" WITH REPLICATION =
  { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };
```

Puis lancer le repair sur tous les noeuds:
```bash
for DNS in $MASTER_DNS $WORKER1_DNS $WORKER2_DNS $WORKER3_DNS $WORKER4_DNS
do
ssh -i $KEYFILE ubuntu@$DNS "nohup nodetool repair &"
done

```

