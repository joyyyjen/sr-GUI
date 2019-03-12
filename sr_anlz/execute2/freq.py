#!/usr/local/bin/python3
from sr_anlz.definition import PKG_DIR
import sr_anlz.execute2.word_error as word_error
import sr_anlz.execute2.functions as functions
import os
import numpy

output_path = os.path.join(PKG_DIR, "output", "ErrorFreqResult.txt")

freqResult = open(output_path, 'w+')
grade = open(os.path.join(PKG_DIR, "output", "ErrorWer.txt"), 'w+')
alignedresult = open(os.path.join(PKG_DIR, "output", "ErrorAlignedresult.txt"), 'w+')

freqDict = {}
mistake = 0



def editDistance(r, h):
    '''
    This function is to calculate the edit distance of reference sentence and the hypothesis sentence.

    Main algorithm used is dynamic programming.

    Attributes:
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
    '''
    d = numpy.zeros((len(r) + 1) * (len(h) + 1), dtype=numpy.uint8).reshape((len(r) + 1, len(h) + 1))
    for i in range(len(r) + 1):
        for j in range(len(h) + 1):
            if i == 0:
                d[0][j] = j
            elif j == 0:
                d[i][0] = i
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitute = d[i - 1][j - 1] + 1
                insert = d[i][j - 1] + 1
                delete = d[i - 1][j] + 1
                d[i][j] = min(substitute, insert, delete)
    return d


def getStepList(r, h, d):
    '''
    This function is to get the list of steps in the process of dynamic programming.

    Attributes:
        r -> the list of words produced by splitting reference sentence.
        h -> the list of words produced by splitting hypothesis sentence.
        d -> the matrix built when calulating the editting distance of h and r.
    '''
    x = len(r)
    y = len(h)
    list = []
    while True:
        if x == 0 and y == 0:
            break
        elif x >= 1 and y >= 1 and d[x][y] == d[x - 1][y - 1] and r[x - 1] == h[y - 1]:
            list.append("e")
            x = x - 1
            y = y - 1
        elif y >= 1 and d[x][y] == d[x][y - 1] + 1:
            list.append("i")
            x = x
            y = y - 1
        elif x >= 1 and y >= 1 and d[x][y] == d[x - 1][y - 1] + 1:
            list.append("s")
            x = x - 1
            y = y - 1
        else:
            list.append("d")
            x = x - 1
            y = y
    # print(list[::-1])
    return list[::-1]


def alignedPrint(list, r, h, result):
    '''
    This funcition is to print the result of comparing reference and hypothesis sentences in an aligned way.

    Attributes:
        list   -> the list of steps.
        r      -> the list of words produced by splitting reference sentence.
        h      -> the list of words produced by splitting hypothesis sentence.
        result -> the rate calculated based on edit distance.
    '''
    editorder = []
    editorder.append(("N", ('', '')))
    alignedresult.write("REF:" + ' ')
    for i in range(len(list)):
        if list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            editorder.append(("I", (" ", h[index])))
            alignedresult.write(" " * (len(h[index])) + " ")
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) < len(h[index2]):
                alignedresult.write(r[index1] + " " * (len(h[index2]) - len(r[index1])) + " ")
                editorder.append(("S", (r[index1], h[index2])))
            else:
                alignedresult.write(r[index1] + ' ')
                editorder.append(("S", (r[index1], h[index2])))

        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            if list[i] == "d":
                editorder.append(("D", (r[index], ' ')))
            else:
                editorder.append(("E", (r[index], r[index])))
            alignedresult.write(r[index] + ' ')
    alignedresult.write('\n')
    alignedresult.write("HYP:" + ' ')
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            alignedresult.write(" " * (len(r[index])) + ' ')
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                alignedresult.write(h[index2] + " " * (len(r[index1]) - len(h[index2])) + ' ')
            else:
                alignedresult.write(h[index2] + ' ')

        else:
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            alignedresult.write(h[index] + ' ')
    alignedresult.write('\n')
    # Evaluation
    alignedresult.write("EVA:" + ' ')
    for i in range(len(list)):
        if list[i] == "d":
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            alignedresult.write("D" + " " * (len(r[index]) - 1) + ' ')
        elif list[i] == "i":
            count = 0
            for j in range(i):
                if list[j] == "d":
                    count += 1
            index = i - count
            alignedresult.write("I" + " " * (len(h[index]) - 1) + ' ')
        elif list[i] == "s":
            count1 = 0
            for j in range(i):
                if list[j] == "i":
                    count1 += 1
            index1 = i - count1
            count2 = 0
            for j in range(i):
                if list[j] == "d":
                    count2 += 1
            index2 = i - count2
            if len(r[index1]) > len(h[index2]):
                alignedresult.write("S" + " " * (len(r[index1]) - 1) + ' ')
            else:
                alignedresult.write("S" + " " * (len(h[index2]) - 1) + ' ')
        else:
            count = 0
            for j in range(i):
                if list[j] == "i":
                    count += 1
            index = i - count
            alignedresult.write(" " * (len(r[index])) + ' ')
    alignedresult.write('\n')

    editorder.append(("N", ('', '')))
    return editorder


