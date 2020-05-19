import pandas as pd
from TextSummarization import nltk_implementation as ck
import numpy as np
from cltk.tokenize.sentence import TokenizeSentence
from matplotlib import pyplot as plt
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from TextSummarization.HindiTokenizer import Tokenizer
import TextSummarization.ProcessStopwords
from cltk.stop.classical_hindi.stops import STOPS_LIST
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import SVC
from sklearn.mixture import GaussianMixture

dataset = pd.read_csv("/Users/rajeshwari/Documents/TextSummarization/TextSummarization/dataset/manual-dataset/csv-files/newsfiles.csv")
print(dataset.head())

t = Tokenizer()

stemmed_dataset = []

for i in range(len(dataset)):

    stemmed_array = dataset['Sentences'][i].split()
    stemmed = [t.generate_stem_words(word) for word in stemmed_array if not word in set(STOPS_LIST)]
    stemmed = ' '.join(stemmed)
    stemmed_dataset.append(stemmed)

print(stemmed_dataset[0:5])

cv = CountVectorizer()
X = cv.fit_transform(stemmed_dataset)

wcss = []

sent = pd.read_csv("/Users/rajeshwari/Documents/TextSummarization/TextSummarization/dataset/manual-dataset/csv-files/sentilist.csv")
print(sent.head())

y = np.array(sent)
z = np.zeros((max(y.shape), max(y.shape)))
z[:y.shape[0],:y.shape[1]] = y
y = z

# k = np.zeros((max(X.shape), max(X.shape)))
# k[:X.shape[0],:k.shape[1]] = X
# y = z

kmeans = KMeans(n_clusters=2, init='k-means++', max_iter=50, n_init=10, random_state=0, verbose=True)
kmeans.fit(X)

distances = np.column_stack([np.sum((X - center) ** 2, axis=1) ** 0.5 for center in kmeans.cluster_centers_])
svm = SVC().fit(distances, y)

true_k = 3
model = KMeans(n_clusters=true_k, init='k-means++', n_init=1)
model.fit(X)



plt.plot(range(1, 141), wcss)
plt.title("The elbow method")
plt.xlabel("No. of clusters")
plt.ylabel("wcss")
plt.show()
plt.imshow()


print("Top terms per cluster: ")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = cv.get_feature_names()
indices = np.random.choice(range(len(order_centroids)), replace=False, size=50000)
out_images = np.array(order_centroids)[indices.astype]
# for x in range(true_k):
#     print("Cluster %d: " % i),
#     for ind in out_images:
#         print(terms[ind]),
#     print
#
# print("\n")

