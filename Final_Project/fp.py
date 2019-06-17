import re
import gensim
import logging
import pandas as pd
import random
import os
import nltk
import pymorphy2
import flask
#import urllib
from gensim.models import word2vec
from tqdm import tqdm
# from pymystem3 import Mystem
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize
# nltk.download('punkt')
from string import punctuation
from random import choice
from flask import Flask
from flask import render_template, request, url_for, redirect
morph = pymorphy2.MorphAnalyzer()


# работа с моделью (НКРЯ, 2015)


def w2v():
    # скачиваем модель
    # urllib.request.urlretrieve(
      #  "http://rusvectores.org/static/models/rusvectores2/ruscorpora_mystem_cbow_300_2_2015.bin.gz",
       # "ruscorpora_mystem_cbow_300_2_2015.bin.gz")
    m = r'ruscorpora_mystem_cbow_300_2_2015.bin.gz'
    if m.endswith('.vec.gz'):
        model = \
            gensim.models.KeyedVectors.load_word2vec_format(m, binary=False)
    elif m.endswith('.bin.gz'):
        model = \
            gensim.models.KeyedVectors.load_word2vec_format(m, binary=True)
    else:
        model = \
            gensim.models.KeyedVectors.load(m)
    return model

model = w2v()
# замена тэгов pymorphy2 на mystem
pymorphyVSmystem = {
    'NOUN': 'S',
    'ADJF': 'A',
    'ADJS': 'A',
    'COMP': 'A',
    'VERB': 'V',
    'INFN': 'V',
    'PRTF': 'V',
    'PRTS': 'V',
    'GRND': 'V',
    'PRED': 'V',
    'ADVB': 'ADV',
    'NUMR': 'NUM',
    'NPRO': 'SPRO',
    'CONJ': 'CONJ',
    'PRCL': 'PART',
    'PREP': 'P',
    'INTJ': 'INTJ'
    }

# inflections = ['case', 'number', 'person', 'tense', 'mood', 'voice']
# словарь категорий слова, по которым будет изменяться похожее слово


def inflections(word, pos):
    inflection = {}
#     существительное не изменяется по роду
    if pos != 'NOUN':
        inflection['gender'] = word.tag.gender
    else:
        pass
    if pos == 'VERB':
        # у глагола с тэгом 'perf' отсутствует форма настоящего времени
        if word.tag.aspect != 'perf':
            inflection['tense'] = word.tag.tense
        else:
            pass
    inflection['case'] = word.tag.case
    inflection['number'] = word.tag.number
    inflection['person'] = word.tag.person
    inflection['mood'] = word.tag.mood
    inflection['voice'] = word.tag.voice
    return inflection

# список текстов из папки с текстами


def files():
    filelist = []
    start_path = r'.\texts'
    for filename in os.listdir(start_path):
        filepath = os.path.join(start_path, filename)
        filelist.append(filepath)
    return filelist

# случайно выбираем текст, из которого берем фразу


def name():
    name = random.choice(files())
    return name

# эта функция создает словарь (d)
# автор (Мураками или Компьютер): [предложение, название произведения],
# предварительно выбрав случайное предложение из текста
# (для интереса длиной > 50 знаков)


def sentSplit():
    d = {}
    all_sent_list = []
    sent_book = []
    filename = name()
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.readlines()
    for line in text:
        title = re.search(r'([а-яА-Я]|\s)+?\n', line)
        author = re.search('Харуки Мураками', line)
        date = re.search('\d\n', line)
        if not author and not date and not title:
            all_sent_list.extend(sent_tokenize(line))
    sentence = random.choice(all_sent_list)
    while len(sentence) < 50:
        sentence = random.choice(all_sent_list)
    sent_book.append(sentence)
    r1 = re.search(r'texts\\(.+?)\.txt', filename)
    if r1:
        sent_book.append(r1.group(1))
    d['Мураками'] = sent_book
    return d

