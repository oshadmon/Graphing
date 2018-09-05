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
      Execute query + store results in dict
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
     Based on the results in the table, graph the output
     :args: 
        yaxy:str - y-axy name
        data:dict - data to graph 
        file_name:str - HTML file that stores graph 
     """ 
     yaxy="count" 
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
     Based on the results in the table, graph the output on a horizontal bar graph
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
        ))
     # Layout 
     layout = go.Layout(
        title=self.title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_name)
     # Add query bellow graph
     with open(file_name, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")

def main(): 
   """
   :positional arguments:
      host                  host/port connection to database [127.0.0.1:5432]
      user                  user/password to database [root:passwd]
      dbname                database name [test]
      html_file             File containing output image

   :optional arguments:
      -h,             --help       show this help message and exit
      --title         TITLE        Title of the graph
      --query         QUERY        Select statement to run against (2 values in select max)
      --total-only    TOTAL_ONLY   Graph only the cummulated values
      --daily-only    DAILY_ONLY   Dont graph the cummulated values
   """
   parser = argparse.ArgumentParser()
   parser.add_argument('usr',                  default='root:passwd',         help='user/password to database [root:passwd]') 
   parser.add_argument('hst',                  default='localhost:5432',       help='host/port to database [localhost:5432]')    
   parser.add_argument('db',                   default='test',                help='database name [test]')
   parser.add_argument('query',                default='SELECT * FROM table', help='query to execute') 
   parser.add_argument('-t', '--title',    default='',                    help='graph Name') 
   parser.add_argument('-g', '--graph',    default='line',                help='Type of graph to draw [line | bar | pie]') 
   parser.add_argument('-d',   '--data-dir', default='/var/www/html',       help='Location to store graph [/var/www/html]')
   args = parser.parse_args()

   gg=GenerateGraph(usr=args.usr, hst=args.hst, db=args.db, query=args.query, title=args.title, data_dir=args.data_dir) 
   #gg.draw_line_graph() 
   gg.draw_bar_graph() 

if __name__ == '__main__': 
   main()

