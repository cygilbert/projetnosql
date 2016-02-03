
# coding: utf-8

import time
import pandas as pd
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType


conf = SparkConf().setAppName("Calcul trends 30j")
sc = SparkContext(conf=conf)
hc = HiveContext(sc)

wikipediadata = hc.read.format("org.apache.spark.sql.cassandra") \
        .load(keyspace="projet", table="wikipediadata")


def filename(day):
    return '/home/ubuntu/projetnosql/day_{}_30jtrending.csv'.format(day)


def compute(day):
    # On veut les jours day-30 à day-1
    sums = wikipediadata.where(
            (wikipediadata.day >= day-30) & (wikipediadata.day <= day-1))

    # Sous-ensemble de test
    #sums = sums.where((sums.page == 'Cadillac_Brougham') | ((sums.page == 'Roald_Dahl') & (sums.projectcode == 'fr')))

    # On somme les heures de la journées
    sums = sums.groupby('projectcode', 'page', 'day').sum('views')
    # On cache pour plus tard
    sums.cache()

    # on définit une windows := jour precedent
    window_spec =  Window.partitionBy(sums.projectcode, sums.page) \
            .orderBy(sums.day.asc()).rowsBetween(-1, -1)

    # on calcule la différence entre views(d) - views(d-1)
    diffs = sums.withColumn('diff', sums.views - F.sum(sums.views) \
            .over(window_spec))

    # on calcule les coefs à appliquer à chaque jour
    coefs = pd.DataFrame({'day': range(day-30, day)})
    coefs['coef'] = 1. / (day - coefs.day)

    coefs = hc.createDataFrame(coefs)
    diffs = diffs.join(coefs, 'day')

    # on calcul le score de chaque jour
    diffs = diffs.withColumn('sub_score', diffs.diff * diffs.coef)

    totals = diffs.groupby('projectcode', 'page').sum('views', 'sub_score')
    # on normalise par la racine de la somme des views 
    totals = totals.withColumn('score',
            totals['SUM(sub_score)'] / F.sqrt(totals['SUM(views)'])) \
            .orderBy(F.desc('score')) \
            .withColumnRenamed('SUM(views)', 'total_views') \
            .limit(10)

    views = sums.select('projectcode', 'page', 'day', 'views') \
           .join(totals.select('projectcode', 'page', 'total_views', 'score'), 
                  (totals.projectcode == sums.projectcode) & (totals.page == sums.page), 'right_outer')

    df = totals.select('projectcode', 'page', 'total_views', 'score').toPandas()
    df2 = views.toPandas()
    df2 = df2.iloc[:, 2:]
    df2 = df2.pivot_table(values='views', columns=['day'], index=['projectcode', 'page'], fill_value=0)
    df = df.merge(df2, left_on=['projectcode', 'page'], right_index=True)
    df.to_csv(filename(day), index=False)
    
    # on vide le cache
    hc.clearCache()

    



for day in range(89, 29, -1):
    if os.path.exists(filename(day)):
        with open('/home/ubuntu/projetnosql/log_time', 'a') as f:
            f.write('\nFile {} already exists, skip day {}' \
                 .format(filename(day), day))
        continue

    try:
        t0 = time.time()
        compute(day)
        # on calcule la différence entre views jour courant - views jour précédent
        t1 = time.time()
        d = t1-t0
        m = int(d // 60)
        s = int(d % 60)
        with open('/home/ubuntu/projetnosql/log_time', 'a') as f:
            f.write('\n30j history of day {} written in {} min and {} sec'.format(day, m, s))
    except:
        with open('/home/ubuntu/projetnosql/log_errors', 'a') as f:
            f.write('\n30j history of day {} has not been correctly computed!'.format(day))     

