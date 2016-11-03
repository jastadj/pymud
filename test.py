class BaseClass(object):
	def __init__(self, val):
		self.val = val
	def show(self):
		print "I am base"
		print self.val

class Derived(BaseClass, object):
	def __init__(self, val, val2):
		BaseClass.__init__(self, val)
		self.val2 = val2
	def show(self):
		BaseClass.show(self)
		print "I am derived"
		print self.val2

mybase = BaseClass(5)
mybase.show()

mydv = Derived(5,3)
mydv.show()
