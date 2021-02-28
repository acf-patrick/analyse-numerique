#-*- coding:utf-8 -*-

from polynomial import Polynomial

class Base:
	"""
	Base class
	"""

	def __init__(self, x = [], y = []):
		"""
		parameters :
		 - x : list of abscissas
		 - y : list of ordinates. Must have the same length as x

		 You also can set the attribute function, y attribute will be filled automaticaly.
		"""

		self._x = [_ for _ in x]
		self._y = [_ for _ in y]

		self._init()
		self._function = None

	def _init(self):
		self._basis = []
		self.interpolation = None

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		ret = "<{} method>\n\n".format(type(self).__name__)
		ret += "basis :\n" + '-'*5 + '\n'
		if self._basis:
			for i, l in enumerate(self._basis):
				ret += "L{}(x) = {}\n".format(i, l)

		return ret + "\nInterpolation :\n" + '-'*11 + '\n' + str(self.interpolation) + '\n'

	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, value):
		if len(value) != len(self._y):
			raise Exception("New value for x doesn't have the same length as y")

		self._x = value
		self._init()

	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, value):
		if len(value) != len(self._x):
			raise Exception("New value for y doesn't have the same length as x")

		self._y = value
		self._init()
	
	@property
	def function(self):
		return self._function
	
	@function.setter
	def function(self, value):
		try:
			value.__call__
		except AttributeError:
			raise TypeError("must be a function")

		self._y = [value(x) for x in self._x]
		self._function = value
		self.interpolation = None

		self._init()

	def _instruction(self):
		raise Exception( "Basis not yet calculated. Provide a function or\
				 use the set method to fill the list of points!" )

	def _calculate_basis(self):
		if len(self._x) != len(self._y):
			self._instruction()

	def __getitem__(self, index):
		"""
		get the index-th vector in the appropriate basis
		"""
		try:
			return self._basis[index]
		except IndexError:
			if not self._basis:
				self._instruction()
			return None

	def set(self, *points):
		"""
		set the list of points
		"""
		for x, y in points:
			self._x.append(x)
			self._y.append(y)

		self._function = None
		self._init()

	def compute(self):
		"""
		calculate the interpolation
		"""
		if not self._basis:
			self._calculate_basis()

		return None

class Lagrange(Base):
	"""
	Interpolation using Lagrange's method
	"""

	def _calculate_basis(self):
		Base._calculate_basis(self)

		x = self._x
		for k in range(len(x)):
			p = 1
			for i in range(len(x)):
				if i == k:
					continue
				p *= Polynomial(-x[i], 1)/(x[k] - x[i])
			self._basis.append(p)

	def compute(self):
		Base.compute(self)

		self.interpolation = 0
		for k in range(len(self._x)):
			self.interpolation += self._y[k]*self._basis[k]

		return self.interpolation

class Newton(Base):
	"""
	Interpolation using Newton's method
	"""

	def __str__(self):
		s = super().__str__()
		s = s.split("\n\n")

		dd = "Divided differencies :\n"
		dd += '-'*len(dd[:-2]) + '\n'

		if self._dd:
			x = self._x
			for i in range(len(x)):
				dd += "{}\t| ".format(x[i])
				for j in range(i+1):
					dd += "{}\t".format(self._dd[j][i-j])
				dd += '\n'

		return "\n\n".join((*s[:-1], dd, s[-1]))

	def _init(self):
		super()._init()
		self._dd = []

	def _calculate_basis(self):
		Base._calculate_basis(self)

		x = self._x
		self._basis = [1]
		for k in range(1, len(x)):
			self._basis.append(self._basis[-1]*Polynomial(-x[k-1], 1))

	def divided_difference(self, k, n):
		"""
		get the divided difference f[xk, ..., xn]
		"""
		x, y = self._x, self._y

		if self._dd:
			if n < k:
				raise Exception("indice k must be smaller than n")
			return self._dd[n-k][k]
		
		self._dd = [y]
		for i in range(1, len(x)):
			self._dd.append([])
			for j in range(len(x)-i):
				self._dd[i].append((self._dd[i-1][j+1]-self._dd[i-1][j])/(x[i+j]-x[j]))

		return self.divided_difference(k, n)

	def compute(self):
		Base.compute(self)

		self.interpolation = 0
		for i in range(len(self._x)):
			self.interpolation += self.divided_difference(0, i)*self._basis[i]

		return self.interpolation
