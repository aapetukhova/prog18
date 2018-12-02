from flask import Flask
from flask import url_for, render_template, request, redirect
import csv
import os
import collections
import matplotlib
import matplotlib.pyplot as plt
import json
import seaborn
from matplotlib import style


def creating_csv():
    with open('results.csv', 'w+', encoding='utf-8') as f:
        f.write('name')
        f.write(';')
        f.write('age')
        f.write(';')
        f.write('sex')
        f.write(';')
        f.write('city')
        f.write(';')
        f.write('language')
        f.write(';')
        f.write('education')
        f.write(';')
        f.write('frs')
        f.write(';')
        f.write('cat')
        f.write(';')
        f.write('phe')
        f.write(';')
        f.write('new')
        f.write(';')
        f.write('rad')
        f.write(';')
        f.write('hyu')
        f.write('\n')


def creating_json():
    with open('file.json', 'w+', encoding='utf-8') as f:
        pass

creating_csv()
creating_json()


def plot(k):
    s = []
    n = 0
    X = []
    Y = []
    with open('results.csv', 'r', encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        row1 = next(filereader)
        xlabel = row1[k]
        for row in filereader:
            n += 1
            if row[k] != xlabel:
                s.append(row[k])
        counter = collections.Counter(s)
        for key, value in counter.items():
            X.append(key)
            Y.append(value)
    plt.subplot(3, 4, k)
    plt.scatter(X, Y)
    plt.title(xlabel)
    plt.xticks(X, rotation=90)
    plt.xlim(-0.5, len(X)-0.5)
    plt.ylim(0, n+0.5)
    plt.ylabel('NUM')


def query(k, language, education):
    s = []
    n = 0
    X = []
    Y = []
    with open('results.csv', 'r', encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        row1 = next(filereader)
        xlabel = row1[k]
        for row in filereader:
            if row[4] == language and row[5] == education:
                n += 1
                s.append(row[k])
        counter = collections.Counter(s)
        for key, value in counter.items():
            X.append(key)
            Y.append(value)
        plt.subplot(3, 4, k)
        plt.scatter(X, Y)
        plt.xticks(X, rotation=90)
        plt.title(xlabel)
        plt.xlim(-0.5, len(X)-0.5)
        plt.ylim(0, n+0.5)
        plt.ylabel('NUM')

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

        with open('results.csv', 'a', encoding='utf-8') as f:
            for i in range(0, len(s)):
                if i != len(s) - 1:
                    f.write(s[i])
                    f.write(';')
                else:
                    f.write(s[i])
                    f.write('\n')
    return render_template('index.html')


@app.route('/json')
def json():
    s = []
    with open('results.csv', 'r', encoding='utf-8') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        rows = list(filereader)
    with open('file.json', 'a', encoding='utf-8') as f:
        json.dump(rows, f)
    with open('file.json', 'r', encoding='utf-8') as f:
        for item in f:
            s.append(item)
    return render_template('json.html', s=s)


@app.route('/stats')
def stats():
    for i in range(1, 12):
        plot(i)
    plt.subplots_adjust(top=0.6, bottom=0.4, left=0.125, right=0.99,
                        hspace=0.2, wspace=0.35)
    plt.tight_layout()
    plt.savefig('./static/plot.png', orientation='landscape', dpi=450)
    return render_template('stats.html')


@app.route('/search')
def search():
    return render_template('search.html')


@app.route('/results')
def results():
    if request.args:
        language = request.args['language']
        education = request.args['education']
        if education == 'school':
            rEd = 'Неполное среднее'
        elif education == 'graduate':
            rEd = 'Среднее'
        elif education == 'bachelor':
            rEd = 'Высшее'
        for i in range(6, 11):
            query(i, language, education)
        plt.subplots_adjust(top=1, bottom=0, left=0.125, right=0.99,
                            hspace=0.2, wspace=0.35)
        plt.tight_layout()
        plt.savefig('./static/results.png', orientation='landscape', dpi=450)
        return render_template('results.html', language=language,
                               education=rEd)
    return redirect(url_for('search'))

if __name__ == '__main__':
    app.run(debug=True)
