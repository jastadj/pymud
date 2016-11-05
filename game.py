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
        tcmd = command.getCommand(words[0])
        
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
