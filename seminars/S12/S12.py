from flask import Flask
from flask import url_for, render_template, request, redirect
import sqlite3
import json


def creating_json():
    with open('file.json', 'w+', encoding='utf-8') as f:
        pass
    
##creating_json()


def tab(var):
    s = []
    X = []
    Y = []
    conn = sqlite3.connect('questionnaire.db')
    c = conn.cursor()
    c.execute('SELECT ? FROM questionnaire', var)
    data = c.fetchall()
    for item in data:
        s.append(item)
    counter = collections.Counter(s)
##    for key, value in counter.items():
##        X.append(key)
##        Y.append(value)    
    conn.commit()
    conn.close()
    return counter
    

    
app = Flask(__name__)


@app.route('/')
def index():
    s = []
    if request.args:
        s.append(request.args['name'])
        s.append(request.args['age'])
        s.append(request.args['sex'])
        s.append(request.args['city'].capitalize())
        s.append(request.args['language'])
        s.append(request.args['education'])

        s.append(request.args['frs'])
        s.append(request.args['cat'])
        s.append(request.args['phe'])
        s.append(request.args['new'])
        s.append(request.args['rad'])
        s.append(request.args['hyu'])
# подключаемся к базе данных
        conn = sqlite3.connect('questionnaire.db')

# создаем объект "курсор", которому будем передавать запросы
        c = conn.cursor()

# создаем таблицу
        c.execute("CREATE TABLE IF NOT EXISTS questionnaire (name text, age integer, sex text, city text, language text, education text, forsatz text, catalogue text, phenomenon text, newton text, radja text, hyundai text)")
        

# вставляем строку
        c.execute("INSERT INTO questionnaire VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11]))

# сохраняем изменения
        conn.commit()

# отключаемся от БД
        conn.close()       


    return render_template('index.html')



@app.route('/json')
def json():
    conn = sqlite3.connect('questionnaire.db')
    c = conn.cursor()
    c.execute('SELECT * FROM questionnaire')
    s = c.fetchall()
    conn.commit()
    conn.close() 
    return render_template('json.html', s=s)


@app.route('/stats')
def stats():
    a = []
    b = []
    s = ['age', 'sex', 'city', 'language', 'education', 'forsatz', 'catalogue', 'phenomenon', 'newton', 'radja', 'hyundai']
    for item in s:
        d = tab(item)
        a.append(tab(item))

    return render_template('stats.html', a=a)


if __name__ == '__main__':
    app.run(debug=True)

    
