# MistyBIT-LCT-4

<a href="http://188.72.108.76/auth/login">Ссылка на решение</a> 

<a href="https://web.telegram.org/k/#@branchlessEmployeeBot">Ссылка на телеграм бота</a> 

<a href="https://hub.docker.com/repository/docker/vaynbaum/task-hack/general">Ссылка на репозиторий на DockerHub</a> 

Для развертывания системы необходимо скачать проект, заменить в `*.env` файлах значения ****** на переменные 
1. пароль для mailer'а (внешних, сторонних приложений, не как на почте) и логин (от почты) для отправки сообщений)  (в mail.env)
2. SECRET_STRING для jwt токенов, команда в linix, bash:
   
> $ openssl rand -hex 32 (в .env в /api)
> 
3. YANDEX_KEY_API_LOC для яндекс геокодирования (в .env в /api)
4. TOKEN для тг-бота (в файле config.py в /bot)
5. API_KEY для яндекс-карты (в файлах environments/environment.prod.ts и environments/environment.ts в /front/src/environments)

и ввести команду 
> docker compose up

(две версии docker-compose.yml файлов - одна собирает проект из исходников, другая из образов с DockerHub)

### Письма на почту могут попадать в СПАМ
