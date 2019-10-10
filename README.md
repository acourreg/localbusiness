# localbusiness
The purpose of this Udacity project is to gather small and mid size businesses data

So it can help entrepreneurs to explore some business opportunities in the town and sector they like, thanks to some metrics.

Credits for used datasets are in credits.txt

## Quicklaunch

you can clone this project, then launch the server (if you have pyspark installed localy)
Source datasets are not included for no issue with license, but output data is here for server to function.

```
git clone https://github.com/acourreg/localbusiness.git
cd localbusiness
python server.py
```

If you are interested only in data-pipeline part, you can launch the jupyter notebook with command below (but you will need to download each dataset, for it to work)
```
jupyter notebook
```

![image](https://github.com/acourreg/localbusiness/blob/master/screenshot.png?raw=true)


! Some functionalities on the app are for demo purpose - not fully implemented
(the main work was on data processing)

## Udacity project Answers part ----

> What's the goal? What queries will you want to run? How would Spark or Airflow be incorporated? Why did you choose the model you chose?

The goal is to help entrepreneurs to become, with local business economic metrics. Those can be grouped by states / cities / sector of activity.

Spark was incorporated as the tool came pretty handly at manipulating multiple csv formats quickly. It also allowed to save results 
and retrieve
results

> Document the steps of the process.

The data which have been evaluated, and the final data model are documented in repo-pdf. 50+ datasets have been visited in total for this project,
15 evaluated deeply, and finally 6 kept for this project.

The steps were those (can be found in the Jupyter notebook attached):

1- Download (manually) the csv/ excels, and export it all as csv format
2- Load all the datasets into respective stream variables
3- Transform this stream in dimension spark-Sql tables (sector/states/cities/companies) -  in 3rd normal form
4- export these tables under parquet format

A nextflow for the server is following:

1- retrieve previously saved parquet tables
2- Analyse Http request with given states and sector researched
3- display some analytics results for these params


> Propose how often the data should be updated and why.

The data need to be updated only once a year, so no need heavy orchestrator like Airflow for now.
1 year since most financial results are updated every year, and some are anyway late from 3 years (as these data are hard to find).
The best approach at this moment is still to manually find new datasets to complete existing ones.

> Include a description of how you would approach the problem differently under the following scenarios:

> If the data was increased by 100x.

First I wouldnt save it to parquet files, but rather use an SQL or cassandra DB instead. Using spark as backend here is good as 
a quickwin solution, but not recommendable for production usage. Also spark would still be Ok to be used in this context. The only difference
would be dataset not to be downloaded, but loaded remotely by spark.

> If the pipelines were run on a daily basis by 7am.

There would be any use for this at the moment, but in this case maybe a simple cron over airflow should be enough. Since the computational
steps arent that complex or risky.

> If the database needed to be accessed by 100+ people.

In this case an SQL / CQL DB would be mandatory, but we could still use the same server (modified)