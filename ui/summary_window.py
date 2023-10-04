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
        self.btnPreview = self.__bindQPushButton('pushButtonPreview')
        self.btnPreview.clicked.connect(self.clickPreview)                     # Preview 버튼
        self.btnRun = self.__bindQPushButton('pushButtonRun')
        self.btnRun.clicked.connect(self.clickRun)                             # Run 버튼
        
        # Radio Button 그룹 생성 - Mode
        self.btnGroupMode = QButtonGroup()                                # Mode Radio Button 그룹
        self.radioInsert = self.__bindObject(QRadioButton, 'radioButtonInsert')
        self.radioDirect = self.__bindObject(QRadioButton, 'radioButtonDirect')
        self.radioMerge = self.__bindObject(QRadioButton, 'radioButtonMerge')
        self.radioTrunc = self.__bindObject(QRadioButton, 'radioButtonTrunc')
        self.radioReplace = self.__bindObject(QRadioButton, 'radioButtonReplace')
        self.btnGroupMode.addButton(self.radioInsert)
        self.btnGroupMode.addButton(self.radioDirect)
        self.btnGroupMode.addButton(self.radioMerge)
        self.btnGroupMode.addButton(self.radioTrunc)
        self.btnGroupMode.addButton(self.radioReplace)

        
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
    
    # ================================== yml 파일 생성 [START] ==================================
    def clickMakeYmlFile(self):
        # Mode 변수 받아오기
        selectedMode = self.btnGroupMode.checkedButton()
        # Mode 선택 안 되어있으면 에러
        if not selectedMode:
            QMessageBox.warning(
                    self.window, 'Message',
                    'Insert Mode를 선택해주세요.',
                    QMessageBox.Ok
                )
        
        # Mode 클릭 돼있을 때만 수행
        else:
            # Config 변수 셋팅
            try:
                srcYmlConfig = mkYml.YmlConfig()
                tgtYmlConfig = mkYml.YmlConfig()

                tableList = self.treeWidgetToList(self.treeMigTab)

                for i in tableList:
                    srcYmlConfig.setType(self.parent().srcType.currentText())
                    srcYmlConfig.setIp(self.parent().srcIp.text())
                    srcYmlConfig.setPort(self.parent().srcPort.text())
                    srcYmlConfig.setSid(self.parent().srcSid.text())
                    srcYmlConfig.setUser(self.parent().srcUser.text())
                    srcYmlConfig.setPw(self.parent().srcPw.text())
                    srcYmlConfig.setQuery(i)                    # 쿼리 형태로 저장
                    
                    tgtYmlConfig.setType(self.parent().tgtType.currentText())
                    tgtYmlConfig.setIp(self.parent().tgtIp.text())
                    tgtYmlConfig.setPort(self.parent().tgtPort.text())
                    tgtYmlConfig.setSid(self.parent().tgtSid.text())
                    tgtYmlConfig.setUser(self.parent().tgtUser.text())
                    tgtYmlConfig.setPw(self.parent().tgtPw.text())
                    tgtYmlConfig.setQuery(i)                    # 테이블 형태로 저장
                    tgtYmlConfig.setMode(selectedMode.text())

                    # 셋팅 값으로 Yml 파일 생성
                    mkYml.exec(srcYmlConfig, tgtYmlConfig)
                QMessageBox.information(
                    self.window, 'Message',
                    '파일이 생성되었습니다.',
                    QMessageBox.Ok
                )
            except Exception as e:
                QMessageBox.warning(
                    self.window, 'Message',
                    f'파일 생성 실패\n* {e}',
                    QMessageBox.Ok
                )
        
    # 트리 형태를 리스트로 변환
    def treeWidgetToList(self, treeWidget):
        rootItems = [treeWidget.topLevelItem(i) for i in range(treeWidget.topLevelItemCount())]
        result = []

        for rootItem in rootItems:
            self.processItem(rootItem, result, "")

        return result
    
    # __ 구분자 넣어서 "schema__table__partition" 형태로 저장
    def processItem(self, item, result, parentText):
        itemText = item.text(0)

        if parentText:
            fullText = parentText + "__" + itemText
        else:
            fullText = itemText

        childCount = item.childCount()
        if childCount > 0:
            for i in range(childCount):
                childItem = item.child(i)
                self.processItem(childItem, result, fullText)

                # 파티션 항목 처리
                grandchildCount = childItem.childCount()
                if grandchildCount > 0:
                    for j in range(grandchildCount):
                        grandchildItem = childItem.child(j)
                        self.processItem(grandchildItem, result, fullText + "__" + childItem.text(0))
        else:
            result.append(fullText)
    # ================================== yml 파일 생성 [END] ==================================

    # ================================== Preview 수행 [START] ==================================
    def clickPreview(self):
        os.system(fr"embulk preview {cm.ROOT_PATH}\files\yml\MIG.TEST01_20230828.yml")
    # ================================== Preview 수행 [END] ==================================

    def clickRun(self):
        pass


    