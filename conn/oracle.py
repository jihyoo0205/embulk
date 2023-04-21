import cx_Oracle as co
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def startConn(src):
    #co.init_oracle_client(config_dir=r"C:\app\client\product\19.0.0\client_1\network\admin")
    try:
        # host 주소 있으면 direct / null이면 TNS
        if src.host is not None:
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
        else:
            res = os.popen('tnsping ' + src.tnsName).read()
            print('\n\n'+res+'\n\n')
            # username sys 면 sysdba 모드
            if src.user.upper() == 'SYS':
                conn = co.connect(
                    user = src.user, 
                    password = src.passwd, 
                    dsn = src.tnsName,
                    mode = co.SYSDBA,
                    threaded = True)
            else:
                conn = co.connect(
                    user = src.user, 
                    password = src.passwd, 
                    dsn = src.tnsName,
                    threaded = True)
        
    except co.DatabaseError as e:
        print('Database connection error: %s' %(e))
        exit()
    
    return conn

def endConn(cur, conn):
    cur.close()
    conn.close()