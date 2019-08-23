import argparse
import datetime 
import os
import plotly.graph_objs as go
import plotly.offline as off 
import plotly.plotly as py
import psycopg2
import sys 

from plotly.graph_objs import *
import plotly.plotly as py 

class GenerateGraph: 
   def __init__(self, usr:str='root:passwd', hst:str='localhost:54321', db:str='test', query:str='SELECT * FROM table',
                title:str='', data_dir:str='/var/www/html'):
      """
      Generate graphs based on the results in database 
      :param: 
         self.cur:psycopg2.extensions.cursor - connection to database 
            usr:str - database user & passwd 
            hst:str - database host & port
            db:str  - database name
         self.query:str - query to get data 
         self.title:str - graph title
         self.data_dir:str - dir to store graph
         self.xaxy:str  - x-axy of graph (this is set to the first column in SELECT)
         self,yaxy:list - y-axy of graph (this is all columns SELECT execept the first one)  
      """
      self.cur = self.__create_connection(usr, hst, db) 
      self.query=query 
      self.data_dir=data_dir
      self.xaxy=query.lower().split('select ')[1].split(',')[0]
      self.yaxy=query.lower().split('%s,' % self.xaxy)[-1].split('from')[0].replace(' ','').split(',')
      self.title=title
      if self.title == '':
         self.title+=self.xaxy+' VS'
         for i in range(len(self.yaxy)):
            if i != 0: 
               self.title+=' AND '+self.yaxy[i]
            else: 
               self.title+=' '+self.yaxy[i]
   
   def __create_connection(self, usr:str='root:passwd', 
                           hst:str='localhost:54321', db:str='test')->psycopg2.extensions.cursor: 
      """
      Create connection
      :param:
         usr:str - user & passwd to connect to database 
         hst:str - host & port to connection to databse
         db:str  - database name
      :return: 
         connection to database 
      """
      conn=psycopg2.connect(host=hst.split(':')[0], port=int(hst.split(':')[1]), user=usr.split(':')[0], password=usr.split(':')[1], dbname=db) 
      conn.autocommit=True
      return conn.cursor()

   def generate_data(self)->dict: 
      """
      Execute query & store results in dict
      :sample: 
         Given the query - 'SELECT timestamp, SUM(col1) FROM table GROUP BY timestamp ORDER BY timestamp'; the results stored in 
         a dict object, with each column being used a key.  When needed to graph, the first column in the query is used the x-axy,
         while all other columns are used for graphing. In the query shown: timestamp would be the x-axy while SUM(col1) would be the  
         values graphed (ie Y-AXY values). 
      :return: 
         dictionary of results
      """
      results={self.xaxy:[]}
      for i in self.yaxy: 
         results[i]=[]
      self.cur.execute(self.query)
      data=self.cur.fetchall()
      for d in data: 
         for i in range(len(d)):
            if i == 0: 
               results[self.xaxy].append(d[i])
            else: 
               results[self.yaxy[i-1]].append(d[i])
      return results

   def draw_line_graph(self): 
     """
     Based on the results in the table, draw a line graph 
     :args: 
        yaxy:str - y-axy name
        data:dict - data to graph 
        file_name:str - HTML file that stores graph 
     """ 
     data=self.generate_data() 
     file_name=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), self.title.replace('AND', '').replace('  ', ' ').replace(' ', '_'))
     # Generate Trace 
     traces=[]
     for key in range(1, len(data)):
        traces.append(go.Scatter(
           x=data[self.xaxy], 
           y=data[self.yaxy[key-1]]
         )
     )
     print(traces) 
     # Layout 
     layout = go.Layout( 
           title=self.title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_name)

     # Add query bellow graph
     with open(file_name, 'a') as f: 
        f.write("<body><div><center>"+self.query+"</center></div></body>") 

   def draw_bar_graph(self): 
     """
     Based on the results in the table, graph the output on a vertical bar graph
     :args: 
        yaxy:str - y-axy 
        data:dict - data to graph 
        file_name:str - HTML file that stores the graph
     """ 
     yaxy='count'
     data=self.generate_data()
     file_name=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), self.title.replace('AND', '').replace('  ', ' ').replace(' ', '_'))
     # Generate Teaces 
     traces=[]
     for key in range(1, len(data)):
        traces.append(go.Bar(
           x=data[self.xaxy], 
           y=data[self.yaxy[key-1]],
           orientation='v'
        )
     )
     print(traces)
     exit(1)
     # Layout 
     layout = go.Layout(
        title=self.title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_name)
     # Add query bellow graph
     with open(file_name, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")

   def draw_pie_graph(self): 
     """
     Based on the results in the table, graph the output in a pie graph
     ;args;
       yaxy:str - y-axy 
       data:dict - data to graph 
       file_name:str - HTML file that stores the graph
     """
     yaxy='count'
     data=self.generate_data()
     file_name=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), self.title.replace('AND', '').replace('  ', ' ').replace(' ', '_'))
     # Generate Teaces 
     values=''
     for key in list(data.keys()):
        if key != self.xaxy: 
           values=key 
     trace=go.Pie(
        labels=data[self.xaxy],
        values=data[values]
     )
     # Layout 
     layout = go.Layout(
        title=self.title,
     )
     off.plot({'data': [trace], 'layout': layout}, auto_open=True, filename=file_name)
     # Add query bellow graph
     with open(file_name, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")


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
   parser.add_argument('-t', '--title',        default='',                    help='graph Name') 
   parser.add_argument('-g', '--graph',        default='line',                help='Type of graph to draw [line | bar | pie]') 
   parser.add_argument('-d',   '--data-dir',   default='/var/www/html',       help='Location to store graph [/var/www/html]')
   args = parser.parse_args()

   gg=GenerateGraph(usr=args.usr, hst=args.hst, db=args.db, query=args.query, title=args.title, data_dir=args.data_dir) 

   if args.graph.lower() == 'line': 
      gg.draw_line_graph() 
   if args.graph.lower() == 'bar': 
      gg.draw_bar_graph() 
   if args.graph.lower() == 'pie':
      gg.draw_pie_graph()

if __name__ == '__main__': 
   main()

