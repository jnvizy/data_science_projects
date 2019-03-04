#!/bin/bash

#Load zip in S3
spark-shell -i batch1_load.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3
#Get zip from S3, structure it and load in S3 as parquet
spark-shell -i batch2_struct.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3
spark-shell -i  batch2_struct_mentions.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3
spark-shell -i  batch2_struct_translatementions.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3
spark-shell -i  batch2_struct_events.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3
spark-shell -i  batch2_struct_translateevents.scala --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3

#Load parquet from S3 and store it in mongodb
spark-shell -i batch4_load.scala  --packages  com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3,org.mongodb.spark:mongo-spark-connector_2.11:2.4.0
