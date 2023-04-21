# Embulk yml 파라미터
# oracle : https://www.rubydoc.info/gems/embulk-input-oracle/0.10.1
# mysql  :
import datetime as dt, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class YmlConfig:
    def __init__(self):
        self.tnsPath = r"C:\app\client\product\19.0.0\client_1\network\admin"
        self.driverPath = r"C:\app\client\product\19.0.0\client_1\jdbc\lib\ojdbc8.jar"
        self.host = ''
        self.port = ''
        self.type = ''
        self.user = ''
        self.passwd = ''
        self.dbName = ''
        self.table = ''
        self.schema = ''
        self.query = ''
        self.tnsName = ''
        self.maxThreads = 1
        self.minOutputTasks = 1

    def setDriverPath(self, driverPath):
        self.driverPath = driverPath
    
    def setType(self, type):
        self.type = type

    def setHost(self, host):
        self.host = host
    
    def setPort(self, port):
        self.port = port

    def setUser(self, user):
        self.user = user
    
    def setpasswd(self, passwd):
        self.passwd = passwd

    def setDbName(self,dbName):
        self.dbName = dbName
    
    def setQuery(self, query):
        self.query = query
    
    def setTnsPath(self, tnsPath):
        self.tnsPath = tnsPath

    def setTnsName(self,tnsName):
        self.tnsName = tnsName
    
    def setMaxThreads(self,maxThreads):
        self.maxThreads = maxThreads
    
    def setMinOutputTasks(self, minOutputTasks):
        self.minOutputTasks = minOutputTasks

    def getConfig(self):
        print(f'type: {self.type}')
        print(f'driverPath: {self.driverPath}')
        print(f'host: {self.host}')
        print(f'port: {self.port}')
        print(f'tnsPath: {self.tnsPath}')
        print(f'tnsName: {self.tnsName}')
        print(f'dbName: {self.dbName}')
        print(f'user: {self.user}')
        print(f'passwd: {self.passwd}')
        print(f'maxThreads: {self.maxThreads}')
        print(f'minOutputTasks: {self.minOutputTasks}')

    def configOracle(self):
         #driverPath = input('Input the JDBC driver Path : ')

        while True:
            print('1. Direct Connection \n2. Connection using TNS')
            connType = input('Enter number of connection type : ')

            if connType == '1':
                host = input('Input host IP : ')
                self.setHost(host)
                port = input('Input port number : ')
                self.setPort(port)
                break
            
            if connType == '2':
                tnsName = input('Input TNS name : ')
                self.setTnsName(tnsName)
                break
            else:
                print('\nEnter answer again !!\n')

        dbName = input('Input name of database : ')
        self.setDbName(dbName)
        user = input('Input user to connect database : ')
        self.setUser(user)
        passwd = input('Input password of user : ')
        self.setpasswd(passwd)
        maxThreads = input('Input maximum number of threads (default:1) : ') or 1
        self.setMaxThreads(maxThreads)
        minOutputTasks = input('Input minimum number of output tasks (default:1) : ') or 1
        self.setMinOutputTasks(minOutputTasks)

    def configOthers(self):
        host = input('Input host IP : ')
        self.setHost(host)
        port = input('Input port number : ')
        self.setPort(port)
        dbName = input('Input name of database : ')
        self.setDbName(dbName)
        user = input('Input user to connect database : ')
        self.setUser(user)
        passwd = input('Input password of user : ')
        self.setpasswd(passwd)
        maxThreads = input('Input maximum number of threads (default:1) : ') or 1
        self.setMaxThreads(maxThreads)
        minOutputTasks = input('Input minimum number of output tasks (default:1) : ') or 1
        self.setMinOutputTasks(minOutputTasks)

    def execConfig(self):
        type = input('Input the type : ')
        self.setType(type)

        if type.lower() == 'oracle':
            self.configOracle()

        elif type.lower() == 'mysql':
            self.configOthers()
           
        # TODO: 이관대상 테이블/스키마/쿼리 어떻게 입력할지 고민
    
    
def main():
    # -- SOURCE, TARGET Config 정보 변수
    srcYmlConfig = YmlConfig()
    tgtYmlConfig = YmlConfig()

    # -- 1. yml 파일 생성할 경로 입력
    # -- 2. 날짜_시간.yml 포맷으로 생성
    ymlPath = input("Input the path to create the yml file : ")
    
    date = dt.datetime.now()
    ymlPath += '\\' + date.strftime("%Y%m%d_%H%M%S") + '.yml'
    print('Path to the created file : ' + ymlPath)
    
    # -- 대상 DB 정보 입력
    print('\n*********************************************************')
    print('Input Source Database Information')
    print('*********************************************************')
    srcYmlConfig.execConfig()
    print('\n*********************************************************')
    print('Input Target Database Information')
    print('*********************************************************')
    tgtYmlConfig.execConfig()
    
    # -- 파일 Open
    f = open(ymlPath, 'w')

    # -- 입력한 정보 출력
    print('\n*********************************************************')
    print('Check Source Database Information')
    print('*********************************************************')
    srcYmlConfig.getConfig()
    print('\n*********************************************************')
    print('Check Target Database Information')
    print('*********************************************************')
    tgtYmlConfig.getConfig()

    # -- yml 파일 작성 - PARALLEL
    f.write(f'exec:\n')
    f.write(f'  max_threads: {srcYmlConfig.maxThreads}\n')
    f.write(f'  min_output_tasks: {srcYmlConfig.minOutputTasks}\n')

    # -- yml 파일 작성 - SOURCE DB INFORMATION 
    f.write(f'in:\n')
    f.write(f'  type: {srcYmlConfig.type}\n')
    f.write(f'  driver_path: {srcYmlConfig.driverPath}\n')
    f.write(f'  tns_admin_path: {srcYmlConfig.tnsPath}\n')
    f.write(f'  net_service_name: {srcYmlConfig.tnsName}\n')
    f.write(f'  host: {srcYmlConfig.host}\n')
    f.write(f'  port: {srcYmlConfig.port}\n')
    f.write(f'  database: {srcYmlConfig.dbName}\n')
    f.write(f'  user: {srcYmlConfig.user}\n')
    f.write(f'  password: {srcYmlConfig.passwd}\n')
    f.write(f'  query: {srcYmlConfig.query}\n')

    # -- yml 파일 작성 - TARGET DB INFORMATION 
    f.write(f'\nout:\n')
    f.write(f'  type: {tgtYmlConfig.type}\n')
    f.write(f'  host: {tgtYmlConfig.host}\n')
    f.write(f'  port: {tgtYmlConfig.port}\n')
    f.write(f'  database: {tgtYmlConfig.dbName}\n')
    f.write(f'  user: {tgtYmlConfig.user}\n')
    f.write(f'  password: {tgtYmlConfig.passwd}\n')
    f.write(f'  query: {srcYmlConfig.query}\n')
    
    f.close()

    return srcYmlConfig, tgtYmlConfig

if __name__ == "__main__":
    main()