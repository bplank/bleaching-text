__author__ = "bplank"

import argparse
import codecs

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction import DictVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.model_selection import StratifiedKFold

import numpy as np
import random
import json
from collections import Counter
import os

# for analysis of features
import nltk
from scipy import stats

from myutils import Featurizer, EmbedsFeaturizer, get_size_tuple, PREFIX_WORD_NGRAM, PREFIX_CHAR_NGRAM, TWEET_DELIMITER

# fix seed for replicability
seed=103
random.seed(seed)
np.random.seed(seed)

def main():

    # parse command line options
    parser = argparse.ArgumentParser(description="""simple classifier""")
    parser.add_argument("data", help="json data file") # cross-validation if no --test file given
    parser.add_argument("--test", help="if given train on all and test on test file (otherwise CV)", required=False)
    parser.add_argument("--pred", help="write prediction to json file", default=False, action='store_true', required=False)
    parser.add_argument("--embeds", help="use embeddings as features")
    parser.add_argument("--only-mean", help="use only average embedding", default=False, action="store_true")
    parser.add_argument("--folds", help="number of folds (if no test data is given)", default=10, type=int)
    parser.add_argument("--C", help="parameter C for regularization", required=False, default=1, type=float)
    parser.add_argument("--n-gram", help="word n-gram size, string separated by -", default="1-2")
    parser.add_argument("--c-n-gram", help="character n-gram size, string separated by -", default="0") # 0=off
    parser.add_argument("--tf-idf", help="use tf-idf", default=False, action="store_true")
    parser.add_argument("--show-instance", help="print instance", default=False, action="store_true")
    parser.add_argument("--rm-uu", help="remove USER and URL token from instances", default=False, action="store_true")
    parser.add_argument("--analyze-features", help="path to output for feature analysis", default=None)

    args = parser.parse_args()

    ## read input data
    print("load data..")

    if args.pred:
        X_train, y_train, X_test, y_test, _ = vectorize_data(args, test=True)
        f1_test, acc_test, pred = train_eval(args, X_train, y_train, X_test, y_test)
        jsonData = json.load(open(args.test))
        jsonData['machine'] = list(pred)
        json.dump(jsonData, open(args.test + '2', 'w'))

    elif args.test:
        X_train, y_train, X_test, y_test, _ = vectorize_data(args, test=True)

        f1_test, acc_test, _ = train_eval(args, X_train, y_train, X_test, y_test)
        print("weighted f1: {0:.1f}".format(f1_test * 100))
        print("accuracy: {0:.1f}".format(acc_test * 100))

        get_majority_baseline(y_train, y_test)

    else:
        ## if no --test file is given performe stratified CV

        X_all, y_all, _ = vectorize_data(args, test=False)

        skf = StratifiedKFold(n_splits=args.folds)
        f1_scores, acc_scores = [], []
        for train, test in skf.split(X_all, y_all):
            X_train, y_train = X_all[train], y_all[train]
            X_test, y_test = X_all[test], y_all[test]

            f1_test, acc_test, _ = train_eval(args, X_train, y_train, X_test, y_test)

            f1_scores.append(f1_test)
            acc_scores.append(acc_test)
            print("weighted f1: {0:.1f}".format(f1_test * 100))

        print("==================================")
        f1_scores = np.array(f1_scores)
        acc_scores = np.array(acc_scores)
        print("mean f1: {:.2f} ({:.2f})".format(np.mean(f1_scores) * 100, np.std(f1_scores) * 100))
        print("mean acc: {:.2f} ({:.2f})".format(np.mean(acc_scores) * 100, np.std(acc_scores) * 100))

        get_majority_baseline(y_train, y_test)

    if args.analyze_features:
        analyze(args)

    # print out parameters
    for (a, v) in vars(args).items():
        print(a, v)


