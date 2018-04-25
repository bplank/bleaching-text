


python3 ../src/classifier.py data/FR-data-200tweets.json.balanced --test french2dutch/all.json --pred --n-gram 1-2 --c-n-gram 3-6
python3 ../src/classifier.py data/FR-data-200tweets.json.balanced.comb --test french2dutch/all.json --pred --n-gram 1-2 --c-n-gram 3-6

python3 ../src/classifier.py data_humans/FR-data-20tweets.json.balanced --test french2dutch/all.json --pred --n-gram 1-2 --c-n-gram 3-6
python3 ../src/classifier.py data_humans/FR-data-20tweets.json.balanced.comb --test french2dutch/all.json --pred --n-gram 1-2 --c-n-gram 3-6
