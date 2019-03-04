import sys.process._
import java.net.URL
import java.io.File
import java.io.File
import java.nio.file.{Files, StandardCopyOption}
import java.net.HttpURLConnection 
import org.apache.spark.sql.functions._

import org.apache.spark.input.PortableDataStream
import java.util.zip.ZipInputStream
import java.io.BufferedReader
import java.io.InputStreamReader
import org.apache.spark.{SparkConf, SparkContext}

import com.amazonaws.services.s3.AmazonS3Client
import com.amazonaws.auth.BasicAWSCredentials

import org.apache.commons.lang.StringUtils
import org.apache.spark.sql.types._;
import org.apache.spark.sql._;
import org.apache.spark.sql.SQLContext
import java.sql.Date
import java.text.SimpleDateFormat
import scala.util.Try
    
val AWS_ID = "AKIAJNW545DSRAJK6IOQ"
val AWS_KEY = "OrTgAeLFrgL76/+7XFieHC4hoz9gtFZpNx4lCnW/"
val awsClient = new AmazonS3Client(new BasicAWSCredentials(AWS_ID, AWS_KEY))

sc.hadoopConfiguration.set("fs.s3a.access.key", AWS_ID) // mettre votre ID du fichier credentials.csv
sc.hadoopConfiguration.set("fs.s3a.secret.key", AWS_KEY) // mettre votre secret du fichier credentials.csv


val textRDD = sc.binaryFiles("s3a://gdelt-tdenimal/201806.export.CSV.zip"). // charger quelques fichers via une regex
   flatMap {  // decompresser les fichiers
       case (name: String, content: PortableDataStream) =>
          val zis = new ZipInputStream(content.open)
          Stream.continually(zis.getNextEntry).
                takeWhile(_ != null).
                flatMap { _ =>
                    val br = new BufferedReader(new InputStreamReader(zis))
                    Stream.continually(br.readLine()).takeWhile(_ != null)
                }
    }

