
import json


datalist = []

def savedata():
	with open('data.txt', 'w') as outfile:
		json.dump(datalist, outfile)


class myclass(object):
	def __init__(self, data):
		self.data = data
	def show(self):
		print "data=" + str(self.data)
		
def initdata():
	datalist.append( myclass(3) )
	datalist.append( myclass(6) )
	datalist.append( myclass(1) )



if __name__ == "__main__":
	
	initdata()
	
	if type(datalist) is list:
		print "is list!"
	
	for dat in datalist:
		dat.show()
		
