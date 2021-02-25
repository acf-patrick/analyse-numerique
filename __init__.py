
class Mere:
	def __init__(self, attribute):
		self.attribute = attribute

	def __setattr__(self, name, value):
		print ('hello')
		self.__dict__[name] = value

class Fille(Mere):
	def __init__(self):
		Mere.__init__(self, 0)
		
f = Fille()