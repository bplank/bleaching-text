mkdir -p data_humans

python3 scripts/0.csv2json.py humanData/dutch2dutch/f1233806.csv humanData/dutch2dutch/f1233807.csv
mv humanData/dutch2dutch/all.json data_humans/NL.NL.json

python3 scripts/0.csv2json.py humanData/dutch2port/f1233804.csv humanData/dutch2port/f1233805.csv
mv humanData/dutch2port/all.json data_humans/NL.PT.json

python3 scripts/0.csv2json.py humanData/french2dutch/f1233798_all.csv humanData/french2dutch/f1233803_all.csv
mv humanData/french2dutch/all.json data_humans/FR.NL.json

python3 scripts/6.humans.filter.py data_humans/NL.NL.json data/NL-data-200tweets.json.balanced data_humans/NL.filtered
python3 scripts/6.humans.filter.py data_humans/NL.PT.json data/PT-data-200tweets.json.balanced data_humans/PT.filtered

python3 scripts/6.humans.to20.py data_humans/NL.filtered.test data_humans/NL.filtered.test.20
python3 scripts/6.humans.to20.py data_humans/NL.filtered.train data_humans/NL.filtered.train.20
python3 scripts/6.humans.to20.py data/FR-data-200tweets.json.balanced data/FR-data-20tweets.json.balanced
python3 scripts/6.humans.to20.py data_humans/PT.filtered.test data_humans/PT.filtered.test.20
python3 scripts/6.humans.featurize.py > run.sh
chmod +x run.sh
./run.sh

