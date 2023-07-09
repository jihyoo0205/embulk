## 소스 설명
<<<<<<< HEAD
- 최종 수정 : 2023.06.14
=======
>>>>>>> 71f24865ade72446fcbad4c49565849bdb542b10

#### 1. conn
  - oracle, mysql 접속 관련 소스
  - oracle.py
    - user명에 따라 SYSDBA 모드 구분해서 접속
  - mysql.py
  
#### 2. env
  - 현재 프로젝트의 가상환경 소스
  - 사용한 라이브러리 경로
    - Lib\site-packages
  - jdbc driver 경로
    - Lib\ojdbc8.jar
  
#### 3. yml
  - mk_yml.py
<<<<<<< HEAD
    - root경로\files\yml 경로에 생성
    - 입력한 이관 대상 테이블 개수만큼 스키마명.테이블명_YYYYMMDD.yml 형태로 생성
    - Source, Target DB 접속 정보 입력 -- YmlConfig 클래스 형태로 변수에 저장
    - srcConfig, tgtConfig 변수명으로 입력 정보 리턴 
=======
    1. root경로\files\yml 경로에 생성
    2. 입력한 이관 대상 테이블 개수만큼 스키마명.테이블명_YYYYMMDD.yml 형태로 생성
    3. Source, Target DB 접속 정보 입력 -- YmlConfig 클래스 형태로 변수에 저장
    4. srcConfig, tgtConfig 변수명으로 입력 정보 리턴 
>>>>>>> 71f24865ade72446fcbad4c49565849bdb542b10
   
#### 4. main.py
  - 제일 먼저 실행되는 메인 소스
  - 실행 순서
    - mk_yml.py 실행하여 yml 파일 생성
    - conn/oracle.py 실행 : source 정보대로 oracle 접속
<<<<<<< HEAD
    - 까지만 테스트함.. 이후는 작성 중임
=======
>>>>>>> 71f24865ade72446fcbad4c49565849bdb542b10
