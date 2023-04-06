import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class YmlConfig:
    def __init__(self):
        self.tnsPath = r"C:\app\client\product\19.0.0\client_1\network\admin"
        self.driverPath = r"C:\app\client\product\19.0.0\client_1\jdbc\lib\ojdbc8.jar"
        self.host = ''
        self.type = ''
        self.user = ''
        self.pw = ''
        self.db = ''
        self.table = ''
        self.schema = ''
        self.query = ''
        self.tnsName = ''
        self.tabList = []
        self.schemaList = []

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
    
    def setPw(self, pw):
        self.pw = pw

    def setDb(self,db):
        self.db = db
    
    def setQuery(self, query):
        self.query = query
    
    def setTnsPath(self, tnsPath):
        self.tnsPath = tnsPath

    def setTnsName(self,tnsName):
        self.tnsName = tnsName

    def setTabList(self, tabList):
        self.tabList = tabList

    def setSchemaList(self, schemaList):
        self.schemaList = schemaList

    def execConfig(self):
        type = input('Input the type : ')
        self.setType(type)

        if type.lower() == 'oracle':
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

        elif type.lower() == 'mysql':
            host = input('Input host IP : ')
            self.setHost(host)

            port = input('Input port number : ')
            self.setPort(port)
            
        db = input('Input name of database : ')
        self.setDb(db)

        user = input('Input user to connect database : ')
        self.setUser(user)

        pw = input('Input password of user : ')
        self.setPw(pw)

        # TODO: 이관대상 테이블/스키마 어떻게 입력할지 고민
        tabName = input('Input name of table (ex. owner.table_name): ')
        tabList = []
        self.setTabList(tabList)
    
    
def main():
    # SOURCE, TARGET Config 정보 변수
    srcYmlConfig = YmlConfig()
    tgtYmlConfig = YmlConfig()

    print('*********************************************************')
    print('Input Source Database Infomation')
    print('*********************************************************')
    srcYmlConfig.execConfig()

    print('*********************************************************')
    print('Input Target Database Infomation')
    print('*********************************************************')
    tgtYmlConfig.execConfig()
    
    return srcYmlConfig, tgtYmlConfig

if __name__ == "__main__":
    main()