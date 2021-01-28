# Property and Crime - DE

### Background
Showing the relationship between house prices of an area 
and its crime-rate. 

Data is specific to London Boroughs. 

Also uses PropertyScraper repository for scraping prices of property
in specific areas of interest.

### Deploying

Environment variables file will be needed for postgres communication which will
be of the following form:

```sh
POSTGRES_DATABASE=""
POSTGRES_USER=""
POSTGRES_HOST=""
POSTGRES_PORT=""
```

A cluster was created on AWS EMR to run the pyspark job. An EC2 key 
pair .pem file needs to be downloaded to ssh into the cluster after editing the 
inbound rules of the master node. \
Once in EMR, a job can be run by copying the python file into the cluster directory
and using the command:

```python
spark-submit spark_batch.py
```

