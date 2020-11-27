# EasyDangerzone

<!-- ABOUT THE PROJECT -->
## 📢 About The Project
사용한 오픈소스 프로젝트: [dangerzone](https://github.com/firstlookmedia/dangerzone)  
OS 및 여러 가지에 의존성이 높은 dangerzone 프로그램을 쉽게 사용할 수 있도록 확장 개발하자는 취지로 고안된 프로젝트입니다.  

## 🎬 실행 동영상 
[실행 동영상 확인하기]( ./video)  

## 🔧 기능 목록
1. 웹에 파일을 업로드 하면, 서버에서 dangerzone 을 거친 바이러스 없는 안전한 파일을 사용자에게 전달   
2. 사용자에게 전달될 때에는 Virustotal API를 거친 결과와 URLhaus의 md5 해시키를 비교한 결과를 함께 알 수 있는 페이지 제작   
3. Dashboard를 통해 파일 변환 추이 및 사용자 추이 확인 가능  
4. Feedback 및 문의사항을 Contact에서 전송 가능  

현재 지원 가능한 파일 타입 목록:  
* PDF(`.pdf`)
* WORD(`.docx`,`.doc`)
* EXCEL(`.xlsx`,`.xls`)
* PPT(`.pptx`,`.ppt`)
* ODF(`.odt`,`.ods`,`.odp`,`.ods`)
* JPEG(`.jpg`,`.jpeg`)
* GIF(`.gif`)
* PNG(`.png`)
* TIFF(`.tif`,`.tiff`)


<!-- GETTING STARTED -->
## 💻 Getting Started
for ubuntu 18.04 LTS:
```
#!/bin/bash

#echo 'ubuntu:korea123!!' | chpasswd
sudo -S sh -c 'echo "ubuntu:korea123!!" | chpasswd'

echo "deb https://packagecloud.io/firstlookmedia/code/ubuntu/ bionic main" | sudo tee -a /etc/apt/sources.list.d/firstlookmedia_code.list
curl -L https://packagecloud.io/firstlookmedia/code/gpgkey | sudo apt-key add -

sudo apt-get update
# sudo apt-get install -y ubuntu-desktop xrdp curl gnupg apt-transport-https dangerzone python3 python3-pip
sudo apt-get install -y curl gnupg apt-transport-https dangerzone python3 python3-pip

pip3 install django>=2.0
mkdir -p /tmp/dangerzone-pixel
mkdir -p /tmp/dangerzone-safe

sudo usermod -aG docker ubuntu
sudo chmod 666 /var/run/docker.sock
sudo systemctl daemon-reload
sudo systemctl start docker
sudo systemctl enable docker
/usr/bin/docker pull flmcode/dangerzone
```

for python3:
```
pip install -r requirements.txt
```

위 요구사항을 모두 설치한 뒤, manage.py가 있는 폴더로 이동합니다.  

for customize:
```
my_settings.py

# 데이터베이스의 정보를 작성합니다.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME' : '데이터베이스 명',
        'USER': '유저이름',
        'PASSWORD':'패스워드',
        'HOST':'localhost',
        'PORT':'3306',
        'OPTIONS':{
            'init_command':'SET sql_mode="STRICT_TRANS_TABLES"'
        }
    }
}

```  
```
secrets.json

# 각종 private key들을 작성합니다.
{
  "API_KEY": "Virustotal API KEY",
  "SECRET_KEY" :"장고 SECRET KEY",
  "WEBHOOK_KEY": "슬랙 WEBHOOK KEY"
}
```


for Run program:
```
python3 manage.py runserver
or
python manage.py runserver
```

# 💡 UPDATE LIST
### ~11.27
* ubuntu에서 MySQL DB 연동  
* 에러 발생하는 부분 try~catch로 처리  

### ~10.19
* urlhash 이용 md5 해시키로 악성파일인지 확인
* MySQL DB 연동
* 폴더 구조 전면 수정 및 MVC 패턴 

### ~9.2
* 파일 업로드 시, 첫번째로 2page 파일, 두번째로 1page 파일을 업로드 하면 첫번째 파일의 두번째 페이지가 같이 merge되서 나오는 오류를 발견함 --> dangerzone-pixel 내부의 width, height, rgb를 매번 변환 시 지우고 새로 업데이트하도록 변경  
* 지원 불가능한 확장자를 업로드하여 실행하면 내부에서 에러를 발생시켜 페이지 자체에 에러가 보여지는 오류 --> 확장자에 대한 조건을 걸어 지원 불가능한 확장자 파일을 선택 시 불가능하다는 alert를 띄우도록 변경

### ~9.10
* virustotal api json to table  
* link contact page to slack   
* modify handling file about dashboard   
