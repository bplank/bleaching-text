import os

tgtDir = 'data_4-1'
os.system('mkdir -p ' + tgtDir)

langs = ['EN', 'NL', 'PT', 'FR', 'ES']

for tgtLang in langs:
    srcLangs = list(langs)
    srcLangs.remove(tgtLang) 

    #combine for comb, lex (and combLex?)
    for feat in ['.comb', '']:
        srcs = []
        for srcLang in srcLangs:
            srcs.append('data_balanced_non_tokenized/' + srcLang + '-data-200tweets.json.balanced' + feat)
        cmd = 'python3 scripts/concatJson.py ' + tgtDir + '/4lang-data-200tweets.json.balanced.' + tgtLang + feat + ' ' + ' '.join(srcs)
        print(cmd)
        

