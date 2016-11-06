import socket
import os.path
import pickle
import item
from tools import *

users = []
usercreds = []

areUsersLoaded = False

class usercred(object):
    def __init__(self, ulogin, upass):
        self.ulogin = ulogin
        self.upass = upass
        self.uname = "unnamed"
        self.cmdaliases = {}
        self.cmdaliases.update( {"?":"help"} )

class user(object):
    def __init__(self,cred):
        self.cred = cred
        self.conn = None
        self.currentRoom = 0
        self.inventory = []
    def send(self, str):
        if self.conn != None:
            self.conn.sendall(str)
    def receive(self, isize):
        rdata = None
        # size should be like 1024, or 4096
        try:
            rdata = self.conn.recv(isize)
        except:
            pass
        
        # not receiving, disconnect!
        if not rdata:
            self.doDisconnect()
        else:
            return rdata
            
    def dologin(self, conn):
        self.conn = conn
    def doDisconnect(self):
        try:
            self.send("Logging off...\n")
        except:
            pass
        print "User " + self.cred.ulogin + " logged off."
        try:
            self.conn.close()       
        except:
            pass
        self.conn = None
        # save user file
        saveUser(self)
    def isOnline(self):
        if self.conn != None:
            return True
        else:
            return False


def loadUserCredentials():
    
    global areUsersLoaded
    global usercreds
    
    if areUsersLoaded:
        return
    
    if os.path.isfile('./data/usercreds.pkl'):
        try:
            fload = open(r'./data/usercreds.pkl', 'rb')
            usercreds = pickle.load(fload)
            fload.close()
        except EOFError:
            print "User cred file empty!"
    # if not, create empty file
    else:
        newfile = open('./data/usercreds.pkl', 'w')
        newfile.close()
    
    areUsersLoaded = True
    
    print str(len(usercreds)) + " user credentials loaded:"


def saveUserCredentials():
    global usercreds
       
    fsave = open(r'./data/usercreds.pkl', 'wb')
    pickle.dump(usercreds, fsave)
    fsave.close()
    print str(len(users)) + " user credentials saved."
    
    return True

def saveUser(tuser):
    fsave = open(r'./users/%s.pkl' % tuser.cred.ulogin, 'wb')
    pickle.dump(tuser, fsave)
    fsave.close()
    print tuser.cred.ulogin + " user file saved."
    
    return True

def saveAllUsers():
	saveUserCredentials()
	for usr in users:
		saveUser(usr)

def loadUser(tusercred):
    
    tuser = None
    
    # user is already online!
    if userOnline(tusercred.ulogin):
        return None
    
    if os.path.isfile('%s.pkl' %tusercred.ulogin):
        try:
            fload = open(r'./users/%s.pkl' %tusercred.ulogin, 'rb')
            tuser = pickle.load(fload)
            fload.close()
        except EOFError:
            print "User cred file empty!"
            return None
    # if not, create empty file
    else:
        newfile = open('./users/%s.pkl' % tusercred.ulogin, 'w')
        newfile.close()
        # create new user
        tuser = user(tusercred)
        print "New user file created for " + tusercred.ulogin
        
        # now save user
        saveUser(tuser)
    
    # check to see that userfile creds match up
    if tuser.cred != tusercred:
		print "User creds dont match for %s!" %tusercred.ulogin
		return None
    
    return tuser

def validLogin(userlogin):
    global usercreds
    
    if len(userlogin) != 2:
        print "login attempt:\n"
        print userlogin
        print "user login does not have two elements!"
        return None
    else:
        for uindex in range(0, len(usercreds)):
            if userlogin[0] == usercreds[uindex].ulogin:
                if userlogin[1] == usercreds[uindex].upass:
                    if not userOnline(userlogin[0]):
                        return usercreds[uindex]
    return None

def validUsername(uname):
    if uname == "usercred":
		return False
    if uname.isalpha():
        return True
    else:
        return False

def userOnline(username):
    global users
    
    for uindex in range(0, len(users)):
        if username[0] == users[uindex].cred.ulogin:
            return True
            
    return False

def usernameAvailable(username):
    global usercred

    if len(usercreds) == 0:
        return True
    for uindex in range(0, len(usercreds)):
        if username == usercreds[uindex].ulogin:
            return False

    return True

def createUserAccount(userlogin):
    if not validUsername(userlogin[0]):
        return None
    
    # does a user file exist already for some reason?
    if os.path.isfile('%s.pkl' %userlogin[0]):
        print "User file for new account already exists!"
        print "  %s.pkl" %userlogin[0]
        return None     
    if usernameAvailable(userlogin):
        newusercred = usercred(userlogin[0], userlogin[1])
        usercreds.append( newusercred);
        print "User account created:" + newusercred.ulogin
        # save credentials
        saveUserCredentials()
        return newusercred
    else:
        return None

def doWho(tuser):
    tuser.send("Users Online:\n")
    tuser.send("-------------\n")
    for usr in users:
        if usr.isOnline():
            tuser.send(usr.cred.ulogin + "\n")
    tuser.send("\n")

