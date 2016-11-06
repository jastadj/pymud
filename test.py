commandlist = []

class command(object):
	def __init__(self, name, fptr):
		self.name = name
		self.fptr = fptr
	
	def execute(self, *args):
		if self.fptr != None:
			if len(args) > 0:
				self.fptr(args[0][0])
			else:
				self.fptr("")








def getCommand(cstr):
	for i in range(0, len(commandlist) ):
		if cstr == commandlist[i].name:
			return commandlist[i]
	
	return None

def doLook(*args):
	
	if args[0] != "":
		for arg in args:
			print arg
	
	print "you see a room"





if __name__ == "__main__":
	
	doquit = False
	
	ch = ""
	
	commandlist.append( command("look", doLook) )
	
	while not doquit:
		
		try:
			ch = raw_input(">")
		except SyntaxError:
			pass
		
		
		if len(ch) == 0:
			continue
			
		words = ch.split()
			
		if words[0] == "quit" or words[0] == "q":
			doquit = True
		else:
			tcmd = getCommand(words[0])
			if tcmd != None:
				if len(words) > 1:
					tcmd.execute(words[1:])
				else:
					tcmd.execute()
			else:
				print "Not a valid command!"
