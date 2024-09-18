# !/usr/bin/python 
# coding:utf-8 
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
class sql_connections():
    def __init__(self, db, schema):
        # Connection Variables
        engine = create_engine("mysql+pymysql://team_pi:pi42838254@61.31.170.%s:3306/%s" %(db, schema), poolclass=NullPool)
        self.cursor = engine.connect()

    def sel_col_wh(self, columns, db, idx, id):
        SQL_QUERY = "SELECT %s FROM %s where %s like '%s'" %(columns, db, idx, id)
        query = self.cursor.execute(text(SQL_QUERY))
        records = [i for i in query]
        return records
    
    def sel_col(self, columns, db):
        SQL_QUERY = "SELECT %s FROM %s" %(columns, db)
        query = self.cursor.execute(text(SQL_QUERY))
        records = [i for i in query]
        return records
    
    def sql(self, query):
        SQL_QUERY = query
        query = self.cursor.execute(text(SQL_QUERY))
        records = [i for i in query]
        return records