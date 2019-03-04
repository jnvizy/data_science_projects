import com.mongodb.spark._
import com.mongodb.spark.config._
import org.apache.spark.sql.SparkSession
import org.bson.Document

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



val AWS_ID = "AKIAJNW545DSRAJK6IOQ"
val AWS_KEY = "OrTgAeLFrgL76/+7XFieHC4hoz9gtFZpNx4lCnW/"
val awsClient = new AmazonS3Client(new BasicAWSCredentials(AWS_ID, AWS_KEY))

sc.hadoopConfiguration.set("fs.s3a.access.key", AWS_ID) // mettre votre ID du fichier credentials.csv
sc.hadoopConfiguration.set("fs.s3a.secret.key", AWS_KEY) // mettre votre secret du fichier credentials.csv

val sqlContext = new org.apache.spark.sql.SQLContext(sc)

//Load events
val events = sqlContext.read.parquet("s3a://gdelt-tdenimal/201801.events","s3a://gdelt-tdenimal/201802.events","s3a://gdelt-tdenimal/201803.events","s3a://gdelt-tdenimal/201804.events","s3a://gdelt-tdenimal/201805.events","s3a://gdelt-tdenimal/201806.events","s3a://gdelt-tdenimal/201807.events","s3a://gdelt-tdenimal/201808.events","s3a://gdelt-tdenimal/201809.events","s3a://gdelt-tdenimal/201810.events","s3a://gdelt-tdenimal/201811.events","s3a://gdelt-tdenimal/201812.events")

//Projection
val columnNameevents=Seq("EventId","Day","MonthYear","Year","Actor1Code","Actor1CountryCode", "Actor1Name", "Actor2Code",  "Actor2CountryCode","Actor2Name", "EventCode", "QuadClass", "SOURCEURL","GoldsteinScale","NumMentions","AvgTone","DATEADDED","ActionGeo_Type","ActionGeo_CountryCode","ActionGeo_Long","ActionGeo_Lat","ActionGeo_FeatureID","Actor2Geo_Type","Actor2Geo_Long","Actor2Geo_Lat","Actor2Geo_CountryCode","Actor1Geo_Type","Actor1Geo_CountryCode","Actor1Geo_Lat","Actor1Geo_Long","NumSources")
val events_anglais = events.select(columnNameevents.map(name => col(name)):_*)


//Load translations events
val translations_events = sqlContext.read.parquet("s3a://gdelt-tdenimal/201801.translation.events","s3a://gdelt-tdenimal/201802.translation.events","s3a://gdelt-tdenimal/201803.translation.events","s3a://gdelt-tdenimal/201804.translation.events","s3a://gdelt-tdenimal/201805.translation.events","s3a://gdelt-tdenimal/201806.translation.events","s3a://gdelt-tdenimal/201807.translation.events","s3a://gdelt-tdenimal/201808.translation.events","s3a://gdelt-tdenimal/201809.translation.events","s3a://gdelt-tdenimal/201810.translation.events","s3a://gdelt-tdenimal/201811.translation.events","s3a://gdelt-tdenimal/201812.translation.events")

//Projection
val events_translated= translations_events.select(columnNameevents.map(name => col(name)):_*)

//Union events - translations events
val total_events = events_anglais.union(events_translated)
val total_events_clean=total_events.filter($"Year".geq(lit(2018)))

//Load mentions
val mentions = sqlContext.read.parquet("s3a://gdelt-tdenimal/201801.mentions","s3a://gdelt-tdenimal/201802.mentions","s3a://gdelt-tdenimal/201803.mentions","s3a://gdelt-tdenimal/201804.mentions","s3a://gdelt-tdenimal/201805.mentions","s3a://gdelt-tdenimal/201806.mentions","s3a://gdelt-tdenimal/201807.mentions","s3a://gdelt-tdenimal/201808.mentions","s3a://gdelt-tdenimal/201809.mentions","s3a://gdelt-tdenimal/201810.mentions","s3a://gdelt-tdenimal/201811.mentions","s3a://gdelt-tdenimal/201812.mentions")


