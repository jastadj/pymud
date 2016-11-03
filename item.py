items = []


class Item(object):
	def __init__(self, name):
		self.name = name


items.append( Item("rock") )

def copyItem(itemindex):
	global items
	
	if itemindex < 0 or itemindex >= len(items):
		return None
	
	return items[itemindex]
