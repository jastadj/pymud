
items = []

class Item(object):
	def __init__(self, name):
		self.name = name

def copyItem(itemindex):
	global items
	
	if itemindex < 0 or itemindex >= len(items):
		return None
	
	return items[itemindex]

#debug
items.append( Item("rock") )