//Ajout DocTranslationInfo
val df_old=mentions.withColumn("MentionDocTranslationInfo", lit("eng"))
val df=df_old.withColumnRenamed("GlobalEventID", "EventId")
//Split des Dates
val mentions_anglais_dates= df.withColumn("daymonthmention", dayofmonth(to_date(df("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("monthmention", month(to_date(df("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("yearmention", year(to_date(df("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("daymonthevent", dayofmonth(to_date(df("EventTimeDate"),"MM/dd/yyyy"))).withColumn("monthevent", month(to_date(df("EventTimeDate"),"MM/dd/yyyy"))).withColumn("yearevent", year(to_date(df("EventTimeDate"),"MM/dd/yyyy")))
//Projection
val columnName=Seq("EventId","EventTimeDate","MentionType","MentionTimeDate","MentionType","MentionSourceName","MentionDocTone","MentionDocTranslationInfo","daymonthmention","monthmention","yearmention","daymonthevent","monthevent","yearevent");
val df_mentions_anglais = mentions_anglais_dates.select(columnName.map(name => col(name)):_*)


//Load translation mentions
val translation_mentions_old = sqlContext.read.parquet("s3a://gdelt-tdenimal/201801.translation.mentions","s3a://gdelt-tdenimal/201802.translation.mentions","s3a://gdelt-tdenimal/201803.translation.mentions","s3a://gdelt-tdenimal/201804.translation.mentions","s3a://gdelt-tdenimal/201805.translation.mentions","s3a://gdelt-tdenimal/201806.translation.mentions","s3a://gdelt-tdenimal/201807.translation.mentions","s3a://gdelt-tdenimal/201808.translation.mentions","s3a://gdelt-tdenimal/201809.translation.mentions","s3a://gdelt-tdenimal/201810.translation.mentions","s3a://gdelt-tdenimal/201811.translation.mentions","s3a://gdelt-tdenimal/201812.translation.mentions")
val translation_mentions=translation_mentions_old.withColumnRenamed("GlobalEventID", "EventId")

val dftr_filter=translation_mentions.withColumn("temp", split(col("MentionDocTranslationInfo"), ":")).select(
   col("*") +: (1 until 2).map(i => col("temp").getItem(i).as(s"tranlation")): _*
)
val dftr_filter_drop=dftr_filter.drop("MentionDocTranslationInfo")
val df_translation=dftr_filter_drop.withColumn("temp", split(col("tranlation"), ";")).select(
   col("*") +: (0 until 1).map(i => col("temp").getItem(i).as(s"MentionDocTranslationInfo")): _*
)
//Split des Dates
val df3= df_translation.withColumn("daymonthmention", dayofmonth(to_date(df_translation("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("monthmention", month(to_date(df_translation("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("yearmention", year(to_date(df_translation("MentionTimeDate"),"MM/dd/yyyy"))).withColumn("daymonthevent", dayofmonth(to_date(df_translation("EventTimeDate"),"MM/dd/yyyy"))).withColumn("monthevent", month(to_date(df_translation("EventTimeDate"),"MM/dd/yyyy"))).withColumn("yearevent", year(to_date(df_translation("EventTimeDate"),"MM/dd/yyyy")))
//Projection
val  df_mentions_translation = df3.select(columnName.map(name => col(name)):_*)

//Union mentions - translation mentions
val total_mentions = df_mentions_translation.union(df_mentions_anglais)
val total_mentions_clean=total_mentions.filter(year($"EventTimeDate").geq(lit(2018)))

//make alias
val df_asmentions = total_mentions_clean.as("total_mentions")
val df_asevents = total_events_clean.as("total_events")


//Jointure left join sur event_id
val total_mentions_events=df_asmentions.join(df_asevents,col("total_mentions.EventId")===col("total_events.EventId"),"left")

//articles pos
//articles neg
val df_neg = total_mentions_events.filter("AvgTone < 0").groupBy("Actor1Code","ActionGeo_CountryCode","MentionDocTranslationInfo","monthmention").agg(count(lit(1)).alias("nb_articles_negatifs"))
val df_pos = total_mentions_events.filter("AvgTone > 0").groupBy("Actor1Code","ActionGeo_CountryCode","MentionDocTranslationInfo","monthmention").agg(count(lit(1)).alias("nb_articles_positifs"))


//alias
val df_aspos = df_pos.as("dfpos")
val df_asneg = df_neg.as("dfneg")

val finalDF = df_aspos.join(df_asneg,col("dfpos.Actor1Code") === col ("dfneg.Actor1Code") && col("dfpos.ActionGeo_CountryCode") === col("dfneg.ActionGeo_CountryCode") && col("dfpos.MentionDocTranslationInfo")===col("dfneg.MentionDocTranslationInfo") && col("dfpos.monthmention")===col("dfneg.monthmention"),"inner").select(col("dfpos.ActionGeo_CountryCode"),col("dfpos.MentionDocTranslationInfo"),col("dfpos.Actor1Code"),col("dfpos.monthmention"),col("nb_articles_negatifs"),col("nb_articles_positifs"))


MongoSpark.save(finalDF.write.option("spark.mongodb.output.uri", "mongodb://master:27020/gdelt.query3").mode("overwrite"))

//System.exit(0)
