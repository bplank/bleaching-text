import os
import sys

if len(sys.argv) < 2:
    print('usage:')
    print('grep "^$" -A 1 runs/3.4-1/*comb*/* | grep -v ":$" | grep -v "^--$" > results')
    print('python3 scripts/5.feats.find.py results')
    exit(1) 


manFeats = {}
manFeatCounts = {}
femFeats = {}
femFeatCounts = {}
for line in open(sys.argv[1]):
    tok = line.split()
    #lang = tok[0].split('/')[2][:2]
    
    scoreFem = float(tok[0].split('--')[1])
    featFem = tok[1]
    if featFem not in femFeats:
        femFeats[featFem] = 0.0
        femFeatCounts[featFem] = 0
    femFeats[featFem] += scoreFem
    femFeatCounts[featFem] += 1

    scoreMan = float(tok[2])
    featMan = tok[3]
    if featMan not in manFeats:
        manFeats[featMan] = 0.0
        manFeatCounts[featMan] = 0
    manFeats[featMan] += scoreMan
    manFeatCounts[featMan] += 1
#avg
for feat in manFeats:
    manFeats[feat] = manFeats[feat] / 5
for feat in femFeats:
    femFeats[feat] = femFeats[feat] / 5

print("TOP FEATS FOR MALE")
for feat in sorted(manFeats, key=manFeats.get, reverse=True)[:20]:
    print(str(round(manFeats[feat], 5)) + '\t' + str(manFeatCounts[feat]) + '\t' + feat)

print()
print("TOP FEATS FOR FEMALE")
for feat in sorted(femFeats, key=femFeats.get, reverse=True)[:20]:
    print(str(round(femFeats[feat], 5)) + '\t' + str(femFeatCounts[feat]) + '\t' + feat)

