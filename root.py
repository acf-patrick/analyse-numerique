#-*- coding:utf-8 -*-

from math import inf, log, ceil

class Solver:
	"""
	base class for all methods
	 - the attribute 'progression' is the sequence storing the whole process
	"""
	def __init__(self, f, max_iteration, tolerance):
		self.function = f
		self.max_iteration = max_iteration
		self.progression = []
		self.epsilon = tolerance
		self.approximation = None

	def __repr__(self):
		return self.__str__()

	def __str__(self):
		if self.approximation == None:
			return type(self).__name__ + " instance"

		e = ".{}f".format(ceil(-log(self.epsilon, 10)))
		body = ""
		for i, x in enumerate(self.progression):
			body += "{}\t{}\t{}\n".format(i, format(x, e), format(self.function(x), e))
		
		sep = ""
		head = ""
		h = 'i', "xi", "f(xi)"
		l = body.split('\n')[0].split('\t')
		for i, s in enumerate(l):
			head += h[i] + ' '*(len(s) - len(h[i])) + '\t'
			sep += '-'*(len(s) + 4)
		head += '\n'; sep += '\n'

		return head + sep + body + sep + \
			"Approximated solution: {}\n".format(format(x, e)) +\
			"Error evaluation: {:.3e}\n".format(self.error())

	def __setattr__(self, name, value):
		if name == "function":
			# we have a new equation
			self.progression = []
			self.approximation = None

		self.__dict__[name] = value

	def _instruction(self):
		print ("maximum iteration has been reached!")
		print ("if you want to get more precise approximation, increase the max_teration attribute")

	def compute(self):
		"""
		calculate the approximation
		"""
		return None

	def error(self):
		"""Error given by the approximation"""
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

	def __str__(self):
		if self.approximation == None:
			return type(self).__name__ + " instance"

		e = ".{}f".format(ceil(-log(self.epsilon, 10)))
		body = ""
		for i, x in enumerate(self.progression):
			m = self._mid(*x)
			body += "{}\t{}\t{}\t{}\n".format(i, format(x[0], e), format(x[1], e), format(self.function(m), e))
		
		sep = ""
		head = ""
		l = body.split('\n')[0].split('\t')
		h = 'i', "ai", "bi", "f(xi)"
		for i, s in enumerate(l):
			head += h[i] + ' '*(len(s) - len(h[i])) + '\t'
			sep += '-'*(len(s) + 4)
		head += '\n'; sep += '\n'

		return head + sep + body + sep + \
			"Approximated solution: {}\n".format(format(m, e)) +\
			"Error evaluation: {:.3e}\n".format(self.error())

	def _mid(self, a, b):
		return (a+b)/2

	def compute(self):
		f = self.function
		a, b = self.progression[-1]

		for i in range(len(self.progression), self.max_iteration):
			if abs(b - a) < self.epsilon or abs(self.function(self._mid(a, b))) < self.tolerance:
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

	def __init__(self, f, a, b, max_iteration = 100, tolerance = 1e-9):
		"""
		parameters :
		 - the function in the equation : f(x) = 0
		 - a, b : two abscissas forming the interval [a; b] where the solution should be
		"""

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

class FixedPoint(Solver):
	""" Fixed point iterative method """

	def __init__(self, f, x0, max_iteration = 100, tolerance = 1e-9):
		"""
		parameters :
		 - the function in the equation : f(x) = x
		 - starting point x0
		"""

		Solver.__init__(self, f, max_iteration, tolerance)
		self.progression = [x0]

	def compute(self):
		for i in range(len(self.progression), self.max_iteration):
			try:
				x = self.function(self.progression[-1])
			except ValueError:
				raise Exception("x = {}, math domain error! The sequence Xn+1 = f(Xn) diverges\n\
					Try with another starting point :\n method.progression = [x0]".format(x))

			if abs(x - self.progression[-1]) < self.epsilon:
				break

			self.progression.append(x)

		if i == self.max_iteration-1:
			self._instruction()

		self.approximation = self.progression[-1]
		return self.approximation

	def error(self):
		x = self.approximation
		if x == None:
			return inf

		return abs(self.function(x) - x)

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
