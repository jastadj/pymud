class myclass(object):
	count = 0
	def __init__(self, data):
		print "myclass contructor..."
		myclass.count += 1
		self.data = data
		
	def totalCount(self):
		print myclass.count
	
	def show(self):
		print "data=%d" % self.data


mylist = []
mylist.append( myclass(3))
mylist.append( myclass(77))

print "total count = %d" %myclass.count

for i in mylist:
	i.show()

print "Creating and appending new item"
newitem = myclass(19)

mylist.append(newitem)

newitem.show()
newitem2 = newitem
newitem2.show()

newitem2.data = 69
print "\n"
newitem.show()
newitem2.show()
