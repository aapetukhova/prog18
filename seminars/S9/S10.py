from flask import Flask
from flask import url_for, render_template, request, redirect
import re


app = Flask(__name__)

@app.route('/')
def lang_list():
    with open('langs.txt', 'r', encoding='utf-8') as f:
        content = f.read().split('\n')
    return render_template('index.html', content=content)


def dict_langs():
    with open('langs.txt', 'r', encoding='utf-8') as f:
        text = f.readlines()
        langs = {}
        for line in text:
            a = re.search('(.+?),(...)', line)
            if a:
                langs[a.group(1)] = a.group(2)
    return langs

def search(abbr, langs):
    needed_langs = {}
    for key, value in langs.items():
        if abbr == value[len(abbr)-1]:
            needed_langs[key] = value
    return needed_langs

##@app.route('/langs/<abbr>')
##def lang_letters(abbr):
##    return render_template('search.html', content=search(abbr))

@app.route('/langs/<abbr>')
def lang_letters(abbr):
    index_url = {'main page': url_for('lang_list')}
    return render_template('search.html', lang_dict=search(abbr, dict_langs()), index_url=index_url)

#если язык соответствует ключу, вывод "язык:" - ключ, "код" - значение, подсловарь из языков на ту же букву



@app.route('/form')
def form():
    if request.args:
        lang = request.args['lang']
        
        return render_template('answer.html', lang=lang)
    else:
        
    return render_template('form.html')

@app.route('/not_found')
def not_found():
    return 'Unfortunately, there is no such language'


if __name__ == '__main__':
    app.run(debug=True)
