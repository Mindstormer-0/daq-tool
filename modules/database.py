import os
import sqlite3
import pandas as pd

def ini_database():
  os.makedirs('./data', exist_ok=True)
  path = os.path.abspath('./data/database.db')
  print(path)
  sqlite3.connect(path)

class dbhelper:
  global db
  db = './data/database.db'

  def run_query(q):
      with sqlite3.connect(db) as conn:
          return pd.read_sql(q,conn)
      
  def run_command(c):
      with sqlite3.connect(db) as conn:
          conn.isolation_level = None
          conn.execute(c) 
          
  def show_tables(self):
      q = '''
          SELECT
              name
          FROM sqlite_master
          WHERE type IN ("table","view");
          '''
      return self.run_query(q)

  def get_table_row_count(self,tablename):
      q = '''
          SELECT
              COUNT(1)
          FROM %s;
          ''' % tablename
      return self.run_query(q)["COUNT(1)"][0]

  def get_tables(self):
      tables = self.show_tables()
      tables["row_count"] = [self.get_table_row_count(t) for t in tables["name"]]