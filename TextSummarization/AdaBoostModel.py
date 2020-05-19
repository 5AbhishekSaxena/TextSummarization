from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import numpy as np



def classifier_builder(excel_file):
    columns = ['Sentence ID', 'Noun Feature', 'Sentence Length Feature', 'Number Feature', 'Relevance to title Feature',
               'Inverse Document Term Frequency Feature', 'Term Frequency Feature', 'Sentence Usefulness']
    custom_dataset = pd.read_excel(excel_file, names=columns)
    custom_dataset = custom_dataset._get_numeric_data()

    feature_list = np.array(custom_dataset)

    X = feature_list[:, [0, 1, 2, 3, 4, 5, 6]]
    y = feature_list[:, 7]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

    abc = AdaBoostClassifier(n_estimators=55, learning_rate=0.5)

    adamodel = abc.fit(X_train, y_train)

    y_pred = adamodel.predict(X_test)

    average_precision = metrics.average_precision_score(y_test, y_pred)

    print("Accuracy for the model: ", metrics.accuracy_score(y_test, y_pred))
    print("Precision score: ", metrics.precision_score(y_test, y_pred))
    print("Recall score: ", metrics.recall_score(y_test, y_pred))
    print("Average precision score: ", average_precision)
    #
    disp = metrics.plot_precision_recall_curve(abc, X_test, y_test)
    disp.ax_.set_title('2-class Precision-Recall curve: '
                       'AP={0:0.2f}'.format(average_precision))

    return adamodel





def generate_summary(test_excel_file):
    train_excel_file = "/Users/rajeshwari/Desktop/testarticles.xlsx"

    model = classifier_builder(train_excel_file)

    columns = ['Sentence ID', 'Noun Feature', 'Sentence Length Feature', 'Number Feature', 'Relevance to title Feature',
               'Inverse Document Term Frequency Feature', 'Term Frequency Feature']
    custom_dataset = pd.read_excel(test_excel_file, names=columns)

    custom_dataset = custom_dataset._get_numeric_data()

    feature_list = np.array(custom_dataset)

    X_test = feature_list[:, [0, 1, 2, 3, 4, 5, 6]]

    y_pred = model.predict(X_test)

    return y_pred

