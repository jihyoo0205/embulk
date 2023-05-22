# Embulk yml 파라미터
# oracle : https://www.rubydoc.info/gems/embulk-input-oracle/0.10.1
# mysql  :
import datetime as dt, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class YmlConfig:
    def __init__(self):
        self.execItem = {}
        self.configItem = {}

        self.table = []
        self.schema = ''
        self.query = ''
        self.where = ''
        self.orderby = ''

        self.setDriverPath()

    def setDriverPath(self):
        self.configItem = {'driver_path' : r"C:\app\client\product\19.0.0\client_1\jdbc\lib\ojdbc8.jar"}
    
    def setType(self, type):
        self.configItem['type'] = type

    def setHost(self, host):
        self.configItem['host'] = host
    
    def setPort(self, port):
        self.configItem['port'] = port

    def setUser(self, user):
        self.configItem['user'] = user
    
    def setpasswd(self, passwd):
        self.configItem['passwd'] = passwd

    def setDbName(self,dbName):
        self.configItem['database'] = dbName
    
    def setQuery(self, query):
        self.configItem['query'] = query
    
    def setTable(self, tableList):
        item = tableList.split(',')
        for i in item:
            self.table.append(i.replace(" ", ""))
        
    def setMaxThreads(self,maxThreads):
        self.execItem['max_threads'] = maxThreads
    
    def setMinOutputTasks(self, minOutputTasks):
        self.execItem['min_output_tasks'] = minOutputTasks

    def execConfig(self):
        type = input('Input the type : ')
        self.setType(type)
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
        table = input('Input list of tables(ex: schema.a, schema.b, schema.c ..) : ')
        self.setTable(table)
        maxThreads = input('Input maximum number of threads (default:1) : ') or 1
        self.setMaxThreads(maxThreads)
        minOutputTasks = input('Input minimum number of output tasks (default:1) : ') or 1
        self.setMinOutputTasks(minOutputTasks)
    
    
def main():
    # SOURCE, TARGET Config 정보 변수
    srcYmlConfig = YmlConfig()
    tgtYmlConfig = YmlConfig()

    # 대상 DB 정보 입력
    print('\n*********************************************************')
    print('Input Source Database Information')
    print('*********************************************************\n')
    srcYmlConfig.execConfig()

    print('\n*********************************************************')
    print('Input Target Database Information')
    print('*********************************************************\n\n')
    #tgtYmlConfig.execConfig()

    # yml 파일 생성할 경로 입력
    createdPath = input("Input the path to create the yml file : ")

    # 이관 대상 테이블 개수만큼 yml 파일 생성
    for i in srcYmlConfig.table :
        ymlPath = createdPath
        # 날짜_테이블명.yml 포맷으로 생성
        date = dt.datetime.now()
        ymlPath += '\\' + i + '_' + date.strftime("%Y%m%d") + '.yml'
        print('Path to the created file : ' + ymlPath)  

        # 파일 Open
        f = open(ymlPath, 'w')

        # yml 파일 작성 - PARALLEL
        f.write(f'exec:\n')
        for k, v in srcYmlConfig.execItem.items():
            f.write(f'  {k}: {v}\n')

        # yml 파일 작성 - SOURCE DB 정보 
        f.write(f'in:\n')
        for k, v in srcYmlConfig.configItem.items():
            f.write(f'  {k}: {v}\n')
        
        # schema.table_name -> schema와 table명 분리
        tmpTable = i.split(".")
        f.write(f'  schema: {tmpTable[0]}\n')
        f.write(f'  table: {tmpTable[1]}\n')
        
        # yml 파일 작성 - TARGET DB 정보 
        f.write(f'\nout:\n')
        for k, v in tgtYmlConfig.configItem:
            f.write(f'  {k}: {v}\n')
        # target 테이블?
        
        f.close()

    return srcYmlConfig, tgtYmlConfig

if __name__ == "__main__":
    main()