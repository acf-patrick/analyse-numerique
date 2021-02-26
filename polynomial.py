#-*- coding:utf-8 -*-

from math import isnan

def isnum(x):
	try:
		return not isnan(x)
	except TypeError:
		return False

class Polynomial:
	'''
		class representing polynomials
	
		instanciation :
		p = Polynomial(x0, x1, ..., xn)

		get/set the k-th coefficient :
		p[k-1] = value
		
		- support common operations :
		addition, substraction, multiplication of two polynomials or with a scalar
		- modifying coefficients will set the degree
		- decreasing the degree of the polynomial will set the list of coefficients as well
	'''

	def __init__(self, *coefficients):
		self._degree = len(coefficients)-1
		self._coefficient = list(coefficients)
		self._troncate()

	def __eq__(self, p):
		if isnum(p):
			return str(p) == str(self)
		elif isinstance(p, Polynomial):
			return self.coefficient == p.coefficient
		return False

	def __getitem__(self, index):
		return self._coefficient[index]
	def __setitem__(self, index, value):
		self._coefficient[index] = value
		self._troncate()

	def __len__(self):
		''' degree of the current polynomial '''
		return len(self.coefficient)-1

	def __call__(self, x):
		ret = 0
		for i, c in enumerate(self.coefficient):
			ret += c*x**i

		return ret

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		if not self._degree:
			# just a number
			return str(self[0])

		ret = ''
		for i in range(self._degree, -1, -1):
			c = self[i]
			if not c:
				continue

			if i == self._degree:
				if c == -1:
					ret += '-x'
				elif c == 1:
					ret += 'x'
				else:
					ret += '{}*x'.format(c)
				if i > 1:
					ret += str(i)
			else:
				ac = abs(c)
				ret += ' {} '.format('-' if c<0 else '+')
				if i > 0:
					if ac != 1:
						ret += '{}*'.format(ac)
					ret += 'x{}'.format(i if i>1 else '')
				else:
					ret += str(ac)

		return ret

	def __neg__(self):
		return Polynomial(*[-x for x in self._coefficient])

	def __rsub__(self, p):
		return self - p
	def __sub__(self, p):
		return self + (-p)

	def __radd__(self, p):
		return self + p
	def __add__(self, p):
		t = type(p)
		p = self.convert(p)

		if p == None:
			raise TypeError('Can not add polynomial with {}'.format(t))

		p = [self, p]
		if p[0]._degree < p[1]._degree:
			p.reverse()

		ret = Polynomial()
		ret._degree = p[0]._degree
		ret._coefficient = [0]*(1+ret._degree)
		for i in range(ret._degree+1):
			ret._coefficient[i] = p[0][i] + (0 if i > p[1]._degree else p[1][i])

		ret._troncate()
		return ret

	def __rtruediv__(self, p):
		return self/p
	def __truediv__(self, p):
		if isnum(p):
			if not p:
				raise ZeroDivisionError
			return self*(1/p)
		else:
			raise TypeError('Can not divide polynomial with {}'.format(t))

	def __rmul__(self, p):
		return self*p
	def __mul__(self, p):
		t = type(p)
		p = self.convert(p)

		if p == None:
			raise TypeError('Can not multiply polynomial with {}'.format(t))

		ret = Polynomial()
		ret._degree = self._degree + p._degree
		ret._coefficient = [0]*(1+ret._degree)

		p = [self, p]
		if p[0]._degree < p[1]._degree:
			p.reverse()

		for i in range(p[1]._degree+1):
			for j in range(p[0]._degree+1):
				ret._coefficient[i+j] += p[0][j] * p[1][i]

		ret._troncate()
		return ret

	def convert(self, x):
		'''
			convert a number to polynomial object
		'''
		if isinstance(x, Polynomial):
			return x

		elif isnum(x):
			return Polynomial(x)

		return None

	def _troncate(self):
		for i in range(self._degree, 0, -1):
			if self[i]:
				break
			del self._coefficient[-1]
		self._degree = len(self._coefficient)-1

	@property
	def coefficient(self):
		return self._coefficient

	@coefficient.setter
	def coefficient(self, value):
		self._degree = len(value)-1
		self._coefficient = list(value)

		self._troncate()

	def set_degree(self, value):
		'''
			the new value must be lower than the current polynomial degree
		'''
		if value == self._degree:
			return

		if value >= 0 and value < self._degree:
			self._degree = value
			self._coefficient = self.coefficient[0:value+1]

		self._troncate()
