import org.apache.spark.sql.SparkSession
import org.graphframes.GraphFrame
import org.apache.spark.rdd.RDD
import scala.util.MurmurHash
import org.apache.spark.sql.{DataFrame, SQLContext}
import org.apache.spark.{SparkConf, SparkContext}

object SparkGraphFrame {
  class SimpleCSVHeader(header:Array[String]) extends Serializable {
    val index = header.zipWithIndex.toMap
    def apply(array:Array[String], key:String):String = array(index(key))
  }

  def main(args: Array[String]) {
    System.setProperty("hadoop.home.dir", "C:\\winutils")
    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.master", "local")
      .getOrCreate()

    /*val stations = spark.read.format("csv").option("header", "true").load("D:\\Downloads\\201508_station_data.csv")
    val trips = spark.read.format("csv").option("header", "true").load("D:\\Downloads\\201508_trip_data.csv")

    val input = stations.select("id", "dockcount", "landmark")
    val output = trips.select("src", "dst", "relationship")

    val g = GraphFrame(input, output)
    g.vertices.show()
    g.edges.show()*/

    val tweets = spark.read.format("csv").option("header", "true").load("C:\\Users\\calcalocalo\\Documents\\foodtweets.csv")
    tweets.createOrReplaceTempView("tweet")
    val v = spark.sql("select id, text, retweetCount from tweet where replyToSID <> 'NA'")
    val e = spark.sql("select id as src, replyToSID as dst from tweet where replyToSID <> 'NA'")

    val g = GraphFrame(v, e)
    g.vertices.show()
    g.edges.show()

    val youngest = g.vertices.groupBy().min("id ")
    youngest.show()
  }
}