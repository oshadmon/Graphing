# Graphing

The following code takes a given query and generates a graph from it. In a given query, the first column is used as the x-axy, while all others will be the values graphed. 

Example: In the following query, ``SELECT timestamp, SUM(total) FROM table_name GROUP BY timestamp;```. ```timestamp``` is the X-AXY and ```SUM(total)``` are the values being graphed.

# Files & Sample Code

```graph.py``` - Script that allows to generate a graph either as line, bar, or pie 
```
ubuntu@ori-foglamp:~/Graphing$ python3 graph.py --help
usage: graph.py [-h] [-t TITLE] [-g GRAPH] [-d DATA_DIR] usr hst db query

positional arguments:
  usr                   user/password to database [root:passwd]
  hst                   host/port to database [localhost:5432]
  db                    database name [test]
  query                 query to execute

optional arguments:
  -h, --help            show this help message and exit
  -t TITLE, --title TITLE
                        graph Name
  -g GRAPH, --graph GRAPH
                        Type of graph to draw [line | bar | pie]
  -d DATA_DIR, --data-dir DATA_DIR
                        Location to store graph [/var/www/html]

```

```ubuntu@ori-foglamp:~/Graphing$ python3 graph.py ubuntu:foglamp 127.0.0.1:5432 github 'SELECT timestamp, SUM(today), SUM (total) FROM github_traffic GROUP BY timestamp ORDER BY timestamp;' -t 'GitHub Traffic over Time' -g line -d /var/www/html/github_graphs/``` 
![Alt text](https://github.com/oshadmon/Graphing/blob/master/imgs/2018_09_05_GitHub_Traffic_over_Time.png)


```ubuntu@ori-foglamp:~/Graphing$ python3 graph.py ubuntu:foglamp 127.0.0.1:5432 github 'SELECT referral, MAX(total) FROM github_referrals GROUP BY referral ORDER BY SUM(today) ASC;' -t 'GitHub Referrals Today' -g bar -d /var/www/html/github_graphs```
![Alt text](https://github.com/oshadmon/Graphing/blob/master/imgs/2018_09_05_GitHub_Referrals_Today.png)


```ubuntu@ori-foglamp:~/Graphing$ python3 graph.py ubuntu:foglamp 127.0.0.1:5432 github 'SELECT referral, MAX(total) FROM github_referrals GROUP BY referral ORDER BY SUM(today) ASC;' -t 'GitHub Referrals Overall' -g pie -d /var/www/html/github_graphs```
![Alt text](https://github.com/oshadmon/Graphing/blob/master/imgs/2018_09_05_GitHub_Referrals_Overall.png)

```sample.html``` - HTML file containing sample graphs. User must download file and open in browser in order to view it
