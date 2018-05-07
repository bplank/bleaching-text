# bleaching-text

you need python packages:
emoji (we used version 0.4.5)
sklearn (we used version 0.19.1)
numpy (we used version 1.14.2)

To reproduce results from the paper (note that they are also already included in the runs folder):
```
./scripts/runAll.sh
parallel -j 16 < run.sh 
```

To generate the tables from the paper:
```
./scripts/getResults.sh
```