def train_eval(args, X_train, y_train, X_test, y_test):

    classifier = LinearSVC(C=args.C)
    
    classifier.fit(X_train, y_train)
    print(classifier.classes_)

    y_predicted_test = classifier.predict(X_test)
    y_predicted_train = classifier.predict(X_train)

    accuracy_dev = accuracy_score(y_test, y_predicted_test)
    accuracy_train = accuracy_score(y_train, y_predicted_train)
    print("Classifier accuracy train: {0:.2f}".format(accuracy_train*100))


    print("===== dev set ====")
    print("Classifier: {0:.2f}".format(accuracy_dev*100))

    print(classification_report(y_test, y_predicted_test, digits=4))

    return f1_score(y_test, y_predicted_test, average="weighted"), accuracy_score(y_test, y_predicted_test), y_predicted_test

def get_majority_baseline(y_train, y_test):
    print("===")
    majority_label = Counter(y_train).most_common()[0][0]
    maj = [majority_label for x in range(len(y_test))]

    print("first instance")
    f1_maj, acc_maj = f1_score(y_test, maj, average="weighted"), accuracy_score(y_test, maj)
    print("Majority weighted F1: {0:.2f} acc: {1:.2f}".format(f1_maj * 100, acc_maj * 100))


def vectorize_data(args, test=False, get_mapping_org_transformed=False):
    """
    :param args:
    :param X_train:
    :param X_test:
    :param get_mapping_org_transformed: True: keeps mapping original to transformed feature
    :return:
    """
    print("vectorize data..")

    df_data = json.load(open(args.data))
    ## if test file is give
    X_train = np.array(df_data["tweets"])
    y_train = np.array(df_data["gender"])

    if test:
        df_data_test = json.load(open(args.test))
        X_test = df_data_test["tweets"]
        y_test = df_data_test["gender"]

    if args.embeds:
        print("load embeddings")
        emb = load_embeddings(args.embeds)        

    dictVectorizer = DictVectorizer()

    if not args.embeds:
        vectorizerWords = Featurizer(word_ngrams=args.n_gram, char_ngrams=args.c_n_gram, binary=args.tf_idf,
                                 rm_user_url=args.rm_uu)
        X_train_dict = vectorizerWords.fit_transform(X_train)
        if test:
            X_test_dict = vectorizerWords.transform(X_test)
    else:
        emb_vectorizer = EmbedsFeaturizer(emb, only_mean=args.only_mean)
        X_train_dict = emb_vectorizer.fit_transform(X_train)

        if test:
            X_test_dict = emb_vectorizer.fit_transform(X_test)


    X_train = dictVectorizer.fit_transform(X_train_dict)
    if test:
        X_test = dictVectorizer.transform(X_test_dict)

    if args.tf_idf:
        tfIdfTransformer = TfidfTransformer(sublinear_tf=True)

        X_train = tfIdfTransformer.fit_transform(X_train)
        if test:
            X_test = tfIdfTransformer.transform(X_test)

    print("Vocab size:", len(dictVectorizer.vocabulary_))

    if args.show_instance:
        print("first instance")
        print(X_train_dict[0])
    if test:
        return X_train, y_train, X_test, y_test, dictVectorizer
    else:
        return X_train, y_train, dictVectorizer


