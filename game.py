import server
import room
import user
import item
from tools import *
import command

def handleUser(tuser):
    userquit = False
    
    room.lookRoom(tuser)
    
    while not userquit:
        
        tuser.send(">")
        
        # get input from user
        data = tuser.conn.recv(1024)
        
        # data not valid, user disconnected?
        if not data:
            break
     
        
        words = data.split()
            
        if len(words) == 0:
            continue
        
        # parse command
        # find potential candidates
        poscmds = []
        for tw in command.commands:
            if tw.name.startswith(words[0]):
                poscmds.append( tw)
        
        if len(poscmds) > 1:
            for pc in poscmds:
                tuser.send("%s\n" %pc.name)
            continue
        elif len(poscmds) == 1:
            tcmd = poscmds[0]
        else:
            tcmd = None
        
        if tcmd == None:
            tuser.send("Unknown command!  Type \'help\'.\n")
        else:
            if len(words) == 1:
                tcmd.execute(tuser)
                if tcmd.name == "quit":
                    userquit = True
            else:
                tcmd.execute(tuser, words[1:])
                    
    tuser.send("Logging off...\n")
    print "User " + tuser.name + " logged off."
    tuser.conn.close()

def gameSay(tuser, msg):
    mystr = tuser.name + ": " + msg
    print mystr
    for uindex in range(0, len(user.users) ):
        if user.users[uindex] == tuser:
            tuser.send("You say \"%s\"\n" % msg )
        else:
            user.users[uindex].send(mystr + "\n")

def moveInDir(tuser, direction):
    if room.getCurrentRoom(tuser).exits[direction] == None:
        tuser.send("No exit to the %s!\n" % room.DIRECTIONS[direction])
        return
    if direction < 0 or direction >= len(room.DIRECTIONS):
        print "Error, user tried to move in direction " + str(direction)
        return
    
    tuser.currentRoom = room.getCurrentRoom(tuser).exits[direction]
    room.lookRoom(tuser)

def showInventory(tuser):
    invstr1 = "You are carrying:"
    invstr2 = "-----------------"
    
    tuser.send(invstr1 + "\n")
    tuser.send(invstr2 + "\n\n")
    
    invsize = len(tuser.inventory)
    
    if invsize == 0:
        tuser.send(" Nothing!\n")
    else:
        for i in range(0, invsize):
            tuser.send(" %s" % tuser.inventory[i].name )
    
