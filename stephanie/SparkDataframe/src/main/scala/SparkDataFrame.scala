import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.DataFrame

import org.apache.spark.ml.Pipeline
import org.apache.spark.ml.evaluation.RegressionEvaluator
import org.apache.spark.ml.feature.{StringIndexer, VectorAssembler}
import org.apache.spark.ml.regression.GBTRegressor
import org.apache.spark.sql.types.{DoubleType, StringType, StructField, StructType}
import org.apache.spark.sql.{Encoders, SparkSession}

object SparkDataFrame {
  def main(args: Array[String]) {
    System.setProperty("hadoop.home.dir", "C:\\winutils")
    val spark = SparkSession
      .builder()
      .appName("Spark SQL basic example")
      .config("spark.master", "local")
      .getOrCreate()



    //reading a csv format, it has a header, the struct types are going to be inferred, and the file path is specified
    val df = spark.read.format("json").option("header","true")
      .load("C:\\Users\\steph\\Downloads\\SparkDataframe1\\SparkDataframe\\src\\main\\scala\\1k.json")

    df.show()

    //we need a subset
    val child = df
      .select("favorite_count","id","in_reply_to_screen_name", "is_quote_status", "reply_count" ,"retweeted", "text", "lang")
      .where("in_reply_to_screen_name is not null " +
        "and text is not null " +
        "and favorite_count is not null " +
        "and id is not null " +
        "and is_quote_status is not null " +
        "and reply_count is not null " +
        "and retweeted is not null " +
        "and text is not null" )
    child.show()

    //We'll split the set into training and test data
    val Array(trainingData, testData) = child.randomSplit(Array(0.8, 0.2))

    val labelColumn = "id"

    //We define two StringIndexers for the categorical variables

    val countryIndexer = new StringIndexer()
      .setInputCol("lang")
      .setOutputCol("replyIndex")

    //We define the assembler to collect the columns into a new column with a single vector - "features"
    val assembler = new VectorAssembler()
      .setInputCols(Array("reply_count", "replyIndex"))
      .setOutputCol("features")

    //For the regression we'll use the Gradient-boosted tree estimator
    val gbt = new GBTRegressor()
      .setLabelCol(labelColumn)
      .setFeaturesCol("features")
      .setPredictionCol("Predicted " + labelColumn)
      .setMaxIter(50).setMaxBins(100)

    //We define the Array with the stages of the pipeline
    val stages = Array(
      countryIndexer,
      assembler,
      gbt
    )

    //Construct the pipeline
    val pipeline = new Pipeline().setStages(stages)

    //We fit our DataFrame into the pipeline to generate a model
    val model = pipeline.fit(trainingData)

    //We'll make predictions using the model and the test data
    val predictions = model.transform(testData)
    predictions.show()

    //This will evaluate the error/deviation of the regression using the Root Mean Squared deviation
    val evaluator = new RegressionEvaluator()
      .setLabelCol(labelColumn)
      .setPredictionCol("Predicted " + labelColumn)
      .setMetricName("rmse")

    //We compute the error using the evaluator
    val error = evaluator.evaluate(predictions)


    println("The Root Mean Square Deviation error: " + error + "\n")

    spark.stop()

  }

}
