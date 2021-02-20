class Polynome:
	def __init__(self, degree):
		self.deg = degree
		self.coef = [0]*(degree+1)

	def __getitem__(self, index):
		return self.coef[index]

	def __setitem__(self, index, value):
		self.coef[index] = value

	def __str__(self):
		return self.__repr__()

	def __repr__(self):
		ret = ''
		for i in range(self.deg, -1, -1):
			ret += str(self.coef[i])
			if i:
				ret += '.x{} + '.format(i)
		return ret

	def __add__(self, poly):
		