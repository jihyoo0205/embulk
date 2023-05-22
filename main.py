import datetime as dt, os, sys
import yml.mk_yml as mkYml
import conn.oracle as oraConn
import conn.mysql as myConn
# TODO : Oracle Home, Mysql Home, Embulk 환경변수 셋팅 (Home, Log 디렉토리)

global oraHomePath
global myHomePath
global emHomePath

def main():
    os.putenv('NLS_LANG', '.UTF8')
    os.putenv('TNS_ADMIN', r'C:\app\client\product\19.0.0\client_1\network\admin')
    # Home 경로 테스트용으로 지정 -- 추후 입력 받는 방식으로 수정
    oraHomePath = r"/app/oracle/product/19c/dbhome_1"
    myHomePath = r"/app/mysql"
    emHomePath = r"C:\embulk"

    # mk_yml 파일 실행
    srcConfig, tgtConfig = mkYml.main()

    # SOURCE (oracle) DB 접속
    # TODO: type에 따라 oracle, mysql 접속 분기
    srcConn = oraConn.startConn(srcConfig)
    if srcConn:
        print ('\n\n' + srcConfig.dbName + " Connected.")

    # SOURCE DB에서 이관 대상 테이블 정보 수집  
    

    # ORACLE TO MYSQL 시 메타 변환

    # embulk 실행
    os.system("embulk")

    # 데이터 이관

    # 데이터 검증
    

if __name__ == "__main__":
    main()