import pickle
import user
from tools import *
import os.path
import item

rooms = []
roomsLoaded = False

DIRECTIONS = ["north", "south", "east","west"]

def getRoomID(troom):
    for i in range(0, len(rooms)):
        if troom  == rooms[i]:
            return i
    return None

class room(object):
    
    def __init__(self):
        self.name = "unnamed"
        self.desc = "no description"
        self.inventory = []
        
        # initialize all exits to none
        self.exits = []
        for i in range(0, len(DIRECTIONS)):
            self.exits.append(None)
    
    def getID(self):
        return getRoomID(self)
    
    def doValidate(self):
        hadtovalidate = False        
        return hadtovalidate
    
    def connectRoom(self, troom, tdir):
        # is direction free?
        if self.exits[tdir] != None:
            return False
        oppdir = None
        
        # get opposite room direction
        if tdir == 0:
            oppdir = 1
        elif tdir == 1:
            oppdir = 0
        elif tdir == 2:
            oppdir = 3
        elif tdir == 3:
            oppdir = 2
        
        # if oppdir didn't get set, error
        if oppdir == None:
            return False
        
        # is opposite direction free in other room?
        if troom.exits[oppdir] != None:
            return False
        
        # connect rooms together
        self.exits[tdir] = getRoomID(troom)
        troom.exits[oppdir] = getRoomID(self)
        
    def addItem(self, titem):
        self.inventory.append(titem)
    
    def show(self):
        # print room stuff to server
        print "ID:" + str(getRoomID(self))
        print self.name
        print self.desc
        print self.exits
        print self.inventory
    
    def userShow(self, tuser):
        # print room name and description
        tuser.conn.sendall(self.name + "\n")
        tuser.conn.sendall(self.desc + "\n")
        
        # print exits in room
        exitsfound = []
        for i in range(0, len(DIRECTIONS)):
            if self.exits[i] != None:
                exitsfound.append( DIRECTIONS[i])
        if len(exitsfound) > 0:
            exitstring = "Exits: "
            for i in exitsfound:
                if i == exitsfound[-1]:
                    exitstring += i
                else:
                    exitstring += i + ", "
            tuser.send(exitstring + "\n")
        
        # print items in room
        if len(self.inventory) > 0:
            istring = "\nYou see "
            for i in range(0, len(self.inventory) ):
                if i == len(self.inventory)-1:
                    istring += " and " + self.inventory[i].name + " here."
                else:
                    istring += self.inventory[i].name + ","
            tuser.send(istring + "\n")
    
    def userEdit(self, tuser):
        userquit = False
        editmode = 0
        
        menustr = { 1:"Print Room",
                    2:"Edit Name",
                    3:"Edit Desc",
                    4:"Create New Exit In Direction",
                    5:"Done"
                    }
        
        while not userquit:
            
            # print room directiosn
            tuser.send("Exits:\n")
            for i in range(0, len(self.exits)):
                estr = ""
                if self.exits[i] == None:
                    estr = "None"
                else:
                    estr = str( getRoomID(rooms[i]) )
                tuser.send("%d.) %s - %s\n" % (i, DIRECTIONS[i], estr) )
            
            # print room
            self.userShow(tuser)
            
            # print menu mode
            if editmode == 0:
                titlestr = "Edit Menu for Room #%d" % getRoomID(self)
                for i in range(0, len(titlestr) ):
                    if i == 0:
                        titlestr += "\n"
                    titlestr += "-"
                tuser.send(titlestr + "\n")
                
                for i in range(0, len(menustr.keys()) ):
                    tuser.send("%d. %s\n" % (menustr.keys()[i], menustr.values()[i]) )
                tuser.send(">")
            else:
                try:
                    tuser.send("%s : " % menustr[editmode])
                except KeyError:
                    tuser.send("Invalid option!\n")
                    editmode = 0;
                    continue
            
            # get input from user
            data = tuser.conn.recv(4096)
            
            # data not valid, user disconnected?
            if not data:
                break
            
            # chop input into word list
            usercmds = data.split()
            
            # if user hit return only
            if len(usercmds) == 0 and editmode == 0:
                continue
            
            # if edit mode is main menu, get mode selection
            if editmode == 0:
                editmode = int(usercmds[0])
                # immediate actions (no input further)
                if menustr[editmode] == "Print Room":
                    self.userShow(tuser)
                    editmode = 0
                elif menustr[editmode] == "Done":
                    userquit = True
                continue
            # else, user is in an option, get further input
            if menustr[editmode] == "Print Room":
                self.userShow(tuser)
                editmode = 0
            elif menustr[editmode] == "Edit Name":
                tuser.send("New Room Name:\n")
                tuser.send(data[:-2] + "\n")
                if userYesOrNo(tuser):
                    self.name = data[:-2]
                    editmode = 0
            elif menustr[editmode] == "Edit Desc":
                tuser.send("New Room Description:\n")
                tuser.send(data[:-2]+"\n")
                if userYesOrNo(tuser):
                    self.desc = data[:-2]
                    editmode = 0
            elif menustr[editmode] == "Create New Exit In Direction":
                if len(usercmds) == 0:
                    continue
                try:
                    tdir = int(usercmds[0])
                except ValueError:
                    tuser.send("Not a valid direction!  Enter dir #\n")
                    editmode = 0
                    continue;
                if tdir < 0 or tdir >= len(DIRECTIONS):
                    tuser.send("%d is an invalid direction!\n" % tdir)
                    edit = 0
                    continue
                elif self.exits[tdir] != None:
                    tuser.send("That direction is not empty!\n")
                    editmode = 0
                    continue
                tuser.send("New room in direction: %s?" % DIRECTIONS[ int(usercmds[0]) ])
                if userYesOrNo(tuser):
                    # create new room in direction
                    newroom = room()
                    rooms.append( newroom)
                    if not self.connectRoom(newroom, tdir):
                        print "Error connecting rooms!"
                    print "New room created, ID:" + str(getRoomID(newroom))
                    #attach new room inversely
                    
                    editmode = 0
                else:
                    editmode = 0
                


def lookRoom(tuser):
    getCurrentRoom(tuser).userShow(tuser)
            
def getCurrentRoom(tuser):
    return rooms[tuser.currentRoom]

                
def loadRooms():
    
    global roomsLoaded
    global rooms
    
    if roomsLoaded:
        return
        
    # load room data
    if os.path.isfile('rooms.pkl'):
        try:
            fload = open(r'./rooms.pkl', 'rb')
            rooms = pickle.load(fload)
            fload.close()
        except EOFError:
            print "Rooms file empty!"
            rooms.append( room() )
    # if not, create empty file
    else:
        newfile = open('rooms.pkl', 'w')
        newfile.close()
        rooms.append( room() )
    
    roomsLoaded = True
    
    vcount = 0
    
    for i in rooms:
        if i.doValidate():
            vcount += 1
    
    print str(len(rooms)) + " rooms loaded."
    if vcount > 0:
        print str(vcount) + " rooms had to be validated."
        
def saveRooms():
    global rooms
    
    fsave = open(r'./rooms.pkl', 'wb')
    pickle.dump(rooms, fsave)
    fsave.close()
    print str(len(rooms)) + " rooms saved."

    return True
