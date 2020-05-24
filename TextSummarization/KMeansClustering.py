import numpy as np
import pandas as pd
from cltk.stop.classical_hindi.stops import STOPS_LIST
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from TextSummarization.HindiTokenizer import Tokenizer


dataset = pd.read_csv("dataset/manual-dataset/csv-files/newsfiles.csv")


def determineSentiment(summary):
    t = Tokenizer()

    stemmed_dataset = []

    for i in range(len(dataset)):
        stemmed_array = dataset['Sentences'][i].split()
        stemmed = [t.generate_stem_words(word) for word in stemmed_array if not word in set(STOPS_LIST)]
        stemmed = ' '.join(stemmed)
        stemmed_dataset.append(stemmed)


    cv = CountVectorizer()
    X = cv.fit_transform(stemmed_dataset)

    sent = pd.read_csv(
        "dataset/manual-dataset/csv-files/sentilist.csv")


    y = np.array(sent)
    z = np.zeros((max(y.shape), max(y.shape)))
    z[:y.shape[0], :y.shape[1]] = y
    y = z

    kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=50, n_init=10, random_state=0, verbose=True)
    kmeans.fit(summary)

    distances = np.column_stack([np.sum((summary - center) ** 2, axis=1) ** 0.5 for center in kmeans.cluster_centers_])
    svm = SVC().fit(distances, y)

    print(svm)












