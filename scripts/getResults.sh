
python3 scripts/9.bigTable.py
echo "" 

python3 scripts/9.smallTable.py
echo "" 


#get most important features
grep "^$" -A 1 runs/3.4-1/*comb*/* | grep -v ":$" | grep -v "^--$" > results
python3 scripts/5.feats.find.py results
echo "" 


python3 scripts/9.humanTable.py
echo "" 

echo "NL.NL Fleiss"
python3 scripts/9.fleiss.py humanData/dutch2dutch/*csv

echo "FR.NL Fleiss"
python3 scripts/9.fleiss.py humanData/french2dutch/*csv

echo "NL.PT Fleiss"
python3 scripts/9.fleiss.py humanData/dutch2port/*csv

echo ""

