from sklearn import datasets
from sklearn.svm import SVC
from sklearn.datasets import load_iris


iris = load_iris()

X, y = iris.data, iris.target

clf = SVC(gamma='scale')
clf.fit(X, y)
print('train Done!')
