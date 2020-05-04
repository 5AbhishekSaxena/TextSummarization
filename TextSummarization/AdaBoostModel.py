# Load libraries
from sklearn.ensemble import AdaBoostClassifier
from sklearn import datasets
# Import train_test_split function
from sklearn.model_selection import train_test_split
# Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
import pandas as pd
import numpy as np

excel_file = "/Users/rajeshwari/Desktop/article.xlsx"
columns = ['Sentence ID', 'Noun Feature', 'Sentence Length Feature', 'Number Feature', 'Relevance to title Feature', 'Sentence Usefulness']
custom_dataset = pd.read_excel(excel_file, columns=columns)
original_headers = list(custom_dataset.columns.values)
#print(original_headers)

# remove the non-numeric columns
custom_dataset = custom_dataset._get_numeric_data()

# put the numeric column names in a python list
numeric_headers = list(custom_dataset.columns.values)

# create a numpy array with the numeric values for input into scikit-learn
feature_list = np.array(custom_dataset)

#print(feature_list)

X = feature_list[:, [1, 2, 3, 4]]
y = feature_list[:, 5]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

abc = AdaBoostClassifier(n_estimators=50, learning_rate=1)

model = abc.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = model.predict(X_test)

print("Accuracy for the model: ", metrics.accuracy_score(y_test, y_pred))
print("Precision score: ", metrics.precision_score(y_test, y_pred))
print("Recall score: ", metrics.recall_score(y_test, y_pred))

summarized_sentence = ""

for i in y_pred:
    if (y_pred[i] == 1):
        summarized_sentence += X_test[i]

print(summarized_sentence)