import os

outDir = 'runs/6.humans/'
os.system('mkdir -p ' + outDir)

for run in ['200',  '20']:
    train = 'data/FR-data-200tweets.json.balanced'
    test = 'data_humans/NL.filtered.test'
    if run == '20':
        test = test + '.20'
    outFile = 'FR.NL.' + run + '.out'
    errFile = 'FR.NL.' + run + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb' + errFile
    print(cmd)

for run in ['200', '20']:
    train = 'data_humans/NL.filtered.train'
    test = 'data_humans/NL.filtered.test'
    if run == '20':
        test = test + '.20'
    outFile = 'NL.NL.' + run + '.out'
    errFile = 'NL.NL.' + run + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb.' + errFile
    print(cmd)


for run in ['200', '20']:
    train = 'data_humans/NL.filtered.train'
    test = 'data_humans/PT.filtered.test'
    if run == '20':
        test = test + '.20'
    outFile = 'NL.PT.' + run + '.out'
    errFile = 'NL.PT.' + run + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb.' + errFile
    print(cmd)

