import json
import sys

if len(sys.argv) < 3:
  print('please specify target file and list of json files to combine')
  exit(0)

finalData = {}
for i in range(2,len(sys.argv)):
  data = json.load(open(sys.argv[i]))
  if i == 2:
    finalData['gender'] = data['gender']
    #finalData['user_ids'] = data['user_ids']
    finalData['tweets'] = data['tweets']
  else:
    finalData['tweets'] += data['tweets']
    finalData['gender'] += data['gender']
json.dump(finalData, open(sys.argv[1], 'w'))

