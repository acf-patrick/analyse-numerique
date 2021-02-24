#-*- coding:utf-8 -*-
from math import log, inf

class Solver:
	"""
	base class for all methods
	"""
	def __init__(self, f, max_iteration, tolerance):
		self.function = f
		self.max_iteration = max_iteration
		self.progression = []
		self.epsilon = tolerance
		self.approximation = None

	def compute(self):
		"""
		calculate the approximation
		"""
		return None

	def error(self):
		return abs(self.function(self.approximation)) if self.approximation != None else inf

class Bisection(Solver):
	""" Bisection Method """

	def __init__(self, f, a, b, max_iteration = 100, tolerance = 1e-10):
		"""
			parameters :
			 - the function in the equation : f(x) = 0
			 - a, b : two abscissas forming the interval to start with
		"""

		if f(a)*f(b) > 0:
			raise Exception("There is no solution for the equation f(x) = 0 in the interval [{}, {}]".format(a, b))

		Solver.__init__(self, f, max_iteration, tolerance)
		self.progression = [(a, b)]

	def compute(self):
		f = self.function
		a, b = self.progression[-1]

		for i in range(len(self.progression)-1, self.max_iteration):
			if abs(b - a) < self.epsilon:
				break

			m = (a+b)/2
			if f(a)*f(m) < 0:
				b = m
			else:
				a = m

			self.progression.append((a, b))

		if i == self.max_iteration-1:
			print ("maximum iteration has been reached!")
			print ("if you want to get more precise approximation, increase the max_teration attribute")

		self.approximation = m
		return m