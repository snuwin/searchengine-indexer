import json
import math
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
def retrievesearch(words: list[str]) -> dict:
    with open('Indexes.json', 'r') as file:
        data = json.load(file)
        retlist = []
        retlist2 = []
        retdict = {}
        similarityarr, webpages = createidfarr(words, data)
        retlist.append(compute_cosine_similarity_scores(similarityarr))
        for x in range(0, len(retlist[0])):
            retlist2.append(0)
            for y in range(0, len(retlist)):
                retlist2[x] += retlist[y][x]
        for x in range(0, len(retlist2)):
            retdict[webpages[x]] = retlist2[x]
        retval = sorted(retdict.items(), key=lambda x:x[1], reverse = True)
        return retval


    
def createidfarr(terms, data) -> list:
    with open('tfidf.json', 'r') as file:
        retval = []
        tffile = json.load(file)
        doclist = []
        docs = defaultdict(int)
        for x in terms:
            if x not in data:
                continue
            for y in data[x]:
                doclist.append(y)
                if x in tffile[y]:
                    docs[y] += tffile[y][x]
        doclist.sort(reverse = True, key = lambda x: docs[x])
        doclist = doclist[:50]
        w = docs[doclist[0]]
        s = docs[doclist[10]]
        termlist = set()
        for x in data:
            for y in doclist:
                if y in data[x]:
                    termlist.add(x)
                    break
        array = []
        for doc in doclist:
            for term in termlist:
                n = tffile[doc]
                if term not in tffile[doc]:
                    array.append(float(0.0))
                else:
                    array.append(float(tffile[doc][term]))
            retval.append(np.array(array))
            array = []
        return retval, doclist

def getwebpages(term, data):
        doclist = [x for x in data[term]]
        return doclist
def tfidfscore(N: int, tf: int, df: int):
    return tf * math.log(N / df)

def compute_cosine_similarity_scores(tfidf_pages):
    summed_similarity_scores = []
    for i in range(len(tfidf_pages)):
        similarity_sum = 0
        for j in range(len(tfidf_pages)):
            similarity_sum += cosine_similarity(tfidf_pages[i].reshape(1, -1), tfidf_pages[j].reshape(1, -1))[0][0]
        summed_similarity_scores.append(similarity_sum)
    return summed_similarity_scores


if __name__ == '__main__':
    print(retrievesearch(["test"]))