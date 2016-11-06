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
        data = tuser.receive(1024)
        
        # data not valid, user disconnected?
        if not data:
            break
     
        
        words = data.split()
            
        if len(words) == 0:
            continue
        
        # parse command
        # store possible cmd candidates here
        poscmds = []
        
        # check user aliases
        if words[0] in tuser.cred.cmdaliases:
			words[0] = tuser.cred.cmdaliases[words[0]]
        
        # check input string for partial or equal matches
        for tw in command.commands:
            if tw.name.startswith(words[0]):
                poscmds.append( tw)
                #if command is exact match
                if words[0] == tw.name:
                    poscmds = [tw]
                    break
        
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
                print words
                tcmd.execute(tuser, words[1:])
                    

def gameSay(tuser, msg):
    for usr in room.getUsersInRoom( room.getCurrentRoom(tuser) ):
        if usr == tuser:
            saystr = "You say \"%s\"" %msg
        else:
            saystr = "\n" + usr.cred.ulogin + " says \"%s\"" % msg
        usr.send(saystr + "\n")

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
    
