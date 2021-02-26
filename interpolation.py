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

		self._basis = []
		self._function = None
		self.interpolation = None

	@property
	def x(self):
		return self._x
	@x.setter
	def x(self, value):
		if len(value) != len(self._y):
			raise Exception("New value for x doesn't have the same length as y")

		self._x = value

		self._calculate_basis()

	@property
	def y(self):
		return self._y
	@y.setter
	def y(self, value):
		if len(value) != len(self._x):
			raise Exception("New value for y doesn't have the same length as x")

		self._y = value

		self._calculate_basis()
	
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

		self._calculate_basis()

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

		# self._calculate_basis()

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

	def _calculate_basis(self):
		Base._calculate_basis(self)

		x = self._x
		self._basis = [1]
		for k in range(1, len(x)):
			self._basis.append(self._basis[-1]*Polynomial(-x[k-1], 1))

	def compute(self):
		Base.compute(self)

		x, y = self._x, self._y

		# divided difference
		self._dd = [y]
		for i in range(1, len(x)):
			self._dd.append([])
			for j in range(len(x)-i):
				self._dd[i].append((self._dd[i-1][j+1]-self._dd[i-1][j])/(x[i+j]-x[j]))

#		for i in range(len(x)):
#			print (x[i], end = '\t')
#			for j in range(i+1):
#				print (self._dd[j][i-j], end = '\t')
#			print ('\n')

		self.interpolation = 0
		for i in range(len(x)):
			self.interpolation += self._dd[i][0]*self._basis[i]

		return self.interpolation
