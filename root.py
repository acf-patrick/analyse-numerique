#-*- coding:utf-8 -*-
from math import log, inf

class Solver:
	"""
	base class for all methods
	 - the attribute 'progression' is the sequence 
	"""
	def __init__(self, f, max_iteration, tolerance):
		self.function = f
		self.max_iteration = max_iteration
		self.progression = []
		self.epsilon = tolerance
		self.approximation = None

	def __setattr__(self, name, value):
		if name == "function":
			self.progression = []
			self.approximation = None
		self.__dict__[name] = value

	def compute(self):
		"""
		calculate the approximation
		"""
		return None

	def _instruction(self):
		print ("maximum iteration has been reached!")
		print ("if you want to get more precise approximation, increase the max_teration attribute")

	def error(self):
		return abs(self.function(self.approximation)) if self.approximation != None else inf

class Bisection(Solver):
	""" Bisection Method """

	def __init__(self, f, a, b, max_iteration = 100, tolerance = 1e-9):
		"""
		parameters :
		 - the function in the equation : f(x) = 0
		 - a, b : two abscissas forming the interval to start with
		"""

		if a > b:
			a, b = b, a

		if f(a)*f(b) > 0:
			raise Exception("There is no solution for the equation f(x) = 0 in the interval [{}, {}]".format(a, b))

		Solver.__init__(self, f, max_iteration, tolerance)
		self.progression = [(a, b)]

	def _mid(self, a, b):
		return (a+b)/2

	def compute(self):
		f = self.function
		a, b = self.progression[-1]

		for i in range(len(self.progression), self.max_iteration):
			if abs(b - a) < self.epsilon:
				break

			y = f(a), f(b)
			if not y[0]:
				m = a
				break
			elif not y[1]:
				m = b
				break

			m = self._mid(a, b)
			if y[0]*f(m) < 0:
				b = m
			else:
				a = m

			self.progression.append((a, b))

		if i == self.max_iteration-1:
			self._instruction()

		self.approximation = m
		return m

class Lagrange(Bisection):
	""" Variant of the bisection method """

	def __init__(self, f, a, b, max_iteration = 100, tolerance = 1e-9):
		Bisection.__init__(self, f, a, b, max_iteration, tolerance)

	def _mid(self, a, b):
		f = self.function
		return a - f(a)*(b-a)/(f(b)-f(a))

class Descartes(Solver):
	""" Secant method """

	def __init__(self, f, a, b = None, max_iteration = 100, tolerance = 1e-9):
		"""
		parameters :
		 - the function in the equation : f(x) = 0
		 - two abscissas a and b. If b not given, we put b = a + tolerance
		"""

		if b == None:
			b = a + tolerance

		if a > b:
			a, b = b, a

		Solver.__init__(self, f, max_iteration, tolerance)
		self.progression = [a, b]

	def compute(self):
		for i in range(len(self.progression), self.max_iteration):
			a, b = self.progression[-2:]
			ya, yb = self.function(a), self.function(b)

			if abs(b - a) < self.epsilon and yb < self.epsilon:
				break

			self.progression.append(b - yb*(b - a)/(yb - ya))

		if i == self.max_iteration-1:
			self._instruction()

		self.approximation = self.progression[-1]
		return self.approximation

class Newton(Solver):
	""" Newton-Raphson method """

	def __init__(self, f, df, x0, max_iteration = 100, tolerance = 1e-9):
		"""
		parameters :
		 - the function in the equation : f(x) = 0
		 - the derivative of the function f
		 - starting point x0
		"""

		Solver.__init__(self, f, max_iteration, tolerance)
		self.derivative = df
		self.progression = [x0]

	def compute(self):
		for i in range(len(self.progression), self.max_iteration):
			x = self.progression[-1]

			if i > 1:
				if abs(x - self.progression[-2]) < self.epsilon:
					break

			dy = self.derivative(x)
			if not dy:
				raise Exception("Since the derivative at x = {} is null, the sequence Xn+1 = Xn - f(Xn)/f'(Xn) given by\
				 the Newton method never converge")

			self.progression.append(x - self.function(x)/dy)

		if i == self.max_iteration-1:
			self._instruction()

		self.approximation = self.progression[-1]
		return self.approximation
