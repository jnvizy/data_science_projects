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

//awsClient.putObject("denimal-thomas-telecom-gdelt2018", "masterfilelist.txt", new File( "/home/ec2-user/masterfilelist2018120111.txt") )
awsClient.putObject("gdelt-tdenimal", "masterfilelist.txt", new File( "/home/ec2-user/masterfilelist2018.txt") )



import org.apache.spark.sql.SQLContext

val sqlContext = new SQLContext(sc)
val filesDF = sqlContext.read.
                    option("delimiter"," ").
                    option("infer_schema","true").
                    csv("s3a://gdelt-tdenimal/masterfilelist.txt").
                    withColumnRenamed("_c0","size").
                    withColumnRenamed("_c1","hash").
                    withColumnRenamed("_c2","url").
                    cache

val sampleDF = filesDF.filter(col("url").contains("export.CSV")).cache

object AwsClient{
    val s3 = new AmazonS3Client(new BasicAWSCredentials(AWS_ID, AWS_KEY))
}


def fileDownloader(urlOfFileToDownload: String, fileName: String) = {
    val url = new URL(urlOfFileToDownload)
    val connection = url.openConnection().asInstanceOf[HttpURLConnection]
    connection.setConnectTimeout(5000)
    connection.setReadTimeout(5000)
    connection.connect()

    if (connection.getResponseCode >= 400)
        println("error")
    else
        url #> new File(fileName) !!
}




sampleDF.select("url").repartition(100).foreach( r=> {
            val URL = r.getAs[String](0)
            val fileName = r.getAs[String](0).split("/").last
            val dir = "/tmp/"
            val localFileName = dir + fileName
            fileDownloader(URL,  localFileName)
            val localFile = new File(localFileName)
            AwsClient.s3.putObject("gdelt-tdenimal", fileName, localFile )
            localFile.delete()
            
})


System.exit(0)
