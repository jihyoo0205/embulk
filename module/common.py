import datetime as dt
import sys
import os
ROOT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

def createDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        print("Successed to create the directory.")
    
    else:
        print("Directory already exists.")

def execSql(cur, sql):
    pass

def setGetDdl() -> str:
    sql = """ BEGIN 
                  DBMS_METADATA.SET_TRANSFORM_PARAM(DBMS_METADATA.SESSION_TRANSFORM,'STORAGE',FALSE);
                  dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'SQLTERMINATOR', true);
                  dbms_metadata.set_transform_param(dbms_metadata.session_transform, 'PRETTY', true);
              END;"""
    
    return sql

def getTabDdl() :
    sql = f"""SELECT 'TABLE', 
                    DBMS_METADATA.GET_DDL('TABLE', ':NAME', ':OWNER') AS DDL_SOURCE 
               FROM DUAL """
    
    return sql

def getIndDdl():
    sql = f""" SELECT 'INDEX', 
                        DBMS_METADATA.GET_DEPENDENT_DDL('INDEX', ':NAME', ':OWNER') AS DDL_SOURCE 
                 FROM DUAL """

    return sql