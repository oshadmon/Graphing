import datetime 
import plotly.graph_objs as go
import plotly.offline as off 
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.plotly as py 

class DrawGraphs: 
   def __init__(self): 
      self.data_dir = '/var/www/html/'

   def __convert_timestamp(self, value:str): 
      if "." in value: 
         new_timestamp = value.replace(value.split(".")[-1], value.split(".")[-1][:6])
         try: 
            return datetime.datetime.strptime(new_timestamp, '%Y-%m-%d %H:%M:%S.%f')
         except:
            return value 
      else:
         new_timestamp = value.replace(value.split(".")[-1], value.split(".")[-1][:6])
         try:
            return datetime.datetime.strptime(new_timestamp, '%Y-%m-%d %H:%M:%S.%f')
         except:         
            return value   

   def __data_breakdown_line(self, data:list)->list:
      traces=[]
      xaxy = list(data[0])[0]
      xvalues = [] 
      yaxy = list(data[0])[1:]
      yvalues = {} 

      for row in data:
         xvalues.append(self.__convert_timestamp(row[xaxy]))
         for key in yaxy: 
            if key not in yvalues: 
               yvalues[key] = [] 
            yvalues[key].append(self.__convert_timestamp(row[key]))

      for key in yaxy: 
         traces.append(
            go.Scatter(
               x = xvalues,
               y = yvalues[key]
            )
         )
      return traces 

   def draw_line_graph(self, file_path:str, title:str, traces:list):
      """
      Based on the results in the table, draw a line graph 
      :args: 
         yaxy:str - y-axy name
         data:dict - data to graph 
         file_path:str - HTML file that stores graph 
      """ 
      # Layout 
      layout = go.Layout( 
         title=title,
      )
      off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_path)
      """
      # Add query bellow graph
      with open(file_path, 'a') as f: 
         f.write("<body><div><center>"+self.query+"</center></div></body>") 
      """
      
   def __data_breakdown_bar(self, data:list)->list:
      traces=[]
      xaxy = list(data[0])[0]
      xvalues = []
      yaxy = list(data[0])[1:]
      yvalues = {}

      for row in data:
         xvalues.append(self.__convert_timestamp(row[xaxy]))
         for key in yaxy:
            if key not in yvalues:
               yvalues[key] = []
            yvalues[key].append(self.__convert_timestamp(row[key]))

      for key in yaxy:
         traces.append(
            go.Bar(
               x = xvalues,
               y = yvalues[key]
            )
         )
      return traces

   def draw_bar_graph(self, file_path:str, title:str, traces:list): 
     """
     Based on the results in the table, graph the output on a vertical bar graph
     :args: 
        yaxy:str - y-axy 
        data:dict - data to graph 
        file_path:str - HTML file that stores the graph
     """ 
     # Layout 
     layout = go.Layout(
        title=title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_path)
     """
     # Add query bellow graph
     with open(file_path, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")
     """

   def __data_breakdown_pie(self, data:list)->list:
      traces=[]
      xaxy = list(data[0])[0]
      xvalues = []
      yaxy = list(data[0])[1]
      yvalues = []

      for row in data:
         xvalues.append(self.__convert_timestamp(row[xaxy]))
         yvalues.append(self.__convert_timestamp(row[yaxy]))
      print(xvalues)
      print(yvalues)
      print(go.Pie(
            lables = xvalues,
            values = yvalues
         )
      )
      return traces   

   def draw_pie_graph(self, file_path:str, title:str, traces:list): 
     """
     Based on the results in the table, graph the output in a pie graph
     ;args;
       yaxy:str - y-axy 
       data:dict - data to graph 
       file_path:str - HTML file that stores the graph
     """
     # Layout 
     layout = go.Layout(
        title=title,
     )
     off.plot({'data': traces, 'layout': layout}, auto_open=True, filename=file_path)
     """
     # Add query bellow graph
     with open(file_path, 'a') as f:
        f.write("<body><div><center>"+self.query+"</center></div></body>")
     """

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
         traces = self.__data_breakdown_line(data)
         self.draw_line_graph(file_path, query_title, traces)
      if graph_type.lower() == 'bar': 
         traces = self.__data_breakdown_bar(data)
         self.draw_bar_graph(file_path, query_title, traces) 
      elif graph_type.lower() == 'pie': 
         traces = self.__data_breakdown_pie(data)
         print(traces)
         self.draw_pie_graph(file_path, query_title, traces)
