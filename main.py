import datetime as dt, os, sys
import yml.mk_yml as mkYml
# TODO : Embulk 환경변수 셋팅 (Home, Log 디렉토리)


def main():
    # YML 파일 생성
    # -- 1. yml 파일 생성할 경로 입력
    # -- 2. 날짜_시간.yml 포맷으로 생성
    ymlPath = input("Input the path to create the yml file : ")
    
    date = dt.datetime.now()
    ymlPath += '\\' + date.strftime("%Y%m%d_%H%M%S") + '.yml'
    print('Path to the created file : ' + ymlPath)
    
    # -- 파일에 데이터 입력
    f = open(ymlPath, 'w')
    # -- mk_yml 파일 실행
    srcYmlConfig, tgtYmlConfig = mkYml.main()

    # -- 입력 정보 출력
    print('')
    print('*********************************************************')
    print('Check Source Database Infomation')
    print('*********************************************************')
    print(f'type: {srcYmlConfig.type}')
    print(f'driverPath: {srcYmlConfig.driverPath}')
    print(f'host: {srcYmlConfig.host}')
    print(f'port: {srcYmlConfig.port}')
    print(f'tnsPath: {srcYmlConfig.tnsPath}')
    print(f'tnsName: {srcYmlConfig.tnsName}')
    print(f'dbName: {srcYmlConfig.db}')
    print(f'user: {srcYmlConfig.user}')
    print(f'pw: {srcYmlConfig.pw}')
    print('')
    print('*********************************************************')
    print('Check Target Database Infomation')
    print('*********************************************************')
    print(f'type: {tgtYmlConfig.type}')
    print(f'driverPath: {tgtYmlConfig.driverPath}')
    print(f'host: {tgtYmlConfig.host}')
    print(f'port: {tgtYmlConfig.port}')
    print(f'tnsPath: {tgtYmlConfig.tnsPath}')
    print(f'tnsName: {tgtYmlConfig.tnsName}')
    print(f'dbName: {tgtYmlConfig.db}')
    print(f'user: {tgtYmlConfig.user}')
    print(f'pw: {tgtYmlConfig.pw}')
    print('')

    # -- yml 파일에 저장 - SOURCE DB INFORMATION 
    f.write(f'in:\n')
    f.write(f'type: {srcYmlConfig.type}\n')
    f.write(f'driver_path: {srcYmlConfig.driverPath}\n')
    f.write(f'tns_admin_path: {srcYmlConfig.tnsPath}\n')
    f.write(f'net_service_name: {srcYmlConfig.tnsName}\n')
    f.write(f'host: {srcYmlConfig.host}\n')
    f.write(f'port: {srcYmlConfig.port}\n')
    f.write(f'database: {srcYmlConfig.db}\n')
    f.write(f'user: {srcYmlConfig.user}\n')
    f.write(f'password: {srcYmlConfig.pw}\n')

    # -- yml 파일에 저장 - TARGET DB INFORMATION 
    f.write(f'\nout:\n')
    f.write(f'type: {tgtYmlConfig.type}\n')
    f.write(f'host: {tgtYmlConfig.host}\n')
    f.write(f'port: {tgtYmlConfig.port}\n')
    f.write(f'database: {tgtYmlConfig.db}\n')
    f.write(f'user: {tgtYmlConfig.user}\n')
    f.write(f'password: {tgtYmlConfig.pw}\n')
    
    f.close()

if __name__ == "__main__":
    main()