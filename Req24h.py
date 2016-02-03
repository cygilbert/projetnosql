
# coding: utf-8

import time
import pandas as pd
import os
from pyspark import SparkContext, SparkConf
from pyspark.sql import HiveContext
from pyspark.sql.window import Window
import pyspark.sql.functions as F
from pyspark.sql.types import FloatType


conf = SparkConf().setAppName("Calcul trends 24h")
sc = SparkContext(conf=conf)
hc = HiveContext(sc)

wikipediadata = hc.read.format("org.apache.spark.sql.cassandra") \
        .load(keyspace="projet", table="wikipediadata")


def filename(day):
    return '/home/ubuntu/projetnosql/day_{}_24htrending.csv'.format(day)


def compute(day):
    # On veut les 24 dernieres heures de day
    sums = wikipediadata.where(wikipediadata.day == day)
    # Sous-ensemble de test
    #sums = sums.where((sums.page == 'Cadillac_Brougham') | ((sums.page == 'Roald_Dahl') & (sums.projectcode == 'fr')))

    # On cache pour plus tard
    sums.cache()

    # on définit une windows := heure précédente
    window_spec =  Window.partitionBy(sums.projectcode, sums.page) \
            .orderBy(sums.hour.asc()).rowsBetween(-1, -1)

    # on calcule la différence entre views(h) - views(h-1)
    diffs = sums.withColumn('diff', sums.views - F.sum(sums.views) \
            .over(window_spec))

    # on calcule les coefs à appliquer à chaque jour
    coefs = pd.DataFrame({'hour': range(24)})
    coefs['coef'] = 1. / (24. - coefs.hour)

    coefs = hc.createDataFrame(coefs)
    diffs = diffs.join(coefs, 'hour')

    # on calcul le score de chaque jour
    diffs = diffs.withColumn('sub_score', diffs.diff * diffs.coef)

    totals = diffs.groupby('projectcode', 'page').sum('views', 'sub_score')
    # on normalise par la racine de la somme des views 
    totals = totals.withColumn('score',
            totals['SUM(sub_score)'] / F.sqrt(totals['SUM(views)'])) \
            .orderBy(F.desc('score')) \
            .withColumnRenamed('SUM(views)', 'total_views') \
            .limit(10)

    views = sums.select('projectcode', 'page', 'hour', 'views') \
           .join(totals.select('projectcode', 'page', 'total_views', 'score'), 
                  (totals.projectcode == sums.projectcode) & (totals.page == sums.page), 'right_outer')

    df = totals.select('projectcode', 'page', 'total_views', 'score').toPandas()
    df2 = views.toPandas()
    df2 = df2.iloc[:, 2:]
    df2 = df2.pivot_table(values='views', columns=['hour'], index=['projectcode', 'page'], fill_value=0)
    df = df.merge(df2, left_on=['projectcode', 'page'], right_index=True)
    df.to_csv(filename(day), index=False)

    



for day in range(89, -1, -1):
    if os.path.exists(filename(day):
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
            f.write('\nday {} written in {} min and {} sec'.format(day, m, s))
    except:
        with open('/home/ubuntu/projetnosql/log_errors', 'a') as f:
            f.write('\nday {} has not been correctly computed!'.format(day))     

