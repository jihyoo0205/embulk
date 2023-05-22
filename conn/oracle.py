import cx_Oracle as co
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def startConn(src):
    try:
        # username sys 면 sysdba 모드
        if src.user.upper() == 'SYS':
            conn = co.connect(
                user = src.user, 
                password = src.passwd, 
                dsn = src.host+":"+src.port+"/"+src.dbName,
                mode = co.SYSDBA,
                threaded = True)
        else:
            conn = co.connect(
                user = src.user, 
                password = src.passwd, 
                dsn = src.host+":"+src.port+"/"+src.dbName,
                threaded = True)
        
    except co.DatabaseError as e:
        print('Database connection error: %s' %(e))
        exit()
    
    return conn

def endConn(cur, conn):
    cur.close()
    conn.close()