import matplotlib.pyplot as plt
%matplotlib inline
from mlxtend.evaluate import plot_decision_regions
import numpy as np
import pandas as pd


class Perceptron(object):
    def __init__(self, step=0.01, epochs=100):
        self.step = step
        self.epochs = epochs

    def train(self, X, y):
        self.w_ = np.zeros(1 + X.shape[1])
        self.errors_ = []

        for _ in range(self.epochs):
            errors = 0
            for xi, target in zip(X, y):
                update = self.step * (target - self.predict(xi))
                self.w_[1:] += update * xi
                self.w_[0] += update
                errors += int(update != 0.0)

            self.errors_.append(errors)
        return self

    def net_input(self, xi):
        return np.dot(xi, self.w_[1:]) + self.w_[0]

    def predict(self, xi):
        return np.where(self.net_input(xi) >= 0.0, 1, -1)


iris = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)

# setosa and versicolor
y = iris.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)

# sepal length and petal length
X = iris.iloc[:100, :2].values

ppn = Perceptron(epochs=10, step=0.1)

ppn.train(X, y)
print('Weights: %s' % ppn.w_)
plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.show()

plt.plot(range(1, len(ppn.errors_) + 1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Missclassifications')
plt.show()
