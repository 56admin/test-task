FROM python:3
#Переменная для указания разрыва между запросами в секундах
ENV TIME='3'
#рабочая директория
WORKDIR /app
ADD main.py requirements.txt /app
RUN python3 -m venv env
CMD 'source' 'env/bin/activate'
RUN pip3 install -r requirements.txt
#создаю точку монтирования для базы данных
VOLUME /app/db
#запускаю пайтон-скрипт
ENTRYPOINT python3 'main.py'
