from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np

if __name__ == "__main__":
    X = np.array([[-1, -1], [-2, -1], [1, 1], [2, 1]])
    y= np.array([0,0,1,1])
    # scaler = StandardScaler()
    # scaler.fit(X)
    # scaler.fit(y)
    # X = scaler.transform(X)
    # y = scaler.transform(y)
    clf = SGDClassifier(loss="log", penalty="l2")
    clf.fit(X, y)
    print clf.score(X,y)
    print(clf.predict([-1, -1]))
    print(clf.predict([-2, -1]))
    print(clf.predict([2,   1]))
    print(clf.predict([1,   1]))
    print(clf.predict([0,   1]))