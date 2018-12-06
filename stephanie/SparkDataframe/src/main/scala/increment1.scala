import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

object increment1 {
  def main(args: Array[String]) {
    System.setProperty("hadoop.home.dir", "C:\\winutils")
    /*val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.master", "local")
      .getOrCreate()*/


    val conf = new SparkConf().setAppName("PbSpark").setMaster("local[2]").set("spark.executor.memory", "4g")
    val sc = new SparkContext(conf)
    import org.apache.spark.sql.SQLContext
    val sqlContext = new SQLContext(sc)

    val EntertainmentTable = sqlContext.jsonFile("C:\\Users\\steph\\Downloads\\SparkDataframe1\\SparkDataframe\\src\\main\\scala\\1k.json")
    EntertainmentTable.registerTempTable("EntertainmentTable")
    //EntertainmentTable.printSchema();
    //how many tweets have been favorited out of 1000
    //1
    val favTweets = sqlContext
      .sql("SELECT favorited, count(*) as count FROM EntertainmentTable where favorited is not null  group by favorited order by count desc limit 10")
    favTweets.show



    //2
    val reTweets = sqlContext
      .sql("SELECT retweeted, count(*) as count FROM EntertainmentTable where retweeted is not null  group by retweeted order by count desc limit 10")
    reTweets.show

    //3
    val quoteTweets = sqlContext
      .sql("SELECT is_quote_status, count(*) as count FROM EntertainmentTable where is_quote_status is not null  group by is_quote_status order by count desc limit 10")
    quoteTweets.show

    //4
    val filterTweets = sqlContext
      .sql("SELECT filter_level, count(*) as count FROM EntertainmentTable where filter_level is not null group by filter_level order by count desc limit 10")
    filterTweets.show

    //5
    val truncatedTweets = sqlContext
      .sql("SELECT truncated, count(*) as count FROM EntertainmentTable where truncated is not null group by truncated order by count desc limit 10")
    truncatedTweets.show

    //6
    val tqTweets = sqlContext
      .sql("SELECT id, truncated, is_quote_status, count(*) as count FROM EntertainmentTable where truncated = true AND is_quote_status = true  group by id, truncated, is_quote_status order by count desc limit 10")
    tqTweets.show

    //7
    val createdTweets = sqlContext
      .sql("SELECT created_at, count(*) as count FROM EntertainmentTable where created_at is not null group by created_at order by count desc limit 15")
    createdTweets.show

    //8
    val replyCountTweets = sqlContext
      .sql("SELECT created_at, max(reply_count) as max_reply FROM EntertainmentTable where created_at is not null group by created_at order by max_reply desc limit 15")
    replyCountTweets.show

    //9
    val quoteCountTweets = sqlContext
      .sql("SELECT created_at, max(quote_count) as max_quote FROM EntertainmentTable where created_at is not null group by created_at order by max_quote desc limit 15")
    quoteCountTweets.show

    //10
    val protectedTweets = sqlContext
      .sql("SELECT user.protected, count(*) as count FROM EntertainmentTable where user.protected = false group by user.protected order by count desc limit 15")
    protectedTweets.show


  }

}
