import sqlite3
import csv
import re
from pymystem3 import Mystem
from flask import Flask
from flask import url_for, render_template, request, redirect


# база данных
# названия статей, тексты  Plain, mystem-тексты, ссылки на статьи


def data():
    # назовем БД 'data.db'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS \
                articles(name text, plain text, mystem text, link text)')
#   большой словарь из маленьких словарей, ключ - номер словаря,
#   значение - маленький словарь
    D = {}
#   счетчик
    n = 0
#   берем данные из таблицы метаданных (в папке с корпусом статей 'YV')
    with open(r'.\YV\metadata.csv', 'r', encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter='\t')
        for row in filereader:
            d = {}
            n += 1
#           путь к тексту plain
            d['plain_path'] = row[0]
            with open(d['plain_path'], 'r', encoding='utf-8') as f:
                text = f.readlines()
#               сам текст
                d['plain'] = (''.join(text[5:]))
#           название статьи
            d['name'] = row[2]
#           ссылка к статье
            d['link'] = row[10]
#           путь к тексту mystem
            d['mystem_path'] = d['plain_path'].replace('plain', 'mystem-plain')
            with open(d['mystem_path'], 'r', encoding='utf-8') as f:
                # сам текст
                d['mystem'] = f.read()
            D[n] = d
    for key, value in D.items():
        c.execute('INSERT INTO articles VALUES (?, ?, ?, ?)',
                  (D[key]['name'], D[key]['plain'],
                   D[key]['mystem'], D[key]['link']))
    conn.commit()
    conn.close()


# функция поиска лемматизированного запроса в лемматизированном тексте


def query_in_text(query):
    symbols = '(),"'''
    m = Mystem()
    lemmas = m.lemmatize(query)
    s = len(lemmas)
#   список ссылок на статьи
    links = []
#   регулярное выражение, которое поможет в поиске слова/фразы
    k = ''
    for i in range(0, s):
        if lemmas[i] != '\n' and lemmas[i] != ' ':
            k += lemmas[i] + '=' + '.+?'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    #   выберем все mуstem-тексты
    c.execute('SELECT mystem FROM articles')
    a = c.fetchall()
    for item in a:
        # отдельный mуstem-текст
        b = ''.join(str(item))
        r = re.search(k, b)
#       если регулярное выражение в тексте, вытаскиваем ссылку статьи
        if r:
            c.execute('SELECT link FROM articles WHERE mystem=?', item)
            e = str(c.fetchone()).strip(symbols).strip("''")
            if e not in links:
                links.append(e)
    conn.commit()
    conn.close()
    return links

# поисковик


app = Flask(__name__)

# страница поиска


@app.route('/')
def search():
    return render_template('search.html')

# страница результатов


@app.route('/results')
def results():
    if request.args:
        query = request.args['query']
        links = query_in_text(query)
        return render_template('results.html', query=query, links=links)
    return redirect(url_for('search'))


if __name__ == '__main__':
    data()
    app.run(debug=True)
