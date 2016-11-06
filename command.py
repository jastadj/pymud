import game
import user
import server
import room
import item

commands = []


class command(object):
	def __init__(self, name, helpstr, fptr, argc = 0):
		self.name = name
		self.helpstr = helpstr
		self.__fptr = fptr
		self.argc = argc
	def execute(self, tuser, *argv):
		if self.__fptr == None:
			pass
		elif self.argc == 0:
			self.__fptr(tuser)
		else:
			if len(argv[0]) != self.argc:
				tuser.send("Invalid parameters!\n")
			else:
				self.__fptr(tuser, argv[0][0])

def getCommand(str):
	for i in range(0, len(commands)):
		if commands[i].name == str:
			return commands[i]
	return None
	
def showHelp(tuser):
	tuser.send("Help Menu\n")
	tuser.send("---------\n")
	for i in range(0, len(commands) ) :
		tuser.send("%s - %s\n" %(commands[i].name, commands[i].helpstr) )

def doSaveServer(tuser):
	server.saveServer()
	
def doEditRoom(tuser):
	room.getCurrentRoom(tuser).userEdit(tuser)
	
def doShutdownServer(tuser):
	server.shutdownServer(tuser)

def doMoveNorth(tuser):
	game.moveInDir(tuser, 0)
def doMoveSouth(tuser):
	game.moveInDir(tuser, 1)
def doMoveEast(tuser):
	game.moveInDir(tuser, 2)
def doMoveWest(tuser):
	game.moveInDir(tuser, 3)


def doDebug(tuser):
	tuser.send("Doing debug...\n")
	
	room.getCurrentRoom(tuser).show()

commands.append( command("help", "Show help menu", showHelp) )
commands.append( command("shutdown", "Shutdown server", doShutdownServer) )
commands.append( command("save", "Save Server Data", doSaveServer) )
commands.append( command("look", "Look around", room.lookRoom) )
commands.append( command("editroom", "Edit room data", doEditRoom) )
commands.append( command("quit", "Logout", None) )
commands.append( command("debug", "do something", doDebug) )
commands.append( command("n", "Move North", doMoveNorth) )
commands.append( command("s", "Move South", doMoveSouth) )
commands.append( command("e", "Move East", doMoveEast) )
commands.append( command("w", "Move West", doMoveWest) )


