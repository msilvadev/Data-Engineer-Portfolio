<h1 align="center">Data Warehouse</h1>

[![author](https://img.shields.io/badge/author-Matheus-red.svg)](https://www.linkedin.com/in/msilvadev/) 
![](https://img.shields.io/badge/Technology-Python-blue.svg)
![](https://img.shields.io/badge/Database-Redshift-blue.svg)
![](https://img.shields.io/badge/Bucket-S3-yellow.svg)

<h2 align="center">Summary</h2>

A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to. You'll be able to test your database and ETL pipeline by running queries given to you by the analytics team from Sparkify and compare your results with their expected results.

<h2 align="center">Role performed</h2>

I played the role of Data Engineer where I could apply what I've learned on data warehouses and AWS to build an ETL pipeline for a database hosted on Redshift. To complete the project, I needed to load data from S3 to staging tables on Redshift and execute SQL statements that create the analytics tables from these staging tables.

<h2 align="center">Detailing files from project</h2>

### [create_cluster](create_cluster.py)
Is where create a cluster Redshift.

### [create_tables](create_tables.py)
Is where create fact and dimension tables for the star schema in Redshift.

### [etl](etl.py)
Is where load data from S3 into staging tables on Redshift and then process that data into your analytics tables on Redshift.

### [sql_queries](sql_queries.py)
Is where you'll define you SQL statements, which will be imported into the two other files above.

### [dwh](dwh.cfg)
Properties file where we out credential to connect with cluster of Redshift and path to bucket S3. We have the following properties:

```
[CLUSTER]
HOST=''
DB_NAME=''
DB_USER=''
DB_PASSWORD=''
DB_PORT=5439

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'

[DWH]
DWH_CLUSTER_TYPE       = multi-node
DWH_NUM_NODES          = 4
DWH_NODE_TYPE          = dc2.large
DWH_CLUSTER_IDENTIFIER = 'redshift-cluster-1'
DWH_DB                 = ''
DWH_DB_USER            = ''
DWH_DB_PASSWORD        = ''
DWH_PORT               = 5439
DWH_IAM_ROLE_NAME      = ''

```

<h2 align="center">Running</h2>

Required to have **Python 3** on the running machine. If you need to install it, you can download [here](https://www.python.org/downloads/).

To run this project you will need to fill the information in [dwh.cfg](dwh.cfg) file in the project root folder.

Now follow steps:

1. Create Cluster Redshit
    Execute the create_cluster script to set up the needed infrastructure for this project.
    ```
      python create_cluster.py
    ```
    
2. Create tables (star schema)
    Execute the create_tables script to set up the database staging and analytical tables
    ```
      python create_tables.py
    ```
    
3. ETL Process
    Execute the etl script to extract data from the files in S3, stage it in redshift, and finally store it in the dimensional tables
    ```
      python etl.py
    ```