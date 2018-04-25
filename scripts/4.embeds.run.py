import os
import sys

outDir = 'runs/6-1/'
os.system('mkdir -p ' + outDir)
#4lang-data-200tweets.json.balanced.NL
for tgtLang in ['EN', 'NL', 'PT', 'FR', 'ES']:
    outFile = outDir + '/' + tgtLang + 'embeds_new.out'
    trainFile = 'data_6-1/4lang-data-200tweets.json.balanced.' + tgtLang
    testFile = 'data_prefixed/' + tgtLang + '-data-200tweets.json.balanced'
    cmd = 'python3 src/classifier.py ' + trainFile + ' ' + '--embeds /net/shared/bplank/gender/embeds_rob/en+es+nl+fr+pt.100.txt' + ' '  + ' --test ' + testFile + ' --show-instance > ' + outFile + ' 2> ' + outFile + '2'
    print(cmd)


