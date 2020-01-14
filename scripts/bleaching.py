import re
from collections import Counter
from math import log
from emoji import UNICODE_EMOJI

emoticon_string = r"""
    (?:
      [<>]?
      [:;=8>]                    # eyes
      [\-o\*\']?                 # optional nose
      [\)\]\(\[dDpPxX/\:\}\{@\|\\] # mouth      
      |
      [\)\]\(\[dDpPxX/\:\}\{@\|\\] # mouth
      [\-o\*\']?                 # optional nose
      [:;=8<]                    # eyes
      [<>]?
      |
      <[/\\]?3                         # heart(added: has)
      |
      \(?\(?\#?                   #left cheeck
      [>\-\^\*\+o\~]              #left eye
      [\_\.\|oO\,]                #nose
      [<\-\^\*\+o\~]              #right eye
      [\#\;]?\)?\)?               #right cheek
    )"""

emoticon_re = re.compile(emoticon_string, re.VERBOSE | re.I | re.UNICODE)
special=set(['NEWLINE','URL','USER'])

#prep for frequency
def initFreq(text):
    frequency=Counter()
    for line in text:
        frequency.update([e.lower() for e in line.split(' ') if e not in special])
    for token,freq in list(frequency.items()):
        frequency[token]=str(int(log(freq,10)))
    for token in special:
        frequency[token.lower()]=token
    return frequency

def frequency(word, frequency):
    return(frequency[word.lower()])

def length(word):
    return '0' + str(len(word))

def lex(word):
    return word

def punctAgr(token):
    emojis = ''
    for char in token:
        if char in UNICODE_EMOJI:
            emojis += 'J'
    if emojis != '':
        return(emojis)
    elif (emoticon_re.search(token) != None):
        return('E')
    else:
        isWord = False
        for char in token:
            if char.isalpha() or char.isalnum():
                isWord = True
        if isWord:
            beg = ''
            for i in range(len(token)):
                if token[i].isalpha() or token[i].isalnum():
                    break
                else:
                    beg += 'P'
            end = ''
            for i in range(len(token)-1, 0, -1):
                if token[i].isalpha() or token[i].isalnum():
                    break
                else:
                    end += 'P'
            return(beg + 'W' + end)
        else:
            return('P' * len(token)) 

def punctCons(token):
    emojis = ''
    for char in token:
        if char in UNICODE_EMOJI:
            emojis += char
    if emojis != '':
        return(emojis)
    else:
        newWord = ''
        lastAlpha = False
        for char in token:
            if char.isalpha() or char.isalnum():
                if not lastAlpha:
                    newWord += 'W'
                lastAlpha = True
            else:
                newWord += char
                lastAlpha = False
        return newWord

def shape(token):
    packed=''
    for char in token:
        if char.isupper():
            packed+='u'
        elif char.islower():  
            packed+='l'
        elif char.isdigit():
            packed+='d'
        else:
            packed+='x'
    return re.sub(r'(.)\1{2,}',r'\1\1',packed)
        
def vowels(word):
    new = ''
    for char in word:
        if char.lower() in 'euioa':
            new += 'v'
        elif char.isalpha():
            new += 'c'
        else:
            new += 'o'
    return new

def bleachAll(text, freq):
    newText = ''
    for method in ['frequency', 'length', 'lex', 'punctAgr', 'punctCons', 'shape', 'vowels']:
        if method != 'frequency':
            newText += bleachText(text, method, freq)
    return newText

# to use frequency, you have to run it like this:
# freqs = bleaching.initFreq(text)
# bleaching.bleachText(text, 'frequency', freqs)
# the frequency is then based on the entire dataset

#if you do not need the frequency transformation:
# bleaching.bleachText(text, 'length', None)
def bleachText(text, method, freq):
    if method == 'all':
        return bleachAll(text, freq)
    newText = ''
    for line in text.split('\n'):
        for word in line.split(' '):
            if word not in special:
                if method== 'frequency':
                    if freq == None:
                        print('ERROR: frequency is used, but no counter is given')
                    newText += frequency(word, freq) + ' '
                if method== 'all':
                    if freq == None:
                        print('ERROR: all is used, but no counter is given')
                    newText += frequency(word, freq) + ' '
                elif method== 'length':
                    newText += length(word) + ' '
                elif method== 'lex':
                    newText += lex(word) + ' '
                elif method== 'punctAgr':
                    newText += punctAgr(word) + ' '
                elif method== 'punctCons':
                    newText += punctCons(word) + ' '
                elif method== 'shape':
                    newText += shape(word) + ' ' 
                elif method== 'vowels':
                    newText += vowels(word) + ' '
                else:
                    print('ERROR method ' + method + '  does not exist')
            else:
                newText += word + ' '
        newText += '\n'
    return newText[:-1]