def analyze(args):
    """ train SVM and get feature weights"""

    # create directory
    output_dir = args.analyze_features + "/" + os.path.basename(args.data)
    if os.path.dirname(output_dir) and not os.path.exists(os.path.dirname(output_dir)):
        os.makedirs(os.path.dirname(output_dir))

    classifier = LinearSVC(C=args.C)

    X_train, y_train, dictVectorizer = vectorize_data(args, get_mapping_org_transformed=True)
    classifier.fit(X_train, y_train)
    print(classifier.classes_)

    ## notice: this works as of now only for the transformed data, as it fetches original for an approx. mapping
    if args.data.endswith(".balanced"):
        original_texts = json.load(open(args.data))['tweets']
    elif args.data.find(".comb") > 0:
        original_texts = json.load(open(args.data.replace('comb', 'combOrig')))['tweets']
    else:
        original_texts = json.load(open('.'.join(args.data.split('.')[:-1])))['tweets']
    transformed_texts = json.load(open(args.data))['tweets']

    print(stats.describe(classifier.coef_[0]))
    print(classifier.classes_)
    lowest = sorted(zip(classifier.coef_[0], dictVectorizer.get_feature_names()))[:100]
    highest = sorted(zip(classifier.coef_[0], dictVectorizer.get_feature_names()), reverse=True)[:100]
    feats = dict([(e[1], {}) for e in highest + lowest])
    extract_feats(args, feats, original_texts, transformed_texts)

    OUT = open(output_dir, "w")
    for (coef1, pattern1), (coef2, pattern2) in zip(lowest, highest):
        OUT.write(str(coef1) + ' ' + pattern1)
        OUT.write((80 - len(str(coef1) + ' ' + pattern1)) * ' ')
        OUT.write(str(coef2) + ' ' + pattern2 + '\n')
        for (a1, b1), (a2, b2) in zip(sorted(feats[pattern1].items(), key=lambda x: -x[1])[:100],
                                      sorted(feats[pattern2].items(), key=lambda x: -x[1])[:100]):
            OUT.write(a1 + (80 - len(a1)) * ' ')
            OUT.write(a2 + '\n')
        OUT.write('\n')


def extract_feats(args, feats,original,transformed):
    """
    get mapping between transformed and original features (to later extract most frequent ones)
    (assumes same strategy as in Featurizer)
    """
    lower, upper = get_size_tuple(args.n_gram)
    if args.c_n_gram != "0":
        c_lower, c_upper = get_size_tuple(args.c_n_gram)
    for otext,ttext in zip(original,transformed):
        for otweet,ttweet in zip(otext.split(TWEET_DELIMITER),ttext.split(TWEET_DELIMITER)):
            if len(otweet.split(' ')) != len(ttweet.split(' ')):
                print('DIFF LEN:', otweet, ttweet)
                continue
            # word n-grams
            for n in range(lower, upper + 1):
                if args.rm_uu:
                    otweet = otweet.replace("USER", "")
                    otweet = otweet.replace("URL", "")
                    ttweet = ttweet.replace("USER", "")
                    ttweet = ttweet.replace("URL", "")
                for ongram,tngram in zip(nltk.ngrams(otweet.split(" "), n),nltk.ngrams(ttweet.split(" "), n)):
                    #print(ongram, tngram)
                    tngram = "{}_{}".format(PREFIX_WORD_NGRAM, "_".join(tngram))
                    ongram=' '.join(ongram).lower()
                    if tngram in feats:
                        feats[tngram][ongram]=feats[tngram].get(ongram,0)+1
            if args.c_n_gram != "0":
                ## character n-grams
                for n in range(c_lower, c_upper + 1):
                    if args.rm_uu:
                        otweet = otweet.replace("USER", "")
                        otweet = otweet.replace("URL", "")
                        ttweet = ttweet.replace("USER", "")
                        ttweet = ttweet.replace("URL", "")
                    for ongram, tngram in zip(nltk.ngrams(otweet, n), nltk.ngrams(ttweet, n)):
                        # print(ongram, tngram)
                        tngram = "{}_{}".format(PREFIX_CHAR_NGRAM, "_".join(tngram))
                        ongram = ' '.join(ongram).lower()
                        if tngram in feats:
                            feats[tngram][ongram] = feats[tngram].get(ongram, 0) + 1


def load_embeddings(path_file):
    emb = {}
    for line in codecs.open(path_file, encoding="utf-8", errors='ignore'):
        try:
            fields = line.strip().split()
            vec = [float(x) for x in fields[1:]]
            word = fields[0]
            if len(vec) == 100:
                emb[word] = vec
            else:
            #if len(vec) != 100:
                print(word, " - issue with vector")
        except ValueError:
            continue
    print("embeddings loaded ({})".format(len(emb)))
    return emb

if __name__=="__main__":
    main()

