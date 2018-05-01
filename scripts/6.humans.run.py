import os

outDir = 'runs/6.humans/'
os.system('mkdir -p ' + outDir)

for run in [('data/FR-data-200tweets.json.balanced',  '200'), ('data/FR-data-20tweets.json.balanced',  '20')]:
    train = run[0]
    test = 'data_humans/NL.filtered.test.20'
    if run[1] == 20:
        test = test + '.20'
    outFile = 'FR.NL.' + run[1] + '.out'
    errFile = 'FR.NL.' + run[1] + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb' + errFile
    print(cmd)

for run in [('NL.filtered', '200'), ('NL.filtered', '20')]:
    train = 'data_humans/' + run[0] + '.train'
    test = 'data_humans/' + run[0] + '.test.20'
    if run[1] == '20':
        train = train + '.20'
    outFile = 'NL.NL.' + run[1] + '.out'
    errFile = 'NL.NL.' + run[1] + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb.' + errFile
    print(cmd)


for run in [('NL.filtered', '200'), ('NL.filtered', '20')]:
    train = 'data_humans/' + run[0] + '.train'
    test = 'data_humans/PT.filtered.test.20'
    if run[1] == '20':
        train = train + '.20'
    outFile = 'NL.PT.' + run[1] + '.out'
    errFile = 'NL.PT.' + run[1] + '.err'
    cmd = 'python3 src/classifier.py ' + train + ' --test ' + test + ' --n-gram 1-2 --c-n-gram 3-6 > ' + outDir + 'lex.' + outFile + ' 2> ' + outDir + 'lex.' + errFile
    print(cmd)
    cmd = 'python3 src/classifier.py ' + train + '.comb --test ' + test + '.comb --n-gram 5 > ' + outDir + 'comb.' + outFile + ' 2> ' + outDir + 'comb.' + errFile
    print(cmd)

