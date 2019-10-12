#waste

##환경설정 후 실행법

1. 저장소를 clone
2. 저장소 위치로 터미널 이동 cd

3. venv 설치 및 venv 환경으로 설정
pip install virtualenv

가상환경 venv 폴더 생성
virtualenv venv

venv로 환경 설정
-linux: source venv/bin/activate
-window: call venv/Scripts/activate

4. 패키지 환경을 맞춤(설치) 
pip install -r requirements.txt

5. 실행
python manage.py runserver
