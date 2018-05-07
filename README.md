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

If you use parts of this repository we appreciate if you cite us:

```
@InProceedings{vangoot:ea:2018,
  author    = {van der Goot, Rob and Ljube\v{s}i\'{c}, Nikola  and Matroos, Ian and Nissim, Malvina and Plank, Barbara},
  title     = {Bleaching Text: Abstract Features for Cross-lingual Gender Prediction},
  booktitle = {Proceedings of the 56th Annual Meeting of the Association for Computational Linguistics},
  month     = {August},
  year      = {2018},
  address   = {Melbourne},
  publisher = {Association for Computational Linguistics},
}

```
