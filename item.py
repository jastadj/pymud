
items = []

class Item(object):
	def __init__(self, name):
		self.name = name

# note , this isn't really copying anything
# need to import copy and do the right thing!
def copyItem(itemindex):
	global items
	
	if itemindex < 0 or itemindex >= len(items):
		return None
	
	return items[itemindex]

#debug
items.append( Item("rock") )
