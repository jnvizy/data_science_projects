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
val dataFrame = sqlContext.read.parquet("s3a://gdelt-tdenimal/201801.mentions")
MongoSpark.save(dataFrame.write.option("spark.mongodb.output.uri", "mongodb://master:27017/tdenimal.mentions").mode("append"))

System.exit(0)
