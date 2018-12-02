##def answer(lang):
##    with open('langs.txt', 'r', encoding='utf-8') as f:
##        text = f.readlines()
##        for line in text:
##            r = re.search(lang.lower(), line)
##            if r:
                
## словарь ключ - язык, значение - код
import re
def dict_langs():
    with open('langs.txt', 'r', encoding='utf-8') as f:
        text = f.readlines()
        langs = {}
        for line in text:
            a = re.search('(.+?),(...)', line)
            if a:
                langs[a.group(1)] = a.group(2)
    return langs

def user_lang(lang, l):
    d = []
    for key, value in l.items():
        if lang == key:
            d.append(key)
            d.append(value)
        if key[0] == lang[0]:
            d.append(key)
            d.append(value)    
    print(d[0])
    print(d[1])
    for i in range (2, len(d)-1):
        print(d[i])

user_lang('японский', dict_langs())
            
            



##находит сокращение - вывод код языка - пердыдущая функция + печать языков на ту же букву
                





##import re
##
##def search(abbr, langs):
##    needed_langs = {}
##    for key, value in langs.items():
##        if abbr == value[len(abbr)-1]:
##            needed_langs[key] = value
##    print(needed_langs)
##
##search('j', dict_langs())
