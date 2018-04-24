import os
import sys

outDir = 'runs/5.feats/'
os.system('mkdir -p ' + outDir)

for lang in ['EN', 'NL', 'PT', 'FR', 'ES']:
    outFile = outDir + '/' + lang + '.comb.5.out'
    trainFile = 'data_4-1/4lang-data-200tweets.json.balanced.' + lang 
    testFile = 'data/' + lang + '-data-200tweets.json.balanced'
    cmd = 'python3 src/classifier.py ' + trainFile + ' --test ' + testFile + ' --analyze-features ' + outFile + '.feats --comb > ' + outFile + ' 2> ' + outFile + '2'
    print(cmd)
    

