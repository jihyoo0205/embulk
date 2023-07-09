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

UI_FILE_PATH = fr"{cm.ROOT_PATH}\ui\main.ui"

class MainWindow(QObject):
    def __init__(self, uiFileName, parent=None):
        super(MainWindow, self).__init__(parent)
        uiFile = QFile(uiFileName)
        uiFile.open(QFile.ReadOnly)
        loader = QUiLoader()
        self.window = loader.load(uiFile)
        uiFile.close()
        self.setup_ui()
        self.window.show()
    
    def setup_ui(self):
        self.treeSrcTab = self.__bindQTreeWidget('treeViewSrcTables')
        self.treeMigTab = self.__bindQTreeWidget('treeViewMigTables')
        self.pbPlus = self.__bindQPushButton('pushButtonPlus')
        self.pbMinus = self.__bindQPushButton('pushButtonMinus')
        self.pbPlus.clicked.connect(self.copy_item)
        self.pbMinus.clicked.connect(self.remove_item)

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
    
    def find_item(self, treeList, item):
        count = treeList.topLevelItemCount()
        for i in range(count):
            if item.text(0) == treeList.topLevelItem(i).text(0):
                return i
            
        return -1
    
    def find_child_items(self, parent_item, selected_item):
        count = parent_item.childCount()
        for i in range(count):
            child_item = parent_item.child(i)
            if selected_item.text(0) == child_item.text(0):
                return i
        return -1

    def copy_item(self):
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
            parent_item = item.parent()
            child_count = item.childCount()
            copied_item = item.clone()

            # 1) 최상단 항목일 때
            if parent_item is None:
                if self.find_item(tgtTreeList, copied_item) < 0:
                    tgtTreeList.addTopLevelItem(copied_item)

            # 2) 하위 항목일 때
            else:
                # 선택한 항목이 최하위 항목일 때
                if child_count == 0:
                    copied_parent_item = parent_item.clone()
                    copied_parent_item.takeChildren()
                    retrunIdx = self.find_item(tgtTreeList, copied_parent_item)

                    # 같은 스키마가 없으면 추가
                    if retrunIdx < 0:
                        copied_parent_item.addChild(copied_item)
                        tgtTreeList.addTopLevelItem(copied_parent_item)

                    # 있으면 그 아래에 하위 항목만추가
                    else:
                        target_parent_item = tgtTreeList.topLevelItem(retrunIdx)
                        if self.find_child_items(target_parent_item, copied_item) < 0:
                            target_parent_item.addChild(copied_item)


    def remove_item(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab

        selected_items = srcTreeList.selectedItems()

        for item in selected_items:
            parent_item = item.parent()
            if parent_item is not None:
                if parent_item.childCount() == 1:
                    index = srcTreeList.indexOfTopLevelItem(parent_item)
                    srcTreeList.takeTopLevelItem(index)
                parent_item.removeChild(item)
            else:
                index = srcTreeList.indexOfTopLevelItem(item)
                srcTreeList.takeTopLevelItem(index)



    def clickMoveItem(self):
        sender = self.sender()
        if self.pbPlus == sender:
            srcTreeList = self.treeSrcTab
            tgtTreeList = self.treeMigTab
        else:
            srcTreeList = self.treeMigTab
            tgtTreeList = self.treeSrcTab


        item = srcTreeList.takeTopLevelItem(srcTreeList.currentColumn())
        root = QTreeWidget.invisibleRootItem(tgtTreeList)
        root.addChild(item)


def exec():
    app = QApplication(sys.argv)
    form = MainWindow(UI_FILE_PATH)

    sys.exit(app.exec_())