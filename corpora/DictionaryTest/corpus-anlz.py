import difflib

with open('uniqWIKI.txt') as text1:
    with open('uniqWIKI2.txt') as text2:
        d = difflib.Differ()
        diff = list(d.compare(text1.readlines(), text2.readlines()))
        with open('test.txt', 'w') as diff_file:
            _diff = ''.join(diff)
            diff_file.write(_diff)

uniq = open("commWIKI3.txt",'w')
k=0
with open ('test.txt') as text3:
    words = text3.readlines()
    for word in words:
        if word[0] ==" ": uniq.write(word)


'''

file = open("librispeech-lexicon.txt",'r')
output = open("lexicon.txt",'w')
pronounciation = file.readlines()
for i in pronounciation:
    word = i.split()
    output.write("{} {}\n".format(word[0].lower()," ".join( i for i in word[1:])))


from collections import Counter;
file = open("wiki_00.txt",'r')
tokens = file.readlines()
print(type(tokens))
types = Counter(tokens)
print(types.most_common(100))
'''