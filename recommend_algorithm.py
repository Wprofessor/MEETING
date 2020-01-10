# 核心算法
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB


def dataInit():
    data = pd.read_excel('./data.xlsx')
    label = data.推荐会议室
    data = data.drop(['推荐会议室'], axis=1)
    data = pd.get_dummies(data)
    label_y = pd.factorize(label)
    return data, label_y[0], label_y[1]


def modelBYS(X, y):
    clf = MultinomialNB()
    model = clf.fit(X, y)
    return model


def predict(data=None):
    X, y, tag = dataInit()
    model = modelBYS(X, y)
    result = model.predict_proba(np.array(data).reshape(1,-1))

    result = sorted(enumerate(result[0]), key=lambda x: x[1], reverse=True)
    idx = [i[0] for i in result]
    real_result = [tag[i] for i in idx]
    return real_result


# if __name__ == '__main__':
#     print(predict())
