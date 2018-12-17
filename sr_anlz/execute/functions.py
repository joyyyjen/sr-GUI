#!/usr/local/bin/python3
from metaphone import doublemetaphone
import nltk
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('stopwords')

#homoResult = open(os.path.join(PKG_DIR,"output","homoresult"),'w+')
''''
def homo_check(pair):
    #count = 0
    for pair in error_s:
        word1 = pair[1][0]
        word2 = pair[1][1]
        if doublemetaphone(word1) == doublemetaphone(word2):
            return "homo"
            #homoResult.write("{} {}\n".format(word1, word2))
            #count += 1
        else:
            if stem_check(word1, word2): 
                return "stem"
    #return count
'''


def homo_check(pair):
    word1 = pair[1][0]
    word2 = pair[1][1]
    if doublemetaphone(word1) == doublemetaphone(word2): return "homophone"
    elif stemlemma_check(word1, word2): return "inflection"
    elif simi_sound(word1, word2):
        if any(char.isdigit() for char in word1) or any(char.isdigit() for char in word2): return "number"
        else: return "quasi-homophone"
    else: return "None"
    #return count
def stemlemma_check(word1,word2):
    sno = SnowballStemmer('english')
    wnl = WordNetLemmatizer()
    if sno.stem(word1) == sno.stem(word2):
        #print(word1, word2)
        return True
    elif wnl.lemmatize(word1) == wnl.lemmatize(word2):
        return True

def simi_sound(word1,word2):
    phone1 = doublemetaphone(word1)[0]
    phone2 = doublemetaphone(word2)[0]

    pointer = len(phone1)
    phones = str(phone1)+str(phone2)
    #print(phone1, phone2,phones)
    for i in range(0,len(phones)):
        #print(i, pointer)

        if pointer < len(phones)-1:
            if phones[i] == phones[pointer]:
                pointer += 1
                continue
            else: break

        else:
            return True

def merge(pair):
    set1 = pair[0]
    set2 = pair[1]
    word1 = set1[1][0] #1
    word2 = set2[1][0] #3
    word3 = set2[1][1] #4
    result = homo_check(('S',(word1+word2, word3)))
    if word1+word2 == word3: return "merge"
    elif result != 'None': return "merge + " + result
    elif word1 + "-" + word2 == word3: return "merge"
    else: return "None"

def split(pair):
    set1 = pair[0]
    set2 = pair[1]
    word1 = set1[1][0]
    word2 = set1[1][1]
    word3 = set2[1][1]
    if word2+word3 == word1: return "split"
    elif ss_split(pair) != 'None': return ss_split(pair)
    else: return "None"

def ss_split(pair):
    set1 = pair[0]
    set2 = pair[1]
    token1 = set1[1][0] + set2[1][0]
    token2 = set1[1][1] + set2[1][1]
    new_pair = ('S',(token1,token2))
    result = homo_check(new_pair)
    if result != 'None':
        return "split + " + result
    else: return 'None'

def delete(pair):
    set1 = pair[0]
    set2 = pair[1]
    word1 = set1[1][0]
    word2 = set2[1][0]
    if word1 != word2 : return "distanced align"
    else: return "None"
def stopwords_missing(pair):
    stop_words = set(stopwords.words('english'))
    word1 = pair[1][0]
    word2 = pair[1][1]
    if (word1 in stop_words) or (word2 in stop_words):
        return "stop words missing"
    else: return 'None'

def type(name,pair):
    if name == 'S': result = homo_check(pair)
    elif name == 'SS': result = ss_split(pair)
    elif name == 'DS': result = merge(pair)
    elif name == 'SI': result = split(pair)
    elif name == 'DD': result = delete(pair)
    elif name == 'D' or name =='I': result = stopwords_missing(pair)
    else: result = "None"
    return result