# эта функция разбивает исходную строку на символы, чтобы потом можно было
# вернуть исходную пунктуацию


def rawString(phrase):
    symbols = []
    wordlist = []
    r2 = re.findall('(\w+)(\s)?([^\w\s])?(\s)?', phrase)
    for item in r2:
        symbols.append(item)
    for w in symbols:
        for i in w:
            if i != '':
                wordlist.append(i)
    return(wordlist)

# эта функция оставляет из предыдущего списка символов только слова


def onlyWords(wordlist):
    words = []
    for w in wordlist:
        r3 = re.search(r'[А-Яа-я]+', w)
        if r3:
            if w not in punctuation:
                words.append(w)
    return words

# эта функция создает словарь (origin_model)
# оригинальное слово: слово из модели


def wMDict(words, model):
    origin_model = {}
    word_info = {}
    normal_pos_infl = {}
    sw = stopwords.words('russian')
    for item in words:
        if item.lower() not in sw:
            pos_infl = {}
            word = morph.parse(item)[0]
            normal = word.normal_form
            pos = word.tag.POS
            pos_infl['pos'] = pos
            pos_infl['infl'] = inflections(word, pos)
            normal_pos_infl[normal] = pos_infl
            word_info.update(normal_pos_infl)
            if pymorphyVSmystem[normal_pos_infl[normal]['pos']]:
                query = normal + '_' +\
                    pymorphyVSmystem[normal_pos_infl[normal]['pos']]
            else:
                pass
            if query in model:
                top5_similar = model.most_similar(positive=[query], topn=5)
                for word in top5_similar:
                    r4 = re.search('([а-я].+?)_(.+)', word[0])
                    if r4:
                        if r4.group(2) ==\
                              pymorphyVSmystem[normal_pos_infl[normal]['pos']]:
                            parsed = morph.parse(r4.group(1))[0]
                            inflection = word_info[normal]['infl'].values()
                            inflected = parsed.inflect({item for
                                                        item in inflection
                                                        if item is not None})
                            if inflected:
                                origin_model[item] = inflected.word
                                break
                            else:
                                origin_model[item] = item
                    else:
                        origin_model[item] = item
            else:
                origin_model[item] = item
    return origin_model


# меняем оригинальные слова на слова из модели, получаем строку,
# идентичную оригинальной, но со словами из модели


def wordChange(raw, origin_model):
    final = []
    for i in raw:
        try:
            final.append(origin_model[i])
        except:
            final.append(i)
    final[0] = final[0].capitalize()
    s = ''.join(final)
    return s


# эта функция создает словарь автор (компьютер): фраза, произведение
def comp():
    y = []
    d = sentSplit()
    phrase = d['Мураками'][0]
    raw = rawString(phrase)
    ow = onlyWords(raw)
    origin_model = wMDict(ow, model)
    changed = wordChange(raw, origin_model)
    y.append(changed)
    y.append(d['Мураками'][1])
    d['Компьютер'] = y
    del d['Мураками']
    return d

# список словарей автор: фраза, произведение,
# который будет использоваться в игре


def sentences():
    sent_list = []
    for i in range(0, 10):
        z = choice([sentSplit, comp])()
        sent_list.append(z)
    return sent_list


app = Flask(__name__)


@app.route('/')
def index():
    sent_list = sentences()
    flask.g = sent_list
    return render_template('index.html', sent_list=sent_list)


@app.route('/results')
def results():
    sent_list = flask.g
    answrs = []
    correct = 0
    if request.args:
        for item in sent_list:
            for key, value in item.items():
                a = {}
                answer = request.args[value[0]]
                if answer == key:
                    correct += 1
                a[answer] = value[0]
                answrs.append(a)
        return render_template('results.html', correct=correct,
                               rights=sent_list, users=answrs)
    return redirect(url_for('index'))


if __name__ == '__main__':
    import os
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
