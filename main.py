import datetime as dt, os, sys
import make.mk_yml as mkYml
import conn.oracle as oraConn
import conn.mysql as myConn
import ui.main_manager as mainUi
from PySide2.QtWidgets import *

# 최진철 test
# TODO : Oracle Home, Mysql Home, Embulk 환경변수 셋팅 (Home, Log 디렉토리)

def startOraConn(config) :
    conn = oraConn.startConn(config)
    if conn:
        print ('\n\n' + config.configItem['database'] + " Connected.")
    return conn

def main():
    os.putenv('NLS_LANG', '.UTF8')

    # Main Window 실행
    mainUi.exec()

    # mk_yml 파일 실행
    srcConfig, tgtConfig = mkYml.main()

    # SOURCE (oracle) DB 접속
    srcConn = startOraConn(srcConfig)
    
    # TODO: TARGET 접속 확인
    # TODO: type에 따라 oracle, mysql 접속 분기
    if tgtConfig.configItem['type'].upper() == 'ORACLE':
        tgtConn = startOraConn(tgtConfig)
    
    elif tgtConfig.configItem['type'].upper() == 'MYSQL':
        pass

    # SOURCE DB에서 이관 대상 테이블 정보 수집  
    # SOURCE DB CURSOR 생성
    srcCur = srcConn.cursor()


    # -- 테이블 정보
    
    # -- 파티션 정보 --> 트리 형태로 아래에 표시

    # ORACLE TO MYSQL 시 메타 변환

    # embulk 실행
    os.system("embulk")

    # 데이터 이관

    # 데이터 검증
    

if __name__ == "__main__":
    main()