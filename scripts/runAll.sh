
python3 scripts/0.featurize.py >> run.sh

#python3 scripts/1.ngramTuning.run.py >> run.sh

python3 scripts/2.lexVScomb.run.py >> run.sh

python3 scripts/3.4-1.run.py >> run.sh

#python3 scripts/4.embeds.prep.py
#python3 scripts/4.embeds.run.py > run.sh
#parallel -j $NTHREADS < run.sh

./scripts/6.humans.prep.sh
python3 scripts/6.humans.run.py >> run.sh

echo "NOW RUN ALL COMMANDS IN run.sh'

