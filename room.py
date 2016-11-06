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

class roomDescriptor(object):
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        

class room(object):
    
    def __init__(self):
        self.name = "unnamed"
        self.desc = "no description"
        self.inventory = []
        self.descriptors = []
        
        # initialize all exits to none
        self.exits = []
        for i in range(0, len(DIRECTIONS)):
            self.exits.append(None)
    
    def getID(self):
        return getRoomID(self)
    
    def doValidate(self):
        hadtovalidate = False   
        
        try:
            dtest = len(self.descriptors)
        except AttributeError:
            self.descriptors = []
            hadtovalidate = True
            
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
        print "items:" + str(len(self.inventory) )
        print "descriptors:" + str(len(self.descriptors))
        print "users here:"
        for usr in getUsersInRoom(self):
            print usr.cred.ulogin
        
    def userShow(self, tuser):
        # print room name and description
        tuser.send("%s" % setColor(tuser, COLOR_CYAN, True) )
        tuser.send(self.name + "\n")
        tuser.send("%s" % resetColor(tuser) )
        tuser.send(self.desc + "\n")
        
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
            tuser.send("%s" % setColor(tuser, COLOR_MAGENTA) )
            tuser.send(exitstring + "\n")
            tuser.send("%s" % resetColor(tuser))
        
        # print items in room
        if len(self.inventory) > 0:
            istring = "\nYou see "
            for i in range(0, len(self.inventory) ):
                if i == len(self.inventory)-1:
                    istring += " and " + self.inventory[i].name + " here."
                else:
                    istring += self.inventory[i].name + ","
            tuser.send(istring + "\n")
        
        # print other players in room
        ulist = getUsersInRoom(self)
        if tuser in ulist:
            ulist.remove(tuser)
        ulistsz = len(ulist)
        if ulistsz > 0:
            uhere = ""
            for usr in ulist:
                if ulistsz == 1:
                    uhere = usr.cred.ulogin + " is here."
                else:
                    if usr == ulist[-1]:
                        uhere += usr.cred.ulogin + " are here."
                    else:
                        uhere += user.cred.ulogin + ", "
            tuser.send(uhere + "\n")


def lookRoom(tuser):
    getCurrentRoom(tuser).userShow(tuser)
            
def getCurrentRoom(tuser):
    return rooms[tuser.currentRoom]

def getUsersInRoom(troom):
    roomnum = getRoomID(troom)
    
    ulist = []
    
    for usr in user.users:
        if usr.currentRoom == roomnum:
            ulist.append(usr)
    
    return ulist
        
                
def loadRooms():
    
    global roomsLoaded
    global rooms
    
    if roomsLoaded:
        return
        
    # load room data
    if os.path.isfile('./data/rooms.pkl'):
        try:
            fload = open(r'./data/rooms.pkl', 'rb')
            rooms = pickle.load(fload)
            fload.close()
        except EOFError:
            print "Rooms file empty!"
            rooms.append( room() )
    # if not, create empty file
    else:
        newfile = open('./data/rooms.pkl', 'w')
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
