from numpy.random import seed
import numpy as np
import pandas as pd
class AdalineSGD(object):
	"""ADAptive LInear NEuron classifier.
	Parameters
	------------
	eta : float
	Learning rate (between 0.0 and 1.0)
	n_iter : int
	Passes over the training dataset.
	Attributes
	-----------
	w_ : 1d-array
	Weights after fitting.
	errors_ : list
	Number of misclassifications in every epoch.
	shuffle : bool (default: True)
	Shuffles training data every epoch
	if True to prevent cycles.
	random_state : int (default: None)
	Set random state for shuffling
	and initializing the weights.
	"""
	def __init__(self, eta=0.01, n_iter=10,
		shuffle=True, random_state=None):
		self.eta = eta
		self.n_iter = n_iter
		self.w_initialized = False
		self.shuffle = shuffle
		if random_state:
			seed(random_state)
	def fit(self, X, y):
		""" Fit training data.
		Parameters
		----------
		X : {array-like}, shape = [n_samples, n_features]
		Training vectors, where n_samples
		is the number of samples and
		n_features is the number of features.
		y : array-like, shape = [n_samples]
		Target values.
		Returns
		-------
		self : object
		"""
		self._initialize_weights(X.shape[1])
		self.cost_ = []
		for i in range(self.n_iter):
			print("loop",i)
			if self.shuffle:
				X, y = self._shuffle(X, y)
			cost = []
			for xi, target in zip(X, y):
				cost.append(self._update_weights(xi, target))
			avg_cost = sum(cost)/len(y)
			self.cost_.append(avg_cost)
		#print(self.cost_)
		return self
	def partial_fit(self, X, y):
		"""Fit training data without reinitializing the weights"""
		if not self.w_initialized:
			self._initialize_weights(X.shape[1])
		if y.ravel().shape[0] > 1:
			for xi, target in zip(X, y):
				self._update_weights(xi, target)
		else:
			self._update_weights(X, y)
		return self
	def _shuffle(self, X, y):
		"""Shuffle training data"""
		r = np.random.permutation(len(y))
		return X[r], y[r]
	def _initialize_weights(self, m):
		"""Initialize weights to zeros"""
		self.w_ = np.zeros(1 + m)
		self.w_initialized = True
	def _update_weights(self, xi, target):
		"""Apply Adaline learning rule to update the weights"""
		output = self.net_input(xi)
		#print(output)
		error = (target - output)
		#print(error)
		self.w_[1:] += self.eta * xi.dot(error)
		print("w[1]",self.w_[1:])
		self.w_[0] += self.eta * error
		print("w[0]",self.w_[0])
		cost = 0.5 * error**2
		return cost
	def net_input(self, X):
		"""Calculate net input"""
		return np.dot(X, self.w_[1:]) + self.w_[0]
	def activation(self, X):
		"""Compute linear activation"""
		return self.net_input(X)
	def predict(self, X):
		"""Return class label after unit step"""
		return np.where(self.activation(X) >= 0.0, 1, -1)

df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)
X = df.iloc[0:100, [0, 2]].values
X_std = np.copy(X)
X_std[:,0] = (X[:,0] - X[:,0].mean()) / X[:,0].std()
X_std[:,1] = (X[:,1] - X[:,1].mean()) / X[:,1].std()
ad = AdalineSGD(n_iter=15, eta=0.01, random_state=1)
ad.fit(X_std,y)
# X,y = ad._shuffle(X_std, y)
# ad._initialize_weights(X.shape[1])
# #print(ad._update_weights(np.array([2,4]),np.array([1])))
# #ad.fit(X_std,y)
# for xi, target in zip(X_std, y):
	# print(ad._update_weights(xi,target))
	