def convertExportarrayToRow (array: Array[String]) : Row = {
    //recuperer les fields et les transformer en Row

    var r :Seq[Any] = Seq()
    r = r :+ array(0).toLong
    r = r :+ array(1).toInt
    r = r :+ array(2).toInt
    r = r :+ array(3).toInt
    
    //FractionDate
   if(Try(array(4).toDouble).getOrElse(null) == null) {r = r :+ null}
    else{ r = r :+ array(4).toDouble }

   // Actor1
   r = r :+ array(5) :+ array(6) :+ array(7) :+ array(8) :+ array(9) :+ array(10) :+ array(11) :+ array(12) :+ array(13) :+ array(14)
   
//   // Actor2
   r = r :+ array(15) :+ array(16) :+ array(17) :+ array(18) :+ array(19) :+ array(20) :+ array(21) :+ array(22) :+ array(23) :+ array(24)
   
  // IsRootEvent
  r = r :+ "1".equals(array(25))
   
  r = r :+ array(26) //EventCode
  r = r :+ array(27) //EventBaseCode
  r = r :+ array(28) //EventRootCode
   
    //QuadClass
   if(Try(array(29).toInt).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(29).toInt }
   
    //GoldsteinScale
   if(Try(array(30).toDouble).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(30).toDouble }
   
    //NumMentions
   if(Try(array(31).toInt).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(31).toInt }
   
    //NumSources
   if(Try(array(32).toInt).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(32).toInt }
   
    //NumArticles
   if(Try(array(33).toInt).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(33).toInt }

    //AvgTone
   if(Try(array(34).toDouble).getOrElse(null) == null) {r = r :+ null}
  else{ r = r :+ array(34).toDouble }

   
    // // ACTOR1GEO
      r = r :+ array(35)
      r = r :+ array(36)
      r = r :+ array(37)
      r = r :+ array(38)
      r = r :+ array(39)
       
   if(Try(array(40).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(40).toDouble }
       
   if(Try(array(41).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(41).toDouble }
       
      r = r :+ array(42)

    // // ACTOR2GEO
      r = r :+ array(43)
      r = r :+ array(44)
      r = r :+ array(45)
      r = r :+ array(46)
      r = r :+ array(47)
       
   if(Try(array(48).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(48).toDouble }
       
   if(Try(array(49).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(49).toDouble }
       
      r = r :+ array(50)
       
    // // ACTIONGEO
      r = r :+ array(51)
      r = r :+ array(52)
      r = r :+ array(53)
      r = r :+ array(54)
      r = r :+ array(55)
       
   if(Try(array(56).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(56).toDouble }
       
   if(Try(array(57).toDouble).getOrElse(null) == null) {r = r :+ null}
      else{ r = r :+ array(57).toDouble }
       
       r = r :+ array(58)
    
    // // DATEADDED 20180128081500
    val dateFormat = new SimpleDateFormat("yyyyMMddhhmmss")
      if(array(59) == null || array(57).length() == 0) {r = r :+ null}
      else{ r = r :+ new java.sql.Date(dateFormat.parse(array(59)).getTime()) }

   if(Try(array(60)).getOrElse(null) == null) {r = r :+ null}
   else{ r = r :+ array(60) }


  ////  tranform seq to  row
   val rowfromseq= Row.fromSeq(r)

   return  rowfromseq
 }


 val dfSchema =  StructType(
    Seq(
    StructField(name = "EventId", dataType = LongType, nullable = false),
      StructField(name = "Day", dataType = IntegerType, nullable = false),
      StructField(name = "MonthYear", dataType = IntegerType, nullable = false),
      StructField(name = "Year", dataType = IntegerType, nullable = false),
      StructField(name = "FractionDate", dataType = DoubleType, nullable = false),
      StructField(name = "Actor1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Name", dataType = StringType, nullable = true),
      StructField(name = "Actor1CountryCode", dataType = StringType, nullable = true),
      StructField(name = "Actor1KnownGroupCode", dataType = StringType, nullable = true),
      StructField(name = "Actor1EthnicCode", dataType = StringType, nullable = true),
      StructField(name = "Actor1Religion1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Religion2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Type1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Type2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Type3Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Name", dataType = StringType, nullable = true),
      StructField(name = "Actor2CountryCode", dataType = StringType, nullable = true),
      StructField(name = "Actor2KnownGroupCode", dataType = StringType, nullable = true),
      StructField(name = "Actor2EthnicCode", dataType = StringType, nullable = true),
      StructField(name = "Actor2Religion1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Religion2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Type1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Type2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Type3Code", dataType = StringType, nullable = true),
      StructField(name = "IsRootEvent", dataType = BooleanType, nullable = true),
      StructField(name = "EventCode", dataType = StringType, nullable = true),
      StructField(name = "EventBaseCode", dataType = StringType, nullable = true),
      StructField(name = "EventRootCode", dataType = StringType, nullable = true),
      StructField(name = "QuadClass", dataType = IntegerType, nullable = true),
      StructField(name = "GoldsteinScale", dataType = DoubleType, nullable = true),
      StructField(name = "NumMentions", dataType = IntegerType, nullable = true),
      StructField(name = "NumSources", dataType = IntegerType, nullable = true),
      StructField(name = "NumArticles", dataType = IntegerType, nullable = true),
      StructField(name = "AvgTone", dataType = DoubleType, nullable = true),
      StructField(name = "Actor1Geo_Type", dataType = StringType, nullable = true),
      StructField(name = "Actor1Geo_FullName", dataType = StringType, nullable = true),
      StructField(name = "Actor1Geo_CountryCode", dataType = StringType, nullable = true),
      StructField(name = "Actor1Geo_ADM1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Geo_ADM2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor1Geo_Lat", dataType = DoubleType, nullable = true),
      StructField(name = "Actor1Geo_Long", dataType = DoubleType, nullable = true),
      StructField(name = "Actor1Geo_FeatureID", dataType =  StringType, nullable = true),
      StructField(name = "Actor2Geo_Type", dataType = StringType, nullable = true),
      StructField(name = "Actor2Geo_FullName", dataType = StringType, nullable = true),
      StructField(name = "Actor2Geo_CountryCode", dataType = StringType, nullable = true),
      StructField(name = "Actor2Geo_ADM1Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Geo_ADM2Code", dataType = StringType, nullable = true),
      StructField(name = "Actor2Geo_Lat", dataType = DoubleType, nullable = true),
      StructField(name = "Actor2Geo_Long", dataType = DoubleType, nullable = true),
      StructField(name = "Actor2Geo_FeatureID", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_Type", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_FullName", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_CountryCode", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_ADM1Code", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_ADM2Code", dataType = StringType, nullable = true),
      StructField(name = "ActionGeo_Lat", dataType = DoubleType, nullable = true),
      StructField(name = "ActionGeo_Long", dataType = DoubleType, nullable = true),
      StructField(name = "ActionGeo_FeatureID", dataType = StringType, nullable = true),
      StructField(name = "DATEADDED", dataType = DateType, nullable = true),
      StructField(name = "SOURCEURL", dataType = StringType, nullable = true)
    )
  )


//Structure data and store dataframe in parquet Format in S3
val data = textRDD.map(_.split("\t")).map(array => convertExportarrayToRow(array))
val dataFrame = spark.createDataFrame(data, dfSchema)
dataFrame.write.format("parquet").mode("overwrite").save("s3a://gdelt-tdenimal/201806.events")

System.exit(0)
