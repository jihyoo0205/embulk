from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import module.common as cm
import cx_Oracle
import make.mk_yml as mkYml
import ui.main_window as mainWindow

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # 디스플레이 설정에 따라 변하게
UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\summary.ui"

class SummaryWindow(QObject):
    def __init__(self, parent=None):
        super(SummaryWindow, self).__init__(parent)
        uiFile = QFile(UI_FILE_PATH)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()

        # 윈도우 띄우기
        self.setupUi()
        self.window.show()

    def setupUi(self):
        self.treeMigTab = self.__bindQTreeWidget('treeViewMigTables')
        self.btnMakeYmlFile = self.__bindQPushButton('pushButtonMakeYmlFile')
        self.btnMakeYmlFile.clicked.connect(self.clickMakeYmlFile)             # Yml File 생성 버튼
        self.btnShowYmlFile = self.__bindQPushButton('pushButtonShowYmlFile')
        self.btnShowYmlFile.clicked.connect(self.clickShowYmlFile)             # Yml File 경로 열기 버튼
        self.btnPreview = self.__bindQPushButton('pushButtonPreview')
        self.btnPreview.clicked.connect(self.clickPreview)                     # Preview 버튼
        self.btnRun = self.__bindQPushButton('pushButtonRun')
        self.btnRun.clicked.connect(self.clickRun)                             # Run 버튼

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
    
    def clickMakeYmlFile(self):        
        # ================= Config 변수 셋팅 [START] ================================
        srcYmlConfig = mkYml.YmlConfig()
        tgtYmlConfig = mkYml.YmlConfig()

        tableList = self.treeWidgetToList(self.treeMigTab)

        for i in tableList:
            srcYmlConfig.setType(self.parent().srcType)
            srcYmlConfig.setIp(self.parent().srcIp)
            srcYmlConfig.setPort(self.parent().srcPort)
            srcYmlConfig.setSid(self.parent().srcSid)
            srcYmlConfig.setUser(self.parent().srcUser)
            srcYmlConfig.setPw(self.parent().srcPw)
            srcYmlConfig.setQuery(i)                    # 쿼리 형태로 저장
            
            tgtYmlConfig.setType(self.parent().tgtType)
            tgtYmlConfig.setIp(self.parent().tgtIp)
            tgtYmlConfig.setPort(self.parent().tgtPort)
            tgtYmlConfig.setSid(self.parent().tgtSid)
            tgtYmlConfig.setUser(self.parent().tgtUser)
            tgtYmlConfig.setPw(self.parent().tgtPw)
            tgtYmlConfig.setTable(i)                    # 테이블 형태로 저장
        # ================= Config 변수 셋팅 [END] ================================
        

    def treeWidgetToList(self, treeWidget):
        rootItems = [treeWidget.topLevelItem(i) for i in range(treeWidget.topLevelItemCount())]
        result = []

        for rootItem in rootItems:
            self.processItem(rootItem, result, "")

        return result
    
    def processItem(self, item, result, parentText):
        itemText = item.text(0)

        if parentText:
            fullText = parentText + "." + itemText
        else:
            fullText = itemText

        childCount = item.childCount()
        if childCount > 0:
            for i in range(childCount):
                childItem = item.child(i)
                self.processItem(childItem, result, fullText)
        else:
            result.append(fullText)

    def clickShowYmlFile(self):
        pass

    def clickPreview(self):
        pass

    def clickRun(self):
        pass


    