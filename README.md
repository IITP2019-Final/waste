#waste

##환경설정 후 실행법

1. 저장소를 clone
2. 저장소 위치로 터미널 이동 cd
3. 가상환경 패키지 설치
- pip install virtualenv
4.가상환경 venv 폴더 생성
- virtualenv venv
5. venv로 환경 설정
- linux: source venv/bin/activate
- window: call venv/Scripts/activate
6. 패키지 환경을 맞춤(설치) 
pip install -r requirements.txt
7. 실행
python manage.py runserver
