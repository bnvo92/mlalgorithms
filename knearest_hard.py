import numpy as np
from math import sqrt
import warnings
from matplotlib import style
from collections import Counter
import pandas as pd
from sklearn import preprocessing, cross_validation, neighbors
import random

def k_nearest_neighbors(data, predict, k=3):
    if len(data) >= k:
        warnings.warn('K set to value less than total voting groups')

    distances = []
    for group in data:
        for features in data[group]:
            ed = np.linalg.norm(np.array(features)-np.array(predict))
            distances.append([ed,group])

    votes = [i[1] for i in sorted(distances)[:k]]
    vote_result = Counter(votes).most_common(1)[0][0]
    confidence = Counter(votes).most_common(1)[0][1] / k
    return vote_result, confidence


accuracies = []

for i in range(25):
    df = pd.read_csv('breast-cancer-wisconsin.data.txt')
    df.replace('?', -99999, inplace=True)
    df.drop(['id'], 1, inplace=True)
    full_data = df.astype(float).values.tolist()
    random.shuffle(full_data)

    test_size = 0.2
    train_set = {2:[], 4:[]}
    test_set = {2:[], 4:[]}
    train_data = full_data[:-int(test_size*len(full_data))]
    test_data = full_data[-int(test_size*len(full_data)):]

    for i in train_data:
        train_set[i[-1]].append(i[:-1])
        
    for i in test_data:
        test_set[i[-1]].append(i[:-1])

    correct = 0
    total = 0

    for group in test_set:
        for data in test_set[group]:
            vote, confidence = k_nearest_neighbors(train_set, data, k=5)
            if group == vote:
                correct += 1

            total += 1
    accuracies.append(correct/total)

print(sum(accuracies)/len(accuracies))

##X = np.array(df.drop(['class'],1))
##y = np.array(df['class'])
##
##X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,test_size=0.2)
##
##clf = neighbors.KNeighborsClassifier()
##clf.fit(X_train,y_train)
