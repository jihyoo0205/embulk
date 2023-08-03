import datetime as dt, os, sys
import make.mk_yml as mkYml
import conn.oracle as oraConn
import conn.mysql as myConn
import ui.main_window as mainWindow
from PySide2.QtWidgets import *

# TODO : Oracle Home, Mysql Home, Embulk 환경변수 셋팅 (Home, Log 디렉토리)

def startOraConn(config) :
    conn = oraConn.startConn(config)
    if conn:
        print ('\n\n' + config.configItem['database'] + " Connected.")
    return conn

def main():
    os.putenv('NLS_LANG', '.UTF8')

    # Main Window 실행
    mainWindow.exec()

    # ORACLE TO MYSQL 시 메타 변환

    # embulk 실행
    os.system("embulk")

    # 데이터 이관

    # 데이터 검증
    

if __name__ == "__main__":
    main()