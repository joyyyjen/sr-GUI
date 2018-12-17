#!/usr/local/bin/python3
import sr_anlz.execute.word_error as word_error
import sr_anlz.execute.functions as functions
import os
from sr_anlz.definition import PKG_DIR

output_path = os.path.join(PKG_DIR, "output", "ErrorFreqResult.txt")

freqResult = open(output_path, 'w+')

freqDict = {}


# outputResult = open('../output/train.txt','w+')

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
    sumE = len(error_SS) + len(error_SD) + len(error_DS) + len(error_II) + len(error_IS) + len(error_SI) + len(
        error_DD) + len(error_I) + len(error_D) + len(error_S)
    print(sumE / len(N_Gram))
    global freqDict
    freqDict["WER"] = [sumE, round(sumE / len(N_Gram),3)]

    return (error_SS, error_SD, error_DS, error_II, error_IS, error_SI, error_DD, error_I, error_D, error_S, len(N_Gram))


def print_func(name, error, total):
    error_tuple = []
    error_list = []

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
    sents = []
    for i in range(len(sol_string)):
        sol_word = sol_string[i].strip("\n").lower().split()
        sum = sum + len(sol_word)
        test_word = test_string[i].strip("\n").lower().split()
        sents.append(word_error.wer(sol_word, test_word))

    error = n_gram_set(sents, 2)
    format_print(error)

    sorted_by_value = sorted(freqDict.items(), key=lambda kv: kv[1],reverse=True)
    test.close()
    sol.close()
    freqResult.close()

    return output_path, sorted_by_value
