#!/usr/local/bin/python3
import sr_anlz.execute.word_error as word_error
from collections import Counter
import sr_anlz.execute.functions as functions
import os
from sr_anlz.definition import PKG_DIR

output_path = os.path.join(PKG_DIR, "output", "ErrorFreqResult.txt")

freqResult = open(output_path, 'w+')

freqDict = {}
# outputResult = open('../output/train.txt','w+')

def editonly(sents):
    bow = []
    for sent in sents:
        for word in sent:
            bow.append(word[0])
    return bow


def n_gram(bow, n):
    N_Gram = [tuple(bow[i:i + n]) for i in range(len(bow) - n + 1)]
    # print(len(N_Gram))
    # print(N_Gram)
    frequency = []
    freq = Counter(N_Gram)
    list1 = freq.most_common()
    print(list1)
    I_total = 0
    S_total = 0
    D_total = 0
    for list2 in list1:
        if 'N' not in str(list2):
            if 'E' in str(list2) and str(list2).count('E') == 2:
                frequency.append((list2[0], round(list2[1] / len(N_Gram), 3)))
            elif 'E' in str(list2) and 'I' in str(list2):
                I_total = I_total + list2[1]
            elif 'E' in str(list2) and 'S' in str(list2):
                S_total = S_total + list2[1]
            elif 'E' in str(list2) and 'D' in str(list2):
                D_total = D_total + list2[1]
            else:
                frequency.append((list2[0], round(list2[1] / len(N_Gram), 3)))
    frequency.append((('I'), round(I_total / len(N_Gram), 3)))
    frequency.append((('S'), round(S_total / len(N_Gram), 3)))
    frequency.append((('D'), round(D_total / len(N_Gram), 3)))

    return (frequency)


def n_gram_set(sents, n):

    # print(bow[1])
    N_Gram = list()
    for sent in sents:
        for i in range(len(sent) - n + 1):
            N_Gram.append(tuple(sent[i:i + n]))

    error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD = [], [], [], [], [], [], []
    error_I = []
    error_D = []
    error_S = []

    k = 0
    for j in N_Gram:
        # print(j[0][0],j[1][0])

        if j[0][0] == 'S' and j[1][0] == 'S':
            error_SS.append(j)
        elif j[0][0] == 'I' and j[1][0] == 'I':
            error_II.append(j)
        elif [0][0] == 'I' and j[1][0] == 'S':
            error_IS.append(j)
        elif j[0][0] == 'S' and j[1][0] == 'I':
            error_SI.append(j)
        elif j[0][0] == 'S' and j[1][0] == 'D':
            error_SD.append(j)
        elif j[0][0] == 'D' and j[1][0] == 'S':
            error_DS.append(j)
        elif j[0][0] == 'D' and j[1][0] == 'D':
            error_DD.append(j)
        elif (j[0][0] == 'N' and j[1][0] == 'S') or (j[0][0] == 'E' and j[1][0] == 'S'):
            if k < len(N_Gram):
                if N_Gram[k + 1][0] == j[1] and N_Gram[k + 1][1][0] == 'E':
                    # print(N_Gram[k+1],j[1])
                    error_S.append(j[1])
        elif j[0][0] == 'S' and j[1][0] == 'N':
            if N_Gram[k - 1][0][0] == 'E':
                error_S.append(j[1])
        elif (j[0][0] == 'E' and j[1][0] == 'D') or (j[0][0] == 'N' and j[1][0] == 'D'):
            if k < len(N_Gram):
                if N_Gram[k + 1][0] == j[1] and N_Gram[k + 1][1][0] == 'E':
                    error_D.append(j[1])
        elif (j[0][0] == 'E' and j[1][0] == 'I') or (j[0][0] == 'N' and j[1][0] == 'I'):
            if k < len(N_Gram):
                if N_Gram[k + 1][0] == j[1] and N_Gram[k + 1][1][0] == 'E':
                    error_I.append(j[1])
        k = k + 1

    print("====Error Freq ====")
    print(error_D)
    sumE = len(error_SS) + len(error_SD) + len(error_DS) + len(error_II) + len(error_IS) + len(error_SI) + len(
        error_DD) + len(error_I) + len(error_D) + len(error_S)
    print(sumE / len(N_Gram))
    global freqDict
    freqDict["WER"] = [sumE,sumE / len(N_Gram)]



    return (error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD, error_I, error_D, error_S)
    # print("SS: {}\nSD: {}\nDS: {}\nII: {}\nIS: {}\nSI: {}\nDD: {}\nI: {}\nD: {}\nS: {}\n".format(error_SS,error_SD,error_DS,error_II,error_IS,error_SI,error_DD,error_I,error_D,error_S))


