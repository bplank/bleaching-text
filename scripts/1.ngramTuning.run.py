import os
import sys

outDir = 'runs/1.ngram'
os.system('mkdir -p ' + outDir)

for lang in reversed(['EN', 'NL', 'FR', 'PT', 'ES']):
    for feat in ['punctAgr', 'punctCons', 'vowels', 'frequency', 'shape', 'length', 'comb']:
        for ngram in list(range(1,7)):
            outFile = outDir + '/' + lang + '.' + feat + '.' + str(ngram) + '.out'
            trainTestFile = 'data_balanced_non_tokenized/' + lang + '-data-200tweets.json.balanced.' + feat
            cmd = 'python3 src/classifier.py ' + trainTestFile + ' --n-gram ' + str(ngram) + ' > ' + outFile + ' 2> ' + outFile + '.err'
            print(cmd)
            outFile = outDir + '/' + lang + '.' + feat + '.1-' + str(ngram) + '.out'
            cmd = 'python3 src/classifier.py ' + trainTestFile + ' --n-gram 1-' + str(ngram) + ' > ' + outFile + ' 2> ' + outFile + '.err'
            print(cmd)
