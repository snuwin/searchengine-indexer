import os
import nltk
import json
import collections
import retrieve

from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
from collections import defaultdict

stop_words = [
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 
    'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 
    'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 
    'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 
    'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", 
    "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 
    'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', 
    "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 
    'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 
    'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 
    'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 
    'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", 
    "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 
    'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 
    'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 
    'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", 
    "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'
]

tokenIndex = dict()

tagmap = defaultdict(lambda: 1)
tagmap['h1'] = 5
tagmap['h2'] = 4
tagmap['h3'] = 3
tagmap['h4'] = 3
tagmap['b'] = 3
tagmap['h5'] = 2
tagmap['h6'] = 2

def indexer():
    documentnum = 0
    with open("WEBPAGES_RAW\\bookkeeping.json", "r") as file:
        data = json.load(file)
        for key, value in data.items():
            keys = key.split('/')
            try:
                with open(f"WEBPAGES_RAW\\{keys[0]}/{keys[1]}") as f:
                    print(f"WEBPAGES_RAW/{keys[0]}/{keys[1]}")
                    documentnum += 1
                    content = f.read()
                    soup = BeautifulSoup(content, 'lxml')

                    for tag in soup.find_all(['html', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'b']):
                        text = tag.get_text().strip()
                        tokendict = defaultdict(int)
                        total = 0
                        for x in text.split():
                            if x.isalpha() and x not in stop_words:
                                total += 1
                                tokendict[WordNetLemmatizer().lemmatize(x).lower()] += 1
                        for token in tokendict.keys():
                            if token not in tokenIndex:
                                test2 = defaultdict(int)
                                test2[key] = 0
                                tokenIndex[token] = test2
                                tokenIndex[token][key] += tokendict[token]
                            else:
                                if key not in tokenIndex[token]:
                                    tokenIndex[token][key] += tokendict[token]
                                else:
                                    tokenIndex[token][key] += tokendict[token]
            except:
                pass

    with open(f'Indexes.json', 'w') as file:
        json.dump(tokenIndex, file)

def getnum(data):
    retval = 0
    for x in data.keys():
        retval += data[x]
    return retval

def getfreq(data, page, total):
    return data[page] / total

def addtfidf():
    retval = defaultdict(list)
    with open("Indexes.json", "r") as file:
        data = json.load(file)
        for term in data.keys():
            total = getnum(data[term])
            for page in data[term]:
                if page not in retval:
                    test2 = defaultdict(int)
                    test2[term] = 0
                    retval[page] = test2
                    retval[page][term] = retrieve.tfidfscore(len(data), getfreq(data[term], page, total), len(data[term]))
                else:
                    retval[page][term] = retrieve.tfidfscore(len(data), getfreq(data[term], page, total), len(data[term]))
    with open(f'tfidf.json', 'w') as file:
        json.dump(retval, file)
indexer()
addtfidf()