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
        # 변수 초기화
        self.execItem = {}
        self.configItem = {}
        self.query = ''
        self.maxThreads = 1
        self.minOutputTasks = 1
        
        # TODO: type 별로 인자값 넣기
        self.setDriverPath('Oracle')

    def setDriverPath(self, type):
        # TODO: type -> oracle / mysql 따라 jdbc 경로 따로 지정
        if type == 'Oracle':
            self.configItem = {'driver_path' : fr"{cm.ROOT_PATH}\env\lib\ojdbc8.jar"}
        
        elif type == 'MySQL':
            pass

    def setType(self, type):
        self.configItem['type'] = type

    def setIp(self, ip):
        self.configItem['ip'] = ip
    
    def setPort(self, port):
        self.configItem['port'] = port

    def setUser(self, user):
        self.configItem['user'] = user
    
    def setPw(self, pw):
        self.configItem['pw'] = pw

    def setSid(self,sid):
        self.configItem['sid'] = sid
    
    def setQuery(self, tableList):
        # schema.table_name -> schema와 table명 분리
        item = tableList.split(".")
        self.query = f"\"select * from {item[0]}.{item[1]}\""
        self.configItem['query'] = self.query

    def setTable(self, tableList):
        # schema.table_name -> schema와 table명 분리
        item = tableList.split(".")
        # table만 입력
        self.configItem['table'] = item[1]
        
    def setMaxThreads(self,maxThreads):
        self.execItem['max_threads'] = maxThreads
    
    def setMinOutputTasks(self, minOutputTasks):
        self.execItem['min_output_tasks'] = minOutputTasks

def makeQuery(owner, table) -> str:
    # 쿼리를 직접 입력받지 않으면, 선택한 객체로 구성
    if query is None:
        if cols is None:
            cols = "*"
        query = f"\"select {cols} from {owner}.{table}\""

    # 쿼리를 직접 입력받으면, 수정하지 않고 그대로 리턴
    return query

def main(srcYmlConfig, tgtYmlConfig) -> YmlConfig:
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