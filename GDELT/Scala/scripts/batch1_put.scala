import sys.process._
import java.net.URL
import java.io.File
import java.io.File
import java.nio.file.{Files, StandardCopyOption}
import java.net.HttpURLConnection 
import org.apache.spark.sql.functions._

import com.amazonaws.services.s3.AmazonS3Client
import com.amazonaws.auth.BasicAWSCredentials
    
val AWS_ID = "AKIAJNW545DSRAJK6IOQ"
val AWS_KEY = "OrTgAeLFrgL76/+7XFieHC4hoz9gtFZpNx4lCnW/"
val awsClient = new AmazonS3Client(new BasicAWSCredentials(AWS_ID, AWS_KEY))

sc.hadoopConfiguration.set("fs.s3a.access.key", AWS_ID) // mettre votre ID du fichier credentials.csv
sc.hadoopConfiguration.set("fs.s3a.secret.key", AWS_KEY) // mettre votre secret du fichier credentials.csv

awsClient.putObject("gdelt-tdenimal", "201802.translation.mentions.CSV.zip", new File( "/data/spark/201802.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201803.translation.mentions.CSV.zip", new File( "/data/spark/201803.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201804.translation.mentions.CSV.zip", new File( "/data/spark/201804.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201805.translation.mentions.CSV.zip", new File( "/data/spark/201805.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201806.translation.mentions.CSV.zip", new File( "/data/spark/201806.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201807.translation.mentions.CSV.zip", new File( "/data/spark/201807.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201808.translation.mentions.CSV.zip", new File( "/data/spark/201808.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201809.translation.mentions.CSV.zip", new File( "/data/spark/201809.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201810.translation.mentions.CSV.zip", new File( "/data/spark/201810.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201811.translation.mentions.CSV.zip", new File( "/data/spark/201811.translation.mentions.CSV.zip") )
awsClient.putObject("gdelt-tdenimal", "201812.translation.mentions.CSV.zip", new File( "/data/spark/201812.translation.mentions.CSV.zip") )
//awsClient.putObject("gdelt-tdenimal", "201801.translation.mentions.CSV.zip", new File( "/data/spark/201801.translation.mentions.CSV.zip") )
//awsClient.putObject("gdelt-tdenimal", "201801.translation.translation.mentions.CSV.zip", new File( "/data/spark/201801.translation.translation.mentions.CSV.zip") )
//awsClient.putObject("gdelt-tdenimal", "201801.translation.translation.mentions.CSV.zip", new File( "/data/spark/201801.translation.translation.mentions.CSV.zip") )

System.exit(0)
