#Data engineering project

###Background
Showing if there is a correlation between house prices of an area 
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
