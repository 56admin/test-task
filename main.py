import requests
import datetime
import time
import json
import sqlite3
import os



#Переменная окружения, которая отвечает за разрыв между запросами в секундах
sleep = os.environ['TIME']


#проверка на отрицательное число в переменной
if int(sleep) >= 1:

    while True:

        #в ДБ есть графа со временем, для того, чтоб было удобнее отслеживать курс
        #эта переменная берет и записывает время запроса в БД
        now = datetime.datetime.now()

        #Создаем/добавляем таблицу для RUB-USD в sqllite
        def add_rub_usd(urrency_usd):
            con = sqlite3.connect('db/db.db')
            coursore = con.cursor()
            coursore.execute('''CREATE TABLE IF NOT EXISTS Rub_Usd(rub TEXT, 
                                            usd TEXT, 
                                            timestamp DATE DEFAULT (datetime('now','localtime')))''')

            con.execute('''INSERT INTO Rub_Usd VALUES(?, ?, ?)''', urrency_usd)
            con.commit()

        #Создаем/добавляем таблицу для RUB-GBP в sqllite
        def add_rub_gbp(urrency_gbp):
            con = sqlite3.connect('db/db.db')
            coursore = con.cursor()
            coursore.execute('''CREATE TABLE IF NOT EXISTS Rub_Gbp(rub TEXT, 
                                            gbp TEXT, 
                                            timestamp DATE DEFAULT (datetime('now','localtime')))''')
            con.execute('''INSERT INTO Rub_Gbp VALUES(?, ?, ?)''', urrency_gbp)
            con.commit()

        #Получаем из запроса к сайту курс для нужных валют
        def getting(url,currency):
            url = requests.get(url)
            url = json.loads(url.text)
            return url['rates'][currency]

        #Присвоение переменных для валют
        rub = getting("http://api.openrates.io/latest?symbols=RUB,USD,GBP", 'RUB')
        gbp = getting("http://api.openrates.io/latest?symbols=RUB,USD,GBP", 'GBP')
        usd = getting("http://api.openrates.io/latest?symbols=RUB,USD,GBP", 'USD')

        #Данные для запись в БД
        end_rub_usd = rub, usd, now
        end_rub_gbp = rub, gbp, now

        #сама запись в БД
        add_rub_usd(end_rub_usd)
        add_rub_gbp(end_rub_gbp)

        #ожидание времени указанной в переменной для повторения цикла
        time.sleep(int(sleep))

else:
    print('Нужно не отрицательное число')



