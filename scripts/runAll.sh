echo "SHALL WE INCLUDE THE RAW DATA IN THE REPO?"
python3 scripts/0.featurize.py > run.sh
chmod +x run.sh
./run.sh

python3 scripts/1.ngramTuning.run.py > run.sh
chmod +x run.sh
./run.sh

python3 scripts/2.lexVScomb.run.py > run.sh
chmod +x run.sh
./run.sh

python3 scripts/3.4-1.prep.sh > run.sh
chmod +x run.sh
./run.sh

python3 scripts/3.4-1.run.sh > run.sh
chmod +x run.sh
./run.sh

python3 scripts/4.embeds.prep.py
python3 scripts/4.embeds.run.py > run.sh
chmod +x run.sh
./run.sh


