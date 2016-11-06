import game
import user
import server
import room
import roomedit
import item
from tools import *

commands = []


class command(object):
    def __init__(self, name, helpstr, fptr, hasargs = False):
        self.name = name
        self.helpstr = helpstr
        self.__fptr = fptr
        self.hasargs = hasargs
    def execute(self, tuser, *argv):
        if self.__fptr == None:
            pass
        elif not self.hasargs:
            self.__fptr(tuser)
        else:
			# arguments provied
            if len(argv) > 0:
                self.__fptr(tuser, argv[0])
            else:
                self.__fptr(tuser, [""])

def getCommand(str):
    for i in range(0, len(commands)):
        if commands[i].name == str:
            return commands[i]
    return None
    
def showHelp(tuser):
    tuser.send("%sHelp Menu%s\n" % (setColor(tuser, COLOR_MAGENTA, True), resetColor(tuser) ) )
    tuser.send("%s---------%s\n" % ( setColor(tuser, COLOR_MAGENTA, False) , resetColor(tuser) ) )
    tuser.send("%s" % setColor(tuser, COLOR_GREEN) )
    for i in range(0, len(commands) ) :
        tuser.send("%s - %s\n" %(commands[i].name, commands[i].helpstr) )
    tuser.send("%s" % resetColor(tuser) )

def doSaveServer(tuser):
    server.saveServer()
    
def doEditRoom(tuser):
	roomedit.roomEdit(tuser, room.getCurrentRoom(tuser) )
    
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

def doLook(tuser, *args):
	# no arguments, look room
	if args[0][0] == "":
		room.lookRoom(tuser)
	# arguments found, look at thing
	else:
		for arg in args[0]:
			pass


def doDebug(tuser, *args):
    tuser.send("Doing debug...\n")
    
    room.getCurrentRoom(tuser).show()

def doShowInventory(tuser):
    game.showInventory(tuser)
    
def doWho(tuser):
	user.doWho(tuser)

def doSay(tuser, *args):
	
	# no arguments
	if args[0][0] == "":
		tuser.send("What the hell are you trying to say??\n")
	# arguments found
	else:
		smsg = unsplit(args[0])
		game.gameSay(tuser, smsg)
		for arg in args[0]:
			pass


commands.append( command("help", "Show help menu", showHelp) )
commands.append( command("shutdown", "Shutdown server", doShutdownServer) )
commands.append( command("save", "Save Server Data", doSaveServer) )
commands.append( command("look", "Look around", doLook, True) )
commands.append( command("editroom", "Edit room data", doEditRoom) )
commands.append( command("quit", "Logout", None) )
commands.append( command("debug", "do something", doDebug, True) )
commands.append( command("n", "Move North", doMoveNorth) )
commands.append( command("s", "Move South", doMoveSouth) )
commands.append( command("e", "Move East", doMoveEast) )
commands.append( command("w", "Move West", doMoveWest) )
commands.append( command("i", "Show inventory", doShowInventory ) )
commands.append( command("who", "Who is online", doWho) )
commands.append( command("say", "Say something", doSay, True) )
