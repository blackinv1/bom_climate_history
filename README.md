# AAC - Climate History
## Overview
This repo contains code that ingests the provided data into a ElasticSearch cluster
* Read documents from files
* Define the ElasticSearch data schema
* Map the documents into the defined schema
* Load the documents into the ElasticSearch cluster

## Requirments


## Config
1. `ElasticSearch Cluster credentials`
- create a `creds.json` file in the `config/` follder, and put the `cloud_id`, `username` and `password` in it

1. `BOM Data Folder`
- create a `data` folder in the root dir of this repo, then extracts the BOM downloads at here
- BOM Data Download: ftp://ftp2.bom.gov.au/anon/gen/clim_data/IDCKWCDEA0.tgz

### Setup
1. Prerequisites
```
Shell - Bash or alternatives
Python3.7 or above
```

1. Create and Python virtual env and activate it
```
> python3 -m venv env
> source env/bin/activate
```

1. Upgrade PIP, then install the relevant packages into the virtual env
```
> pip3 install -r requirements.txt --upgrade pip
```

## Run the application!
```
> ./src/main.py
```

