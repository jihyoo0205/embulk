# https://doc.qt.io/qtforpython-5/tutorials/basictutorial/uifiles.html
# https://hello-bryan.tistory.com/407
# https://onlytojay.medium.com/pyside2로-간단한-calcultor-exe-만들기-3cf247b21f6e

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import module.common as cm
import cx_Oracle
import ui.summary_window as summaryWindow

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # 디스플레이 설정에 따라 변하게
UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\main.ui"

class MainWindow(QObject):
    def __init__(self, uiFileName, parent=None):
        super(MainWindow, self).__init__(parent)
        uiFile = QFile(uiFileName)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()

        # 윈도우를 화면에 표시
        self.setupUi()
        self.window.show()
    
    def setupUi(self):
        self.treeSrcTab = self.__bindQTreeWidget('treeViewSrcTables')
        self.treeMigTab = self.__bindQTreeWidget('treeViewMigTables')
        self.pbPlus = self.__bindQPushButton('pushButtonPlus')
        self.pbMinus = self.__bindQPushButton('pushButtonMinus')
        self.pbPlus.clicked.connect(self.copyItem)
        self.pbMinus.clicked.connect(self.removeItem)
        self.btnConfirm = self.__bindQPushButton('pushButtonConfirm')
        self.btnConfirm.clicked.connect(self.clickConfirm)
        self.editQuery = self.__bindQPlainTextEdit('textEditQuery')
        # ================= 접속 정보 입력 및 접속 버튼 [START] ==================================
        self.srcType = self.__bindQComboBox('comboBoxSrcDbms')             # Source DB Type
        self.srcIp = self.__bindQLineEdit('lineEditSrcHost')               # Source DB 접속 IP
        self.srcPort = self.__bindQLineEdit('lineEditSrcPort')             # Source DB 접속 Port
        self.srcSid = self.__bindQLineEdit('lineEditSrcDB')                # Source DB Name(SID)
        self.srcUser = self.__bindQLineEdit('lineEditSrcUser')             # Source DB 접속 유저
        self.srcPw = self.__bindQLineEdit('lineEditSrcPasswd')             # Source DB 접속 패스워드
        self.srcPw.setEchoMode(QLineEdit.Password)                         # Source 패스워드 마스킹
        self.tgtType = self.__bindQComboBox('comboBoxTgtDbms')             # Target DB Type
        self.tgtIp = self.__bindQLineEdit('lineEditTgtHost')               # Target DB 접속 IP
        self.tgtPort = self.__bindQLineEdit('lineEditTgtPort')             # Target DB 접속 Port
        self.tgtSid = self.__bindQLineEdit('lineEditTgtDB')                # Target DB Name(SID)
        self.tgtUser = self.__bindQLineEdit('lineEditTgtUser')             # Target DB 접속 유저
        self.tgtPw = self.__bindQLineEdit('lineEditTgtPasswd')             # Target DB 접속 패스워드
        self.tgtPw.setEchoMode(QLineEdit.Password)                         # Target 패스워드 마스킹
        self.btnTestConn = self.__bindQPushButton('pushButtonSrcTestConn') # 버튼 클릭 시 실행될 함수 연결
        self.btnTestConn.clicked.connect(self.testConnDb)                  # -> Test Connection
        self.btnConnect = self.__bindQPushButton('pushButtonSrcConn')      # 버튼 클릭 시 실행될 함수 연결
        self.btnConnect.clicked.connect(self.connDb)                       # -> Connection
        self.btnStart = self.__bindQPushButton('pushButtonStart')          # 버튼 클릭 시 실행될 함수 연결
        self.btnStart.clicked.connect(self.clickStart)                          # -> Start
        # ================= 접속 정보 입력 및 접속 버튼 [END] ==================================
        
        # 테스트 용도
        self.srcUser.setText('mig')
        self.srcPw.setText('mig')
        self.srcIp.setText('51.51.102.101')
        self.srcPort.setText('1521')
        self.srcSid.setText('test01')



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
        return btn
    
    def findItem(self, treeList, item):
        count = treeList.topLevelItemCount()
        for i in range(count):
            if item.text(0) == treeList.topLevelItem(i).text(0):
                return i
            
        return -1
    
    def findChildItems(self, parentItem, selected_item):
        count = parentItem.childCount()
        for i in range(count):
            child_item = parentItem.child(i)
            if selected_item.text(0) == child_item.text(0):
                return i
        return -1

    # ================= 테스트 접속 [START] ==================================
    def testConnDb(self):
        # 입력된 오라클 정보를 매핑
        user_id = self.srcUser.text()
        user_pw = self.srcPw.text()
        ip = self.srcIp.text()
        port = self.srcPort.text()
        sid = self.srcSid.text()

        try:
            # 데이터베이스 연결 정보를 설정
            dsn = cx_Oracle.makedsn(ip, port, sid)
            conn = cx_Oracle.connect(user_id, user_pw, dsn)

            # 성공 텍스트 팝업
            QMessageBox.information(
                self.window, 'Message',
                '성공적으로 연결되었습니다.',
                QMessageBox.Ok
            )

            # 연결을 종료
            conn.close()

        except cx_Oracle.DatabaseError as e:
            # 실패 텍스트 팝업
            QMessageBox.warning(
                self.window, 'Message',
                f'연결 실패: {e}',
                QMessageBox.Ok
            )
    # ================= 테스트 접속 [END] ==================================

    # ================= 접속 및 테이블리스트 추가 [START] ==================================
    def connDb(self):
        # pushButtonSrcTestConn 와 동일한 함수 구현
        user_id = self.srcUser.text()
        user_pw = self.srcPw.text()
        ip = self.srcIp.text()
        port = self.srcPort.text()
        sid = self.srcSid.text()

        try:
            dsn = cx_Oracle.makedsn(ip, port, sid)
            conn = cx_Oracle.connect(user_id, user_pw, dsn)

            # 성공 텍스트 팝업
            QMessageBox.information(
                self.window, 'Message',
                '성공적으로 연결되었습니다.',
                QMessageBox.Ok
            )
            
            # 커서 생성 및 쿼리를 실행
            cursor = conn.cursor()
            rows = cursor.execute(cm.getTblList()).fetchall()

            # 반환할 QTreeWidget 생성
            table_tree = self.__bindQTreeWidget("treeViewMigTables")
            table_tree.clear()
            table_tree = self.__bindQTreeWidget("treeViewSrcTables")
            table_tree.clear()
            table_tree.setColumnCount(1)
            table_tree.setHeaderLabels(["Owner - Table Name - Partition Name"])
        
            # 트리 아이템 추가
            for row in rows:
                owner = row[0]
                table_name = row[1]
                partition = row[2] # or "N/A"
        
                owner_item = table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(owner, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(table_tree, [owner])
                table_item = table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0)[0] if table_tree.findItems(table_name, Qt.MatchExactly | Qt.MatchRecursive, 0) else QTreeWidgetItem(owner_item, [table_name])
                if partition:
                    partition_item = QTreeWidgetItem(table_item, [partition])
        
            # 연결을 종료
            conn.close()
        except cx_Oracle.DatabaseError as e:
            # 실패 텍스트 팝업
            QMessageBox.warning(
                self.window, 'Message',
                f'연결 실패: {e}',
                QMessageBox.Ok
            )

    # ================= 접속 및 테이블리스트 추가 [END] ==================================


    # ================= 트리 추가 [START] ==================================
    def copyItem(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab

        selected_items = srcTreeList.selectedItems()

        # 선택했음
        for item in selected_items:
            parentItem = item.parent()
            grandParentItem = parentItem.parent() if parentItem is not None else None
            copiedItem = item.clone()

            # 최상단 항목일 때
            if parentItem is None:
                if self.findItem(tgtTreeList, copiedItem) < 0:
                    tgtTreeList.addTopLevelItem(copiedItem)

            # 중간 항목일 때
            elif parentItem is not None and grandParentItem is None:
                copiedParentItem = parentItem.clone()
                copiedParentItem.takeChildren()
        
                returnIdx = self.findItem(tgtTreeList, copiedParentItem)
        
                if returnIdx < 0:
                    tgtTreeList.addTopLevelItem(copiedParentItem)
                    tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copiedParentItem)).addChild(copiedItem)
        
                else:
                    target_parentItem = tgtTreeList.topLevelItem(returnIdx)
                    if self.findChildItems(target_parentItem, copiedItem) < 0:
                        target_parentItem.addChild(copiedItem)
            
            # 최하위 항목일 때
            elif parentItem is not None and grandParentItem is not None:
                copiedGrandParentItem = grandParentItem.clone()
                copiedGrandParentItem.takeChildren()
                grandparent_return_idx = self.findItem(tgtTreeList, copiedGrandParentItem)
                
                # 부모 항목 아래에 추가
                copiedParentItem = parentItem.clone()
                copiedParentItem.takeChildren()
                
                if grandparent_return_idx < 0:
                    copiedGrandParentItem = grandParentItem.clone()
                    copiedGrandParentItem.takeChildren()
                    tgtTreeList.addTopLevelItem(copiedGrandParentItem)
                    tgtTreeList.topLevelItem(tgtTreeList.indexOfTopLevelItem(copiedGrandParentItem)).addChild(copiedParentItem)
                else:
                    target_grandParentItem = tgtTreeList.topLevelItem(grandparent_return_idx)
                    childIdx = self.findChildItems(target_grandParentItem, copiedParentItem)
                    if childIdx < 0:
                        target_grandParentItem.addChild(copiedParentItem)
                    else:
                        copiedParentItem = target_grandParentItem.child(childIdx)
            
                # 부모 항목 아래에 추가
                if self.findChildItems(copiedParentItem, copiedItem) < 0:
                    copiedParentItem.addChild(copiedItem)

    def removeItem(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab

        selected_items = srcTreeList.selectedItems()

        for item in selected_items:
            parentItem = item.parent()
            if parentItem is not None:
                if parentItem.childCount() == 1:
                    index = srcTreeList.indexOfTopLevelItem(parentItem)
                    srcTreeList.takeTopLevelItem(index)
                parentItem.removeChild(item)
            else:
                index = srcTreeList.indexOfTopLevelItem(item)
                srcTreeList.takeTopLevelItem(index)
    # ================= 트리 추가 제거 [END] ==================================

    
    # ================= 입력한 쿼리 트리에 넣기 [START] =============================
    def clickConfirm(self):
        text = self.editQuery.toPlainText()
        parentItem = None
        childItem = None
        childExists = False
        # Query 최상위항목이 있는지 검사
        for i in range(self.treeMigTab.topLevelItemCount()):
            item = self.treeMigTab.topLevelItem(i)
            if item.text(0) == "Query":
                parentItem = item
                # 있으면 입력한 텍스트와 동일한 하위 항목이 있는지 검사
                for j in range(parentItem.childCount()):
                    childItem = parentItem.child(j)
                    print(childItem.text(0))
                    if childItem is not None and childItem.text(0) == text:
                        childExists = True
                        break
                break
        
        # Query 최상위 항목을 찾지 못했다면 추가
        if parentItem is None: 
            parentItem = QTreeWidgetItem(self.treeMigTab, ["Query"])
        # 하위 항목을 찾지 못했다면 입력한 텍스트로 추가
        if not childExists:
            childItem = QTreeWidgetItem(parentItem, [text])
        # visible 설정
        parentItem.setExpanded(True)
    # ================= 입력한 쿼리 트리에 넣기 [START] =============================


    # ================= Summary 창 띄우기 [START] =============================
    def clickStart(self):
        summary = summaryWindow.SummaryWindow()
        self.copyTree(self.treeMigTab, summary.treeMigTab)
        summary.setParent(self)
    # ================= Summary 창 띄우기 [END] ===============================


    # ================= TreeWidget 복사 [START] ===============================
    def copyTree(self, srcTree, tgtTree):
        count = srcTree.topLevelItemCount()
        for i in range(count):
            item = srcTree.topLevelItem(i)
            clonedItem = item.clone()
            tgtTree.addTopLevelItem(clonedItem)
    # ================= TreeWidget 복사 [END] =================================

def exec():
    app = QApplication(sys.argv)
    form = MainWindow(UI_FILE_PATH)
    sys.exit(app.exec_())