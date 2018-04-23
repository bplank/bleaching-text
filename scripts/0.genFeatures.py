import json
import sys
from collections import Counter
from math import log
import argparse
import re
from emoji import UNICODE_EMOJI
import string

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


parser=argparse.ArgumentParser(description='Feature extractor.')
parser.add_argument('json',help='JSON to be read')
parser.add_argument('method',help='Method to be applied',choices=['vowels', 'punctCons', 'punctAgr', 'length','frequency','shape'])
args=parser.parse_args()
dataset=json.load(open(args.json))
output=[]
frequency=Counter()
special=set(['NEWLINE','URL','USER'])
for texts in dataset['tweets']:
  instance=[]
  if args.method=='length':
    for token in texts.split(' '):
      if token not in special:
        instance.append('0' + str(len(token)))
      else:
        instance.append(token)
    output.append(instance)
  elif args.method=='frequency':
    frequency.update([e.lower() for e in texts.split(' ') if e not in special])
  elif args.method=='shape':
    for token in texts.split(' '):
      if token not in special:
        instance.append(shape(token))
      else:
        instance.append(token)
    output.append(instance)
  elif args.method=='punctCons':
    for token in texts.split(' '):
      if token not in special:
        instance.append(punctCons(token))
      else:
        instance.append(token)
    output.append(instance)
  elif args.method=='punctAgr':
    for token in texts.split(' '):
      if token not in special:
        instance.append(punctAgr(token))
      else:
        instance.append(token)
    output.append(instance)
  elif args.method=='vowels':
    for token in texts.split(' '):
      if token not in special:
        new = ''
        for char in token:
          if char.lower() in 'euioa':
            new += 'v'
          elif char.isalpha():
            new += 'c'
          else:
            new += 'o'
        instance.append(new)
      else:
        instance.append(token)   
    output.append(instance) 

if args.method=='frequency':
  for token,freq in list(frequency.items()):
    frequency[token]=str(int(log(freq,10)))
  for token in special:
    frequency[token.lower()]=token
  for texts in dataset['tweets']:
    instance=[]
    for token in texts.split(' '):
      instance.append(frequency[token.lower()])
    output.append(instance)

"""
feature_map={}
for texts,outputs in zip(dataset['tweets'],output):
  for token,trans in zip(texts.split(' '),outputs):
    if trans not in feature_map:
      feature_map[trans]={}
    feature_map[trans][token]=feature_map[trans].get(token,0)+1
"""

print( dataset['tweets'][0].split(' ')[:20])
print( output[0][:20])

dataset['tweets']=[' '.join(e) for e in output]
json.dump(dataset,open(args.json+'.'+args.method,'w'))
#json.dump(feature_map,open(args.json+'.'+args.method+'.feats','w'))
