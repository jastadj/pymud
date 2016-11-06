from tools import *

def addnums(*args):
	print "args:"
	for arg in args[0]:
		print arg


class myclass(object):
	count = 0
	
	def __init__(self, data):
		print "item created..."
		self.data = data
		myclass.count += 1

print "mycount = " + str(myclass.count)
mylist = []
mylist.append( myclass(5))
print "mycount = " + str(myclass.count)

f = addnums

mystr = "1 2 3"
words = mystr.split()

f(words)
print "\n\n\n"
db = {}
db.update( {"john":"june"})
db.update( {"mel":"july"})
db.update( {"alyssa":"january"})
db.update( {"john":"october"})

if "john" in db:
	print db["john"]
	

