import csv
import re

words = [] #list of words
glosses = [] #list of glosses
with open('file2007.csv', encoding='utf-8') as csvfile: #reading the initial file
    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|') #divide words by a tab
    for row in filereader:
        for item in row: #for every item=word
            tr = re.search('[a-züχʕšč]+?', item)#if it's written with latin letters it's our case
            if tr:
                clean_item = item.strip(',.[]{}""?! ') #cleaning the item from punctuation and spaces
                words.append(clean_item) #list of words
            gloss = re.search('^(\S)?([A-Z]+|[а-яА-Я]+|\[\d|\d-|\d=|\?|\[\{)', item) #search for the glosses - they are kept at the same 'number' as words, so we create the pair word-gloss only by the order of their appearance: including 1-letter words, [word], number-gloss, ?? as a gloss, [number]
            if gloss:
                glosses.append(item.strip())
with open('final.csv', 'w', encoding='utf-8') as f: #opening the final result file
    writer = csv.writer(f)
    writer.writerows(zip(words, glosses)) #we create the pair word-gloss usinf lists