def format_print(freqs, error):
    error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD, error_I, error_D, error_S = error



    for freq in freqs:
        if freq[0] == ('S', 'S'):
            # print("(S,S) : {}=================".format(freq[1]))
            freqResult.write("(S,S) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_SS), freq[1]]
            for errori in error_SS:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == ('S', 'D'):
            # print("(S,D) : {} =================".format(freq[1]))
            freqResult.write("(S,D) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_SD), freq[1]]
            for errori in error_SD:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == ('D', 'S'):
            error_list = []
            # print("(D,S) : {} =================".format(freq[1]))
            freqResult.write("(D,S) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_DS), freq[1]]
            for errori in error_DS:
                error_type = functions.merge(errori)
                if error_type == "None": error_type = ""
                else: error_list.append(error_type)
                freqResult.write("{}\t{}\n".format(errori, error_type))
                # outputResult.write("DS\t{}\t{}\t{}\t{}\t{}\n".format(errori[0][1][0], errori[0][1][1],errori[1][1][0],errori[1][1][1], error_type))
            for i in set(error_list):
                freqDict[freq[0]].append((i,error_list.count(i)))
            freqResult.write('\n')
        elif freq[0] == ('I', 'I'):
            # print("(I,I) : {} =================".format(freq[1]))
            freqResult.write("(I,I) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_II), freq[1]]
            for errori in error_II:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == ('I', 'S'):
            # print("(I,S) : {} =================".format(freq[1]))
            freqResult.write("(I,S) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_IS), freq[1]]
            for errori in error_IS:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == ('S', 'I'):
            error_list = []
            # print("(S,I) : {} =================".format(freq[1]))
            freqResult.write("(S,I) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_SI), freq[1]]
            for errori in error_SI:
                # print(errori)
                error_type = functions.split(errori)
                if error_type == "None": error_type = ""
                else:
                    error_list.append(error_type)
                freqResult.write("{}\t{}\n".format(errori, error_type))
                # outputResult.write("SI\t{}\t{}\t{}\t{}\t{}\n".format(errori[0][1][0], errori[0][1][1],errori[1][1][0],errori[1][1][1], error_type))
            for i in set(error_list):
                freqDict[freq[0]].append((i,error_list.count(i)))
            freqResult.write('\n')
        elif freq[0] == ('D', 'D'):
            # print("(D,D) : {} =================".format(freq[1]))
            freqResult.write("(D,D) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_DD), freq[1]]
            for errori in error_DD:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == 'I':
            # print("(I) : {} =================".format(freq[1]))
            freqResult.write("(I) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_I), freq[1]]
            for errori in error_I:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == 'D':
            # print("(D) : {} =================".format(freq[1]))
            freqResult.write("(D) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_D), freq[1]]
            for errori in error_D:
                # print(errori)
                freqResult.write(str(errori) + '\n')
            freqResult.write('\n')
        elif freq[0] == 'S':
            error_list = []
            # print("(S) : {} =================".format(freq[1]))
            freqResult.write("(S) : {} =================\n".format(freq[1]))
            freqDict[freq[0]] = [len(error_S), freq[1]]
            for errori in error_S:
                # print(errori)
                error_type = functions.homo_check(errori)
                if error_type == "None": error_type = ""
                else:
                    error_list.append(error_type)
                freqResult.write("{}\t{}\n".format(errori, error_type))
                # outputResult.write("S\t{}\t{}\t' '\t' '\t{}\n".format(errori[1][0], errori[1][1], error_type))
            for i in set(error_list):
                freqDict[freq[0]].append((i,error_list.count(i)))
            freqResult.write('\n')
            error_type = ""
    return freqDict



def main_freq():

    test = open(os.path.join(PKG_DIR, "output", "recognition.txt"), 'r')
    sol = open(os.path.join(PKG_DIR, "refined-audio", "trans.txt"), 'r')
    test_string = test.readlines()
    sol_string = sol.readlines()
    # print(len(sol_string))
    sum = 0
    sents = []
    for i in range(len(sol_string)):
        sol_word = sol_string[i].strip("\n").lower().split()
        sum = sum + len(sol_word)
        test_word = test_string[i].strip("\n").lower().split()
        sents.append(word_error.wer(sol_word, test_word))

    bow = editonly(sents)
    frequency = n_gram(bow, 2)
    frequency_sort = sorted(frequency, key=lambda x: x[1], reverse=True)
    error = n_gram_set(sents, 2)
    freqDict1 = format_print(frequency_sort, error)

    test.close()
    sol.close()
    freqResult.close()

    return output_path, freqDict1
