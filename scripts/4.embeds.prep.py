import os

tgtDir = 'data_6-1'
os.system('mkdir -p ' + tgtDir)

langs = ['EN', 'NL', 'PT', 'FR', 'ES']

for tgtLang in langs:
    srcLangs = list(langs)
    srcLangs.remove(tgtLang) 

    #combine prefixed files

    srcs = []
    for srcLang in srcLangs:
        srcs.append('data_prefixed/' + srcLang + '-data-200tweets.json.balanced')
    cmd = 'python3 scripts/concatJson.py ' + tgtDir + '/4lang-data-200tweets.json.balanced.' + tgtLang + ' ' + ' '.join(srcs)
    print(cmd)

