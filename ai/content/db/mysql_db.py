import sys
import os
DIR = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.dirname(DIR)
DIR = os.path.dirname(DIR)
sys.path.append(DIR)
import pandas as pd
import pymysql
from content.configs.global_configs import MysqlConfigs as mc

class MYSQL():

    def __init__(self,db):
        self.conn = pymysql.connect(host=mc.host,
                                    port=int(mc.port),
                                    user=mc.user,
                                    password=mc.pwd,
                                    db=db)
        self.curr = self.conn.cursor()


    @staticmethod
    def generateSql(table_name, columns, whereCauses=None):
        sql = "SELECT "
        count=0
        for c in columns:
            if count!=0:
                sql+=','
            sql+=c
            sql+=' '
            count+=1
        sql += "FROM "
        sql += table_name
        if whereCauses:
            sql += " where "
            count = 0
            for wc in whereCauses:
                if count!=0:
                    sql += ' and '
                sql += wc[0]
                if type(wc[1])==int:
                    sql += '='
                    sql += str(wc[1])
                elif not wc[1].startswith('in'):
                    sql += '='
                    sql += '\'{}\''.format(wc[1])
                else:
                    sql += ' '
                    sql += wc[1]
                count+=1
        return sql

    @staticmethod
    def generate_update_sql_and_data(field_name,field_value,table_name:str,params:dict):
        data = []
        sql = "update `{}` set ".format(table_name)
        for key in params:
            if key == field_name:continue
            sql += '`{}`=%s ,'.format(key)
            data.append(params[key])
        sql = sql[:-1]
        sql += ' where `{}` = "{}"'.format(field_name,field_value)
        return sql,data

    @staticmethod
    def generate_insert_sql_and_data(table_name:str,params:dict):
        data = []
        sql_start = "INSERT INTO `{}` ( ".format(table_name)
        value_str = "VALUES ( "
        for key in params:
            sql_start += '`{}`'.format(key)
            sql_start += ','
            value_str += '%s'
            value_str += ','
            data.append(params[key])
        sql_start = sql_start[:-1] + ') '
        value_str = value_str[:-1] + ')'
        sql = sql_start + value_str
        return sql,data

    @staticmethod
    def generate_insert_sql_and_data_batch(table_name:str,batch_params:list):
        datas = []
        sql_start = "INSERT INTO `{}` ( ".format(table_name)
        value_str = "VALUES ( "
        order_key = []
        for key in batch_params[0]:
            sql_start += '`{}`'.format(key)
            sql_start += ','
            value_str += '%s'
            value_str += ','
            order_key.append(key)
        sql_start = sql_start[:-1] + ') '
        value_str = value_str[:-1] + ')'
        sql = sql_start + value_str
        for p in batch_params:
            datas.append([p[key] for key in order_key])
        return sql,datas

    def search(self,sql):
        a =  self.curr.execute(sql)
        data = self.curr.fetchall()
        return data

    def execute(self,sql_template,data):
        self.curr.execute(sql_template,data)
        self.conn.commit()

    def insert(self,sql_template, data):
        self.curr.execute(sql_template, data)
        self.conn.commit()

    def insert_batch(self,sql_template,data):
        try:
            self.curr.executemany(sql_template, data)
        except pymysql.Error as e:
            print(e)
            self.conn.rollback()
            self.conn.close()
        self.conn.commit()


    def close(self):
        self.conn.close()
        self.curr.close()


class PandasDB():

    def __init__(self,db):
        self.mysql = MYSQL(db)

    def read_sql(self,sql):
        return pd.read_sql(sql,self.mysql.conn)

    def close(self):
        self.mysql.close()

if __name__ == '__main__':
    mysql = MYSQL()
    #sql = "INSERT INTO `polygon_lens_hot_words_score` (`profileid`,`pubid`,`word`,`count`,`rank`,`type`) VALUES (%s, %s, %s, %s, %s, %s)"
    sql = 'SELECT word FROM `polygon_lens_hot_words_score` WHERE id = 4370164'
    a=mysql.search(sql)
    print(a)
    #data = [(1,1,'hello',10,0.32,'post_hot'),(1,1,'hello',10,0.32,'post_hot')]
    #mysql.insert_batch(sql,data)