def wer(r, h):
    """
    This is a function that calculate the word error rate in ASR.
    You can use it like this: wer("what is it".split(), "what is".split())
    """
    # build the matrix
    d = word_error.editDistance(r, h)

    # find out the manipulation steps
    steplist = word_error.getStepList(r, h, d)

    global mistake
    mistake = mistake + d[len(r)][len(h)]
    result_1 = float(d[len(r)][len(h)]) / len(r) * 100
    result = str("%.2f" % result_1) + "%"

    grade.write('{}\n'.format("%.2f" % (100 - result_1)))
    editorder = alignedPrint(steplist, r, h, result)
    return editorder


def n_gram_set(sentences, n):
    # print(bow[1])
    N_Gram = list()
    for sentence in sentences:
        for i in range(len(sentence) - n + 1):
            N_Gram.append(tuple(sentence[i:i + n]))

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
    sumE = len(error_SS) + len(error_SD) + len(error_DS) + len(error_II) + len(error_IS) + len(error_SI) + len(
        error_DD) + len(error_I) + len(error_D) + len(error_S)
    grade.write('WER: {}'.format((sumE / len(N_Gram))))
    print(sumE / len(N_Gram))
    global freqDict
    freqDict["WER"] = [sumE, round(sumE / len(N_Gram),3)]

    return (error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD, error_I, error_D, error_S, len(N_Gram))


def print_func(name, error, total):
    error_tuple = []
    error_list = []
    print(name,error,total)

    freqResult.write("{} : {} =====\n".format(name, len(error) / total))
    freqDict[name] = [len(error), round(len(error) / total,3)]
    for k in error:
        error_type = ""
        error_type = functions.type(name, k)
        if error_type == "None":
            freqResult.write(str(k) + '\n')
        else:
            error_tuple.append(error_type)
            freqResult.write("{}\t{}\n".format(error_type,k))
    for i in set(error_tuple):
        error_list.append((i, error_tuple.count(i)))
    freqDict[name].append(error_list)
    freqResult.write('\n')


def format_print(error):
    error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD, error_I, error_D, error_S, total = error
    print_func("SS", error_SS, total)
    print_func("SD", error_SD, total)
    print_func("DS", error_DS, total)
    print_func("II", error_II, total)
    print_func("IS", error_IS, total)
    print_func("SI", error_SI, total)
    print_func("DD", error_DD, total)
    print_func("I", error_I, total)
    print_func("D", error_D, total)
    print_func("S", error_S, total)


def main_freq():
    test = open(os.path.join(PKG_DIR, "output", "recognition.txt"), 'r')
    sol = open(os.path.join(PKG_DIR, "refined-audio", "trans.txt"), 'r')
    test_string = test.readlines()
    sol_string = sol.readlines()
    # print(len(sol_string))
    sum = 0
    sentences = []
    for i in range(len(sol_string)):
        sol_word = sol_string[i].strip("\n").lower().split()
        sum = sum + len(sol_word)
        test_word = test_string[i].strip("\n").lower().split()
        sentences.append(wer(sol_word, test_word))

    error = n_gram_set(sentences, 2)
    format_print(error)

    sorted_by_value = sorted(freqDict.items(), key=lambda kv: kv[1],reverse=True)
    test.close()
    sol.close()
    freqResult.close()
    alignedresult.close()
    grade.close()


    return output_path, sorted_by_value

def sec_freq(rec_file,trans_file):
    test = open(rec_file,'r')
    sol = open(trans_file,'r')

    test_string = test.readlines()
    sol_string = sol.readlines()
    # print(len(sol_string))
    sum = 0
    sentences = []
    for i in range(len(sol_string)):
        if sol_string[i] == "\n":
            print("Error Occur")
            break
        sol_word = sol_string[i].strip("\n").lower().split()
        sum = sum + len(sol_word)
        test_word = test_string[i].strip("\n").lower().split()
        sentences.append(wer(sol_word, test_word))


    error = n_gram_set(sentences,2)
    print("PASS N-GRAM")

    format_print(error)
    print("PASS FORMAT PRINT")

    sorted_by_value = sorted(freqDict.items(), key=lambda kv: kv[1],reverse=True)
    test.close()
    sol.close()
    freqResult.close()
    alignedresult.close()
    grade.close()

    return output_path, sorted_by_value

