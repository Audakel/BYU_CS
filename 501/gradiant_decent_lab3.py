#%matplotlib inline
import matplotlib.pyplot as plt
import numpy as np

# Steps
# 1 - Calculate the score
# 2 - Calculate the loss
# 3 - Calculate the gradient
# 4 - Update the parameters

class Basic_Network(object):
    def __init__(self, X, Y, classes, step=0.01, delta=0.000001, epochs=100):
        self.step = step
        self.epochs = epochs
        self.classes = classes
        self.delta = delta
        self.X = X
        self.Y = Y


    def train(self):
        self.softmax_loss = []
        self.W = np.random.rand(self.classes, (1 + self.X.shape[1]))
        for _ in range(self.epochs):
            if (_ % 100 == 0):
                print 'We at: ', _
            loss_function_value, grad = self.gradient(self.W)
            self.W -= self.step * grad
            self.softmax_loss.append(loss_function_value)

        return self


    def gradient(self, W):
        # evaluate function value at original point
        fx = self.loss(W)
        gradient = np.zeros(W.shape)
        # iterate over all indexes in x
        it = np.nditer(W, flags=['multi_index'], op_flags=['readwrite'])
        while not it.finished:
            # evaluate function at x+h
            ix = it.multi_index
            old_value = W[ix]
            # increment by delta
            W[ix] = old_value + self.delta
            # evalute f(x + h)
            fxh = self.loss(W)
            # restore to previous value
            W[ix] = old_value
            # compute the partial derivative
            gradient[ix] = (fxh - fx) / self.delta # the slope
            it.iternext() # step to next dimension

        return fx, gradient


    def score(self, W):
        return np.dot(np.array(self.X), W[:, 1:]) + W[:,0]


    def accuracy(self, W):
        scores = self.score(W)
        scores = np.argmax(scores, axis=1)



    def loss(self, W):
        # first shift the values of f so that the highest number is 0:
        scores = self.score(W)
        scores -= np.array([np.amax(scores, axis=1)]).T
        # raise to e^x
        ex = np.exp(scores)
        # normalize to 1
        nex = ex / ex.sum(axis=0)
        nexln = -np.log(nex)
        one_hot_array = np.zeros(self.X.shape)
        one_hot_array[np.arange(self.X.shape[0]), np.array(self.Y).T] = 1

        # find average loss of all
        return ((nexln * one_hot_array)).flatten().sum() / self.Y.shape[0]



# =============================================
#
# load cifar-10-small and project down
#

def unpickle( file ):
    import cPickle
    fo = open(file, 'rb')
    dict = cPickle.load(fo)
    fo.close()
    return dict

data = unpickle( 'cifar-10-batches-py/data_batch_1' )

features = data['data']
labels = data['labels']
labels = np.atleast_2d( labels ).T

N = 1000
D = 10

# only keep N items
features = features[ 0:N, : ]
labels = labels[ 0:N, : ]

# project down into a D-dimensional space
features = np.dot( features, np.random.randn( 3072, D))

# whiten our data - zero mean and unit standard deviation
features = (features - np.mean(features)) / np.std(features)


bn = Basic_Network(X=features, Y=labels, classes=10)
bn.train()


plt.plot(range(1, len(bn.softmax_loss) + 1), bn.softmax_loss, marker='o')
plt.xlabel('Iterations')
plt.ylabel('softmax_loss')
plt.show()