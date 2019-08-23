import datetime
import decimal
import psycopg2

class DBMS: 
   def __init__(self, usr:str='root:passwd', hst:str='localhost:54321', db:str='test'):
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
   
   def __create_connection(self, usr:str='root:passwd', hst:str='localhost:54321', db:str='test')->psycopg2.extensions.cursor: 
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

   def __unify_data_types(self, value):

      if isinstance(value, str):
         new_value = value.replace("\\","\\\\")
      elif isinstance(value, decimal.Decimal):
         new_value = float(value)
      elif isinstance(value, datetime.datetime):
         new_value = value.strftime('%Y-%m-%d %H:%M:%S.%s')
      elif isinstance(value, datetime.datetime):
         new_value = value.strftime('%Y-%m-%d %H:%M:%S.%s')
      elif isinstance(value, datetime.time):
         new_value = value.strftime('%H:%M:%S.%s')
      elif isinstance(value, datetime.date):
         new_value = value.strftime('%Y-%m-%d')
      else:
         new_value = value

      return new_value
   def __format_db_rows(self, db_cursor, output_prefix, rows_data):
      data = "{\"" + output_prefix + "\":[{"
      formatted_row = ""
      first_row = True
      for row in rows_data:
         if not first_row:
            formatted_row = ",{"
         for i, value in enumerate(row):
            new_value = self.__unify_data_types(value)
            if output_prefix == "Query":
               description = str(i)    # this makes column names smaller + avoids non-unique names
            else:
               description = db_cursor.description[i][0]

            if new_value == None:
               formatted_row += "\"" + description+ "\":" + "\"\""
            else:
               formatted_row += "\"" + description + "\":\"" + str(new_value) + "\""

            data += formatted_row
            formatted_row = ","
         first_row = False
         data += "}"
      data += "]}"

      return data


   def __execute_sql_stmt(self, sql_stmt:str):
      """
      Execute a SQL stmt as a statement
      :args:
         sql_stmt:sql - SQL stmt
      """
      ret_val = True

      try:
         self.cur.execute(sql_stmt)
      except psycopg2.DataError as e:
         print("Error executing SQL: %s \n%s" + str(e) + sql_stmt)
         ret_val = False
      except psycopg2.InternalError as e:
         print("Error executing SQL: %s \n%s" + str(e) + sql_stmt)
         ret_val = False
      except psycopg2.IntegrityError as e:
         print("Error executing SQL: %s \n%s" + str(e) + sql_stmt)
         ret_val = False
      except psycopg2.OperationalError as e:
         print("Error executing SQL: %s \n%s" + str(e) + sql_stmt)
         ret_val = False
      except psycopg2.NotSupportedError as e:
         print("Error executing SQL: %s \n%s"+ str(e) + sql_stmt)
         ret_val = False
      except psycopg2.ProgrammingError as e:
         print("Error executing SQL: %s \n%s" + str(e) + sql_stmt)
         ret_val = False
      except (Exception, psycopg2.Error) as e:
         print("Error executing SQL: %s" + str(e))
         ret_val = False
      except:
         print("Error executing SQL: Unknown error \n%s" + sql_stmt)
         ret_val = False

      return ret_val

   def __fetch_rows(self, output_prefix:str, fetch_size:int):
      """
      Fetch N number of rows at a time
      :args:
         fetch_size:int - Number of rows per fetch
      :return:
         if succss return True, else return False
      """

      ret_val = True
      try:
         if fetch_size:
            output = self.cur.fetchmany(fetch_size)  # fetchmany is a list object
         else:
            output = self.cur.fetchall()

      except psycopg2.DataError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except psycopg2.InternalError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except psycopg2.IntegrityError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except psycopg2.OperationalError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except psycopg2.NotSupportedError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except psycopg2.ProgrammingError as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except (Exception, psycopg2.Error) as e:
         print("Unable to fetch query results: %s" + str(e))
         ret_val = False
      except:
         print("Unable to fetch query results: Unknown error")
         ret_val = False


      if ret_val and len(output):
         string_data = self.__format_db_rows( self.cur, output_prefix, output)
      else:
         string_data = None
      return [ret_val, string_data]

   def execute_select_all(self, sql_stmt:str)->list:
      if self.__execute_sql_stmt(sql_stmt):
         ret_val, string_data = self.__fetch_rows('output', 0) # 0 is fetchall()
      else:
         ret_val = False
         string_data = None
      return [ret_val, string_data]
