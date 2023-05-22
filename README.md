<<<<<<< HEAD
# Embulk 
### # 구성
=======
# Embulk
## # 소스 구성
>>>>>>> e77cd63fc3c20be0ca661dbb66077a225a74a4c6
#### 1. conn
  - oracle, mysql 접속 관련 소스
  
#### 2. embulk_env
  - 현재 프로젝트의 가상환경 소스
  
#### 3. yml
  - mk_yml.py
    - 입력값에 따라 yml 파일 생성
    - 소스 설명
      1. yml 파일 생성할 경로 입력
<<<<<<< HEAD
      2. Source, Target DB 접속 정보 입력 -- config 변수에 저장함
      3. 입력한 정보가 맞는지 확인 용도로 출력
      4. 입력한 경로에 날짜 포맷으로 yml 파일 생성
      5. srcConfig, tgtConfig 입력 정보 리턴 
#### 4. main.py
  - 제일 먼저 실행되는 메인 소스
  - 현재 mk_yml.py 실행 후 conn/oracle.py 실행하는 순서로 되어있음
  - mk_yml.py 실행 시 입력받은 config 리턴값을 받음
  
=======
      2. Source, Target DB 접속 정보 입력
      3. 입력한 정보가 맞는지 확인 용도로 출력
      4. 입력한 경로에 날짜 포맷으로 yml 파일 생성
#### 4. main.py
  - 제일 먼저 실행되는 메인 소스
  - mk_yml.py 실행 후 conn/oracle.py 실행하는 순서로 되어있음
  
>>>>>>> e77cd63fc3c20be0ca661dbb66077a225a74a4c6
