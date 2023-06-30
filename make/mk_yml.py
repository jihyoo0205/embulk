# Embulk yml 파라미터
# oracle : https://www.rubydoc.info/gems/embulk-input-oracle/0.10.1
#          https://www.rubydoc.info/gems/embulk-output-oracle/0.8.7
# mysql  : 
import datetime as dt
import sys
import os
import module.common as cm
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class YmlConfig:
    def __init__(self):
        self.execItem = {}
        self.configItem = {}

        self.table = []
        self.query = ''

        self.setDriverPath()

    def setDriverPath(self):
        # TODO: type -> oracle / mysql 따라 jdbc 경로 따로 지정
        self.configItem = {'driver_path' : fr"{cm.ROOT_PATH}\env\lib\ojdbc8.jar"}
    
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
    
    # TODO: 컬럼 선택지는 나중에
    def setQuery(self, schema, table):
        self.query = f"\"select * from {schema}.{table}\""
        self.configItem['query'] = self.query

    def setTable(self, tableList):
        item = tableList.split(',')
        for i in item:
            self.table.append(i.replace(" ", ""))
        
    def setMaxThreads(self,maxThreads):
        self.execItem['max_threads'] = maxThreads
    
    def setMinOutputTasks(self, minOutputTasks):
        self.execItem['min_output_tasks'] = minOutputTasks

    # GUI면 필요없음
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
        table = input('Input list of tables(ex: schema.a, schema.b ..) : ')
        self.setTable(table)
        maxThreads = input('Input maximum number of threads (default: 1) : ') or 1
        self.setMaxThreads(maxThreads)
        minOutputTasks = input('Input minimum number of output tasks (default: 1) : ') or 1
        self.setMinOutputTasks(minOutputTasks)

def makeQuery() -> str:
    cols = input('columns: ')
    owner = input('owner: ')
    table = input('tables: ')
    query = input('query: ') or None

    # 쿼리를 직접 입력받지 않으면, 선택한 객체로 구성
    if query is None:
        if cols is None:
            cols = "*"
        query = f"\"select {cols} from {owner}.{table}\""

    # 쿼리를 직접 입력받으면, 수정하지 않고 그대로 리턴
    return query

def main() -> YmlConfig:
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
    print('*********************************************************\n')
    tgtYmlConfig.execConfig()

    # yml 파일 저장할 디렉토리 없으면 생성
    cm.createDir(cm.ROOT_PATH + r'\files\yml')
    # 이관 대상 테이블 개수만큼 yml 파일 생성
    for i in srcYmlConfig.table :
        # 날짜_테이블명.yml 포맷으로 생성
        ymlPath = fr'{cm.ROOT_PATH}\files\yml'
        date = dt.datetime.now()
        ymlPath += '\\' + i + '_' + date.strftime("%Y%m%d") + '.yml'

        # 파일 Open
        f = open(ymlPath, 'w')

        # yml 파일 작성 - PARALLEL
        f.write(f'exec:\n')
        for k, v in srcYmlConfig.execItem.items():
            f.write(f'  {k}: {v}\n')
        
        # schema.table_name -> schema와 table명 분리 // GUI면 필요 없음
        tmpTable = i.split(".")
        srcYmlConfig.setQuery(tmpTable[0], tmpTable[1])

        # yml 파일 작성 - SOURCE DB 정보 
        f.write(f'in:\n')
        for k, v in srcYmlConfig.configItem.items():
            f.write(f'  {k}: {v}\n')
        
        # yml 파일 작성 - TARGET DB 정보 
        f.write(f'\nout:\n')
        for k, v in tgtYmlConfig.configItem.items():
            f.write(f'  {k}: {v}\n')
        
        f.close()

    return srcYmlConfig, tgtYmlConfig

if __name__ == "__main__":
    main()