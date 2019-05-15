import sys
import pandas
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix

def metrics_to_str(iteration, accuracy, recall, precision, f1, cm):
    metrics_str = str(iteration)
    metrics_str += "," + str(accuracy)
    metrics_str += "," + str(recall)
    metrics_str += "," + str(precision)
    metrics_str += "," + str(f1)
    metrics_str += "," + str(cm).replace('\n', '')
    return metrics_str


def classification_to_str(iteration, test_output, test_predict):
    class_str = ""
    for (output, predict) in zip(test_output.to_list(), test_predict):
        class_str += str(iteration)
        class_str += "," + str(output)
        class_str += "," + str(predict)
        class_str += "\n"
    return class_str


def train_and_test(iteration, enc_data, criterion):
    train_set, test_set = train_test_split(enc_data, test_size=0.2)

    '''
    print(enc_data.keys())
 ['playerID', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS',
       'BB', 'SO', 'IBB', 'HBP', 'SH', 'SF', 'GIDP', 'Sum(P.W)', 'Sum(P.L)',
       'Sum(P.G)', 'Sum(P.SHO)', 'Sum(P.SV)', 'Sum(P.IPouts)', 'Sum(P.H)',
       'Sum(P.ER)', 'Sum(P.HR)', 'Sum(P.BB)', 'Sum(P.SO)', 'AVG(P.BAOpp)',
       'AVG(P.ERA)', 'Sum(P.IBB)', 'Sum(P.WP)', 'Sum(P.HBP)', 'Sum(P.BK)',
       'Sum(P.BFP)', 'Sum(P.GF)', 'Sum(P.R)', 'Sum(P.SH)', 'Sum(P.SF)',
       'Sum(P.GIDP)', 'classification']
    data_attributes = []
    train_input = train_set.loc[:, data_attributes]
    '''

    train_input = train_set.iloc[:, 1:-1]
    train_output = train_set.classification
    test_input = test_set.iloc[:, 1:-1]
    test_output = test_set.classification

#    print("\nTrain Input:")
#    print(train_input)

#    print("\nTrain Output:")
#    print(train_output)

#    print("Test Input:")
#    print(test_input)

#    print("\nTest Output: ")
#    print(test_output)

    clf = DecisionTreeClassifier(criterion=criterion).fit(train_input, train_output)

    test_predict = clf.predict(test_input)
#    print("\nTest Predictions: ")
#    print(test_predict)

    accuracy = accuracy_score(test_output, test_predict)
    recall = recall_score(test_output, test_predict)
    precision = precision_score(test_output, test_predict)
    f1 = f1_score(test_output, test_predict)
    cm = confusion_matrix(test_output, test_predict)

    metrics_str = metrics_to_str(iteration, accuracy, recall, precision, f1, cm)
    classification_str = classification_to_str(iteration, test_output, test_predict)

    print(clf.criterion + ": " + metrics_str)

    return (clf, metrics_str, classification_str)


def test_classifier(iteration, clf, enc_data):
    train_set, test_set = train_test_split(enc_data, test_size=0.2)

    '''
    print(enc_data.keys())
 ['playerID', 'G', 'AB', 'R', 'H', '2B', '3B', 'HR', 'RBI', 'SB', 'CS',
       'BB', 'SO', 'IBB', 'HBP', 'SH', 'SF', 'GIDP', 'Sum(P.W)', 'Sum(P.L)',
       'Sum(P.G)', 'Sum(P.SHO)', 'Sum(P.SV)', 'Sum(P.IPouts)', 'Sum(P.H)',
       'Sum(P.ER)', 'Sum(P.HR)', 'Sum(P.BB)', 'Sum(P.SO)', 'AVG(P.BAOpp)',
       'AVG(P.ERA)', 'Sum(P.IBB)', 'Sum(P.WP)', 'Sum(P.HBP)', 'Sum(P.BK)',
       'Sum(P.BFP)', 'Sum(P.GF)', 'Sum(P.R)', 'Sum(P.SH)', 'Sum(P.SF)',
       'Sum(P.GIDP)', 'classification']
    data_attributes = []
    train_input = train_set.loc[:, data_attributes]
    '''

    test_input = test_set.iloc[:, 1:-1]
    test_output = test_set.classification

#    print("\nTrain Input:")
#    print(train_input)

#    print("\nTrain Output:")
#    print(train_output)

#    print("Test Input:")
#    print(test_input)

#    print("\nTest Output: ")
#    print(test_output)

    test_predict = clf.predict(test_input)
#    print("\nTest Predictions: ")
#    print(test_predict)

    accuracy = accuracy_score(test_output, test_predict)
    recall = recall_score(test_output, test_predict)
    precision = precision_score(test_output, test_predict)
    f1 = f1_score(test_output, test_predict)
    cm = confusion_matrix(test_output, test_predict)

    metrics_str = metrics_to_str(iteration, accuracy, recall, precision, f1, cm)
    classification_str = classification_to_str(iteration, test_output, test_predict)

    print(clf.criterion + ": " + metrics_str)

    return (metrics_str, classification_str)


def main():
    data_filename = sys.argv[1]

    le = LabelEncoder()
    rawData = pandas.read_csv(data_filename)

    enc_data = rawData

    for key in enc_data.keys():
        if key == "classification":
            # Ensure we know the correct encoded values
            enc_data[key] = enc_data[key].map({"Elected" : 1, "Nominated" : 0})
        else:
           enc_data[key] = le.fit_transform(enc_data[key])

    gini_data = []
    entropy_data = []

    (gini_clf, metrics_str, classification_str) = train_and_test(1, enc_data, "gini")
    gini_data.append([metrics_str, classification_str])
    (entropy_clf, metrics_str, classification_str) = train_and_test(1, enc_data, "entropy")
    entropy_data.append([metrics_str, classification_str])

    for i in range(2, 7):
        (metrics_str, classification_str) = test_classifier(i, gini_clf, enc_data)
        gini_data.append([metrics_str, classification_str])
        (metrics_str, classification_str) = test_classifier(i, entropy_clf, enc_data)
        entropy_data.append([metrics_str, classification_str])

    gini_csv = open("g10_DT_gini.csv", "w")

    gini_csv.write("Iteration,Accuracy,Recall Score,Precision,F1 Score,Confusion Matrix\n")
    for data in gini_data:
        gini_csv.write(data[0] + "\n")
    gini_csv.write("\n\n0,Nominated\n1,Elected\n")
    gini_csv.write("\n\nIteration,Classification,Prediction\n")
    for data in gini_data:
        gini_csv.write(data[1] + "\n")

    gini_csv.close()
    entropy_csv = open("g10_DT_entropy.csv", "w")
        
    entropy_csv.write("Iteration,Accuracy,Recall Score,Precision,F1 Score,Confusion Matrix\n")
    for data in entropy_data:
        entropy_csv.write(data[0] + "\n")
    entropy_csv.write("\n\n0,Nominated\n1,Elected\n")
    entropy_csv.write("\n\nIteration,Classification,Prediction\n")
    for data in entropy_data:
        entropy_csv.write(data[1] + "\n")
       
    entropy_csv.close() 

    export_graphviz(gini_clf, 'gini_tree.dot')
    export_graphviz(entropy_clf, 'entropy_tree.dot')


if __name__ == '__main__':
    main()

