import sys
import csv
import json
import numpy as np

if len(sys.argv) < 2:
    print('please give csv file')
    exit(1)

def fleiss_kappa(M):
  """
  See `Fleiss' Kappa <https://en.wikipedia.org/wiki/Fleiss%27_kappa>`_.
  :param M: a matrix of shape (:attr:`N`, :attr:`k`) where `N` is the number of subjects and `k` is the number of categories into which assignments are made. `M[i, j]` represent the number of raters who assigned the `i`th subject to the `j`th category.
  :type M: numpy matrix
  """
  N, k = M.shape  # N is # of items, k is # of categories
  n_annotators = float(np.sum(M[0, :]))  # # of annotators

  p = np.sum(M, axis=0) / (N * n_annotators)
  P = (np.sum(M * M, axis=1) - n_annotators) / (n_annotators * (n_annotators - 1))
  Pbar = np.sum(P) / N
  PbarE = np.sum(p * p)

  kappa = (Pbar - PbarE) / (1 - PbarE)

  return kappa


data = {}
users = set()
for i in range(1, len(sys.argv)):
    with open(sys.argv[i])as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if row[0] == '_unit_id':
                continue
            if len(row) != 33 and len(row) != 31:
                print(row)
                print(len(row))
                print('Error!')
                continue
            guess = row[10]
            gold = row[11]
            userId = row[7]
            tweets = ' NEWLINE '.join(row[13:33]) + str(i)
            if tweets not in data:
                data[tweets] = {}
            data[tweets]['gold'] = gold
            data[tweets]['text'] = tweets
            if 'human' not in data[tweets]:
                data[tweets]['human'] = {}
            data[tweets]['human'][userId] = guess
            users.add(userId)

M = np.zeros((len(data),2))
finalData = {'gender':[], 'tweets':[], 'human':[]}
for rowIdx, sentId in enumerate(sorted(data)):
    for user in sorted(data[sentId]['human']):
        if data[sentId]['human'][user] == 'M':
            M[rowIdx][1] += 1
        else:
            M[rowIdx][0] += 1

#print(M)
print(M.shape)
print(fleiss_kappa(M))

