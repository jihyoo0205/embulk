from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
import sys, os, subprocess
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import module.common as cm
import module.print_log as printLog

os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1' # 디스플레이 설정에 따라 변하게
UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\preview_log.ui"

class PreviewLogWindow(QObject):
    def __init__(self, parent=None):
        super(PreviewLogWindow, self).__init__(parent)
        uiFile = QFile(UI_FILE_PATH)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()

        # 윈도우 띄우기
        self.setupUi()
        self.window.show()

    def setupUi(self):
        self.textEditLog = self.__bindQPlainTextEdit('textEditLog')
        self.textEditLog.setReadOnly(True)
        
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
    