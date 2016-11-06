import copy

items = []

class item(object):
	def __init__(self, name):
		self.name = name
	def show(self):
		print "Name:" + self.name

class weapon(item):
	def __init__(self, name, dmg):
		item.__init__(self, name)
		self.dmg = dmg
	def show(self):
		item.show(self)
		print "Dmg:" + self.dmg


def isItem(itm):
	if type(itm) is item:
		return True
	elif issubclass(type(itm), item):
		return True
	else:
		return False
	
def isWeapon(itm):
	if type(itm) is weapon:
		return True
	elif issubclass(type(itm), weapon):
		return True
	else:
		return False




# note , this isn't really copying anything
# need to import copy and do the right thing!
def copyItem(itemindex):
	global items
	
	if itemindex < 0 or itemindex >= len(items):
		return None
	
	return copy.copy(items[itemindex])

#debug
items.append( item("rock") )
