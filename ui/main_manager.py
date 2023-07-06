from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import module.common as cm
import cx_Oracle

UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\main.ui"

class MainWindow(QObject):
    def __init__(self, uiFileName, parent=None):
        super(MainWindow, self).__init__(parent)
        uiFile = QFile(uiFileName)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()

# ================= 접속 및 테이블리스트 추가 [START] ==================================

        # UI에 연결할 변수를 선언
        self.le_ip = self.__bindQLineEdit('lineEditSrcHost')
        self.le_port = self.__bindQLineEdit('lineEditSrcPort')
        self.le_sid = self.__bindQLineEdit('lineEditSrcDB')
        self.le_id = self.__bindQLineEdit('lineEditSrcUser')
        self.le_pw = self.__bindQLineEdit('lineEditSrcPasswd')
        self.btn_connect = self.__bindQPushButton('pushButtonSrcConn')

        # 버튼 클릭 시 실행될 함수를 연결
        self.btn_connect.clicked.connect(self.__connect_db)

        # 윈도우를 화면에 표시
        self.window.show()

    def __connect_db(self):
        # 입력된 오라클 정보를 매핑
        user_id = self.le_id.text()
        user_pw = self.le_pw.text()
        ip = self.le_ip.text()
        port = self.le_port.text()
        sid = self.le_sid.text()

        # 데이터베이스 연결 정보를 설정
        dsn = cx_Oracle.makedsn(ip, port, sid)
        conn = cx_Oracle.connect(user_id, user_pw, dsn)

        # 커서 생성 및 쿼리를 실행
        cursor = conn.cursor()
        rows = cursor.execute(cm.getTblList()).fetchall()
    
        # 반환할 QTreeWidget 생성
        table_tree = self.__bindQTreeWidget("treeViewSrcTables")
        table_tree.clear()
        table_tree.setColumnCount(3)
        table_tree.setHeaderLabels(["Owner", "Table Name", "Partition Name"])
    
        # 트리 아이템 추가
        for row in rows:
            owner = row[0]
            table_name = row[1]
            partition = row[2] or "N/A"
    
            owner_item = table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(table_tree, [owner])
            table_item = table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(owner_item, [table_name])
            partition_item = QTreeWidgetItem(table_item, [partition])
    
        # 연결을 종료
        conn.close()
# ================= 접속 및 테이블리스트 추가 [END] ==================================

    def __bindQLineEdit(self, objectName):
        return self.window.findChild(QLineEdit, objectName)
    
    def __bindQLabel(self, objectName):
        return self.window.findChild(QLabel, objectName)
    
    def __bindQPlainTextEdit(self, objectName):
        return self.window.findChild(QPlainTextEdit, objectName)
    
    def __bindQComboBox(self, objectName):
        return self.window.findChild(QComboBox, objectName)
    
    def __bindQTreeWidget(self, objectName):
        return self.window.findChild(QTreeWidget, objectName)
    
    def __bindObject(self, qType, objectName):
        return self.window.findChild(qType, objectName)

    def __bindQPushButton(self, objectName):
        btn = self.window.findChild(QPushButton, objectName)
        # 버튼 클릭했을 때 click_objectName 함수 호출
        #eval(f'btn.clicked.connect(self.click_{objectName})')
        return btn

def exec():
    app = QApplication(sys.argv)
    form = MainWindow(UI_FILE_PATH)

    sys.exit(app.exec_())