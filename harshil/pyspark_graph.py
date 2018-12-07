import findspark
findspark.init()
import pyspark as ps
import warnings
from pyspark.sql import SQLContext
from pyspark.sql.functions import udf, when, substring, col, lit, size

from functools import reduce
from pyspark.sql.functions import col, lit, when
from graphframes import *
import os

#os.environ["SPARK_HOME"]="C:\\spark\\spark-2.2.0-bin-hadoop2.7"
#os.environ["HADOOP_HOME"]="F:\\winutils"

try:
    # create SparkContext on all CPUs available: in my case I have 4 CPUs on my laptop
    sc = ps.SparkContext('local[4]')
    sqlContext = SQLContext(sc)
    print("Just created a SparkContext")
except ValueError:
    warnings.warn("SparkContext already exists in this scope")

sc.master
df = sqlContext.read.json("data.json")
print(df.count())

e = df.select(col("user.id").alias("src"),col("retweeted_status.user.id").alias("dst"),lit("retweet").alias("relationship"),).where(col("retweeted_status.user.id").isNotNull()).where(col("user.location")=="United States").distinct()
#v = df.select(col("user.id"),col("user.screen_name"))
v = df.select(col("user.id"),col("user.screen_name")).union(df.select(col("retweeted_status.user.id"),col("retweeted_status.user.name")).where(col("retweeted_status.user.id").isNotNull()).where(col("user.location")=="United States")).distinct()




g = GraphFrame(v, e)
g.degrees.show(5)
g.edges.show(5)
g.vertices.show(5)

#g.inDegrees.sort("inDegree", ascending=False).show(5, False)

#g.inDegrees.sort("inDegree").show(5, False)

#g.shortestPaths(landmarks=["25073877"]).select("id", "distances").where(size(col("distances")) > 0).show(10, False)

#g.triangleCount().select("id", "count").where(col("count") > 0).show(10, False)