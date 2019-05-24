import csv
import re

<<<<<<< HEAD
words = []
glosses = []
with open('test1.csv', encoding='utf-8') as csvfile:
=======

words = []
glosses = []
with open('gloss.csv', encoding='utf-8') as csvfile:
>>>>>>> 1cdd5daf651822f8a068dfca004c78139f4bcf5c
    filereader = csv.reader(csvfile, delimiter='\t', quotechar='|')
    for row in filereader:
        for item in row:
            tr = re.search('([a-z]+?)', item)
            if tr:
                clean_item = item.strip(',.[]')
                words.append(clean_item)
            gloss = re.search('^\S\D[а-я]+?|[A-Z]+?', item)
            if gloss:
                glosses.append(item)
with open('final.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(zip(words, glosses))
<<<<<<< HEAD

##print(words)
##print(glosses)
=======
        
# print(words)
# print(glosses)
>>>>>>> 1cdd5daf651822f8a068dfca004c78139f4bcf5c
