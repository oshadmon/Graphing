import datetime 
import plotly.graph_objs as go
import plotly.offline as off 
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.plotly as py 

class DrawGraphs: 
   def __init__(self): 
      self.data_dir = '/var/www/html/'

   def draw_line_graph(self, file_path:str, title:str, data:dict): 
      """
      Based on the results in the table, draw a line graph 
      :args: 
         yaxy:str - y-axy name
         data:dict - data to graph 
         file_path:str - HTML file that stores graph 
      """ 
      # Generate Trace 
      traces=[]
      for key in range(0, len(data)):
         traces.append(go.Scatter(
            x=data[self.xaxy], 
            y=data[self.yaxy[key-1]]
          )
      )
      print(traces)
      exit(1)
      # Layout 
      layout = go.Layout( 
         title=title,
      )
      print(file_path)
      off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_path)
      """
      # Add query bellow graph
      with open(file_path, 'a') as f: 
         f.write("<body><div><center>"+self.query+"</center></div></body>") 
      """
   '''
   def draw_bar_graph(self): 
     """
     Based on the results in the table, graph the output on a vertical bar graph
     :args: 
        yaxy:str - y-axy 
        data:dict - data to graph 
        file_path:str - HTML file that stores the graph
     """ 
     yaxy='count'
     data=self.generate_data()
     file_path=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), self.title.replace('AND', '').replace('  ', ' ').replace(' ', '_'))
     # Generate Teaces 
     traces=[]
     for key in range(1, len(data)):
        traces.append(go.Bar(
           x=data[self.xaxy], 
           y=data[self.yaxy[key-1]],
           orientation='v'
        )
     )
     # Layout 
     layout = go.Layout(
        title=self.title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_path)
     # Add query bellow graph
     with open(file_path, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")

   def draw_pie_graph(self): 
     """
     Based on the results in the table, graph the output in a pie graph
     ;args;
       yaxy:str - y-axy 
       data:dict - data to graph 
       file_path:str - HTML file that stores the graph
     """
     yaxy='count'
     data=self.generate_data()
     file_path=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), self.title.replace('AND', '').replace('  ', ' ').replace(' ', '_'))
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
     off.plot({'data': [trace], 'layout': layout}, auto_open=True, filename=file_path)
     # Add query bellow graph
     with open(file_path, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")
   ''' 
   def draw(self, graph_type:str, fiile_name:str, title:str, data:dict):
      #file_path = self.data_dir + 'query.png'
      #if file_path != '' and file_path != None :
      #   file_path = self.data_dir + file_namme   

      query_title = title 
      if query_title == '' or query_title == None: 
         query_title = 'Query' 
         
      file_path=self.data_dir+'/%s_%s.html' % (datetime.datetime.now().strftime('%Y_%m_%d'), query_title.replace(' ', '_'))

      self.xaxy = list(data[0])[0] 
      self.yaxy = list(data[0])[1] 

      if graph_type.lower() == 'line': 
         self.draw_line_graph(file_path, query_title, data)

