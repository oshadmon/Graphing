import argparse
import json 

import connect_dbms 
import draw 

def str_to_json(data:str):
   try:
      json_object = json.loads(data)
   except ValueError as error:
      json_object = None
   return  json_object

def main(): 
   """
   Main
   :positional arguments:
      usr                   user/password to database [root:passwd]
      hst                   host/port to database [localhost:5432]
      db                    database name [test]
      query                 query to execute
   :optional arguments:
      -h, --help            show this help message and exit
      -t, --title           graph Name
      -g, --graph           Type of graph to draw [line | bar | pie]
      -d, --data-dir        location to store graph [/var/www/html]
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('usr',                  default='root:passwd',         help='user/password to database [root:passwd]') 
   parser.add_argument('hst',                  default='localhost:5432',       help='host/port to database [localhost:5432]')    
   parser.add_argument('db',                   default='test',                help='database name [test]')
   parser.add_argument('query',                default='SELECT * FROM table', help='query to execute') 
   #parser.add_argument('-t', '--title',        default='',                    help='graph Name') 
   #parser.add_argument('-g', '--graph',        default='line',                help='Type of graph to draw [line | bar | pie]') 
   #parser.add_argument('-d',   '--data-dir',   default='/var/www/html',       help='Location to store graph [/var/www/html]')
   args = parser.parse_args()

   dbms = connect_dbms.DBMS(args.usr, args.hst, args.db)
   drw = draw.DrawGraphs() 

   results = dbms.execute_select_all(args.query)
   dict_results = str_to_json(results[1])

   for key in  dict_results: 
      drw.draw('line', 'query.html', '', dict_results[key])

if __name__ == '__main__': 
   main()

