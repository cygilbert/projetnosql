
# coding: utf-8


# ## Chargement des données

import pandas as pd
import re
from time import time
from boto.s3.connection import S3Connection
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("Chargement des donnees par batch de 25")
sc = SparkContext(conf=conf)
sql = SQLContext(sc)


# Constantes du script:
W = 5 # nombre de workers (et donc de partitions de la liste de fichiers)
N = 25 # nombre de fichiers à lire en meme temps
I0 = 510 # premier fichier à lire

# On récupère la liste des fichiers


conn = S3Connection()
bucket = conn.get_bucket('telecom-bigdata-2016')
keys = bucket.list('projet/pagecounts')
datafiles = ['s3n://telecom-bigdata-2016/{}'.format(key.name) for key in keys]


# In[17]:

print('Il existe {} fichiers.'.format(len(datafiles)))


# A chaque fichier on associer un jour et une heure :

# In[18]:

def to_day_index(month, day):
    '''
    Parameters:
    -----------
    month : between 1 (january 2011) and 3 (march 2011)
    day : between 1 and 31
    Returns:
    --------
    day number starting from 2011'01'01 as 0
    '''
    days_in_month = [31, 28, 31]
    return sum(days_in_month[:month-1]) + (day - 1)    


# In[19]:

def to_month_day(day_index):
    '''
    Parameters:
    -----------
    day number starting from 2011'01'01 as 0 (max is 89)
    Returns:
    --------
    month : between 1 (january 2011) and 3 (march 2011)
    day : between 1 and 31
    '''
    if day_index < 31:
        return 1, day_index + 1
    elif day_index < 59:
        return 2, day_index - 30
    else:
        return 3, day_index - 58


# In[20]:

def extract_date(datafile):
    '''
    Return day (day 0 = 2011'01-01) and hour (from 0 to 23)
    '''
    rex = re.compile(r'.*pagecounts-(\d{4})(\d{2})(\d{2})-(\d{2}).*')
    s = rex.match(datafile)
    #datetime = '{}-{}-{} {}:00'.format(*(s.group(i) for i in range(1, 5)))
    day = to_day_index(int(s.group(2)), int(s.group(3)))
    hour = int(s.group(4))
    return day, hour


# In[21]:

datafiles_datetimes = [(datafile, extract_date(datafile)) for datafile in datafiles]


# On parallélise cette liste (on fait 10 partitions puisqu'on a 10 workers):

# Le travail de chaque worker est de :
# 1. charger un fichier (comme ce sont des fichiers zippés, ils ne peuvent pas être lus en parallèle : on utilisera donc pandas qui peut lire rapidement, en excluant une colonne)
# 2. appliquer les transformations nécessaires : ajouter une colonne *datetime*, retirer la colonne *weight*, retirer les lignes qui ne correspondent pas à un article Wikipedia (i.e. dont le code projet contient '.')
# 3. répéter 1. et 2. quatre fois (~ 1 Go max d'utilisation pour 4 fichiers, on a de la marge normalement puisque les workers ont 3 Go de RAM allouée) et concaténer le tout dans la même dataframe pandas
# 4. flatmapper le tout 


def create_df(datafile_datetime):
    '''
    Pandas nous permet de lire rapidement le fichier (on saute directement une colonne).
    Parameters:
    -----------
    datafile_datetime : 2-tuple with the filename and the date time
    '''
    datafile, (day, hour) = datafile_datetime
    df = pd.read_csv(datafile, sep=' ', compression='gzip', engine='c', header=None, 
                     names=['projectcode', 'page', 'views'], usecols=[0, 1, 2], 
                     na_values=None, keep_default_na=False,
                     dtype={'projectcode': pd.np.str, 'page': pd.np.str, 'views': pd.np.int64})
    # on supprime les pages non-wikipedia
    # on supprime les pages avec 1 seule vue (puisqu'on veut le trend, 1 et
    # 0 ce n'est pas très différent)
    df = df[(df.views > 1) & (~ df.projectcode.str.contains('\.'))]
    df['day'] = day
    df['hour'] = hour
    return df.values.tolist()




L = len(datafiles_datetimes) # nombre total de fichiers a lire
i = I0
while i < L:
    # indices de depart et de fin
    # (l'indice de fin est exclu)
    first = i
    last = min(L, i+N)
    i += N
     
    t0 = time()
    # Lecture des fichiers
    rdd = sc.parallelize(datafiles_datetimes[first:last], W)
    rdd2 = rdd.flatMap(create_df)
    df = sql.createDataFrame(rdd2, 
            ['projectcode', 'page', 'views', 'day', 'hour'])
    # Ecriture dans cassandra
    df.write.format("org.apache.spark.sql.cassandra").\
            options(table="wikipediadata", keyspace="projet").\
            save(mode="append")
    # Calcul et log du temps ecoule
    t1 = time()
    total = t1 - t0
    m = total // 60
    h = m // 60
    m = m % 60
    s = total % 60
    with open("/home/ubuntu/projetnosql/log_time", "a") as f:
        f.write('\nLecture et écritures des fichiers {}'
                'à {} en {} heures {} minutes et {:.0f} secondes.\n'.
                format(first, last-1, h, m, s))
