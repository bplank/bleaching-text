import sys
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

if len(sys.argv) < 2:
    print('usage:')
    print('grep "^mean acc" outputs/1.ngram/*out > results')
    print('python3 scripts/1.ngramTuning.graph.py results')
    exit(0)


fig, ax = plt.subplots(nrows=3, ncols=3)

y_min=50
y_max=75

data = {}
for line in open(sys.argv[1]):
    line = line[line.rfind('/') + 1:]
    tok = line.split('.')
    lang = tok[0]# not really used
    feat = tok[1]
    ngram = tok[2]
    perf = float(line.split()[2])
    if feat not in data:
        data[feat] = {}
    if ngram not in data[feat]:
        data[feat][ngram] = [0.0, 0]
    data[feat][ngram][0] += perf
    data[feat][ngram][1] += 1


for featIdx, feature in enumerate(data):
    row = featIdx % 3
    col = int(featIdx / 3)
    dest = ax[row][col]
    graph = []
    names = ['1', '2', '3', '4', '5', '6', '1-2', '1-3', '1-4', '1-5', '1-6']
    highestScore = 0
    highestN = 0
    for ngram in names:
        if ngram in data[feature]:
            print(feature, ngram, data[feature][ngram][1])
            graph.append(data[feature][ngram][0] / data[feature][ngram][1])
            if data[feature][ngram][0] > highestScore:
                highestScore = data[feature][ngram][0]
                highestN = name
    print(feature, highestN, highestScore) 
    dest.bar(range(len(graph)), graph)
    dest.set_title(feature)
    dest.set_xticks(range(len(names)))
    dest.set_xticklabels(names, rotation=45)
    dest.set_ylim((y_min,y_max))
    dest.set_xlim((0, len(names)))

plt.show()
plt.savefig("ngram.pdf")
