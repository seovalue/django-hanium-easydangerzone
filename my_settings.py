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
