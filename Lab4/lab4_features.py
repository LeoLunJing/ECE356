import sys
import pandas
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix


import numpy as np

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.datasets import make_classification

from pprint import pprint

def main():
    data_filename = sys.argv[1]
    le = LabelEncoder()
    rawData = pandas.read_csv(data_filename)

    enc_data = rawData

    for key in enc_data.keys():
        enc_data[key] = le.fit_transform(enc_data[key])

    zero_importances = {}

    for i in range(0, 5):

        gini_data = []
        entropy_data = []

        train_set, test_set = train_test_split(enc_data, test_size=0.2)

        train_input = train_set.iloc[:, 1:-1]
        train_output = train_set.classification
        test_input = test_set.iloc[:, 1:-1]
        test_output = test_set.classification

        forest = DecisionTreeClassifier()
        
        forest.fit(train_input, train_output)
        importances = forest.feature_importances_
        indices = np.argsort(importances)[::-1]

#        print(rawData.columns)
#        print(importances[0])

#        print("\nFeature ranking:")

#        for (name, importance) in zip(rawData.columns[1:], importances):
#            print(name + ": " + str(importance) + "")

#        print("\nZero importances:")
        for (name, importance) in zip(rawData.columns[1:], importances):
            if importance < 0.0001:
#                print(name + ": " + str(importance) + "")
                if name not in zero_importances:
                    zero_importances[name] = 1
                else:
                    zero_importances[name] += 1

#    print("\n\nOverall Zero Importance Instances:")
    print("Overall Zero Importance Instances:")
    pprint(zero_importances)

    '''
    for f in range(train_input.shape[1]):
        print("%d. feature %d (%f)" % (f + 1, indices[f], importances[indices[f]]))
    '''







if __name__ == '__main__':
    main()

