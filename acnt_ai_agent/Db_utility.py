import psycopg2
from psycopg2 import sql
import pandas as pd
from pandas import DataFrame
from datetime import datetime
from configparser import ConfigParser
import json

class Db_utility:
    def __init__(self,env):
        self.env = env

    def connect(self):
        global conn
        config = ConfigParser()
        config.read('..\\conf\\db_conf.ini')
        env=config.get('Environment','env')
        if env == 'nonprod':
            schemaname=config.get('Database','schema_name_np')
            host=config.get('Database','host_np')
            port=config.get('Database','port_np')
            database=config.get('Database','database_np')
            user=config.get('Database','user_np')
            password=config.get('Database','password_np')

            conn=psycopg2.connect(host=host,port=port,database=database,user=user,password=password)
        return conn

    def get_acc_details(self,name):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('select acc_number,acc_type from ai_schema.accounts_master where acc_holder_name=%s',(name,))
        recs= cursor.fetchall()
        cursor.close()
        return recs

    def get_acc_balance(self,acc_number):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute('select balance from ai_schema.accounts_master where acc_number=%s',(acc_number,))
        recs = cursor.fetchall()
        cursor.close()
        return recs





