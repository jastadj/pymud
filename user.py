import socket
import os.path
import pickle
import item

users = []
usercred = []

usersLoaded = False

class user(object):
    def __init__(self, conn, name):
        self.name = name
        self.conn = conn
        self.currentRoom = 0
        self.inventory = []
    def send(self, str):
		self.conn.sendall(str)

def loadUsers():
    
    global usersLoaded
    global usercred
    
    if usersLoaded:
        return
    
    if os.path.isfile('usercreds.pkl'):
        try:
            fload = open(r'./usercreds.pkl', 'rb')
            usercred = pickle.load(fload)
            fload.close()
        except EOFError:
            print "User cred file empty!"
    # if not, create empty file
    else:
        newfile = open('usercreds.pkl', 'w')
        newfile.close()
    
    usersLoaded = True
    
    print str(len(usercred)) + " users loaded:"


def saveUsers():
    global usercred
       
    fsave = open(r'./usercreds.pkl', 'wb')
    pickle.dump(usercred, fsave)
    fsave.close()
    print str(len(users)) + " users saved."
    
    return True

def validLogin(userlogin):
    global usercred
    
    if len(userlogin) != 2:
        print "login attempt:\n"
        print userlogin
        print "user login does not have two elements!"
        return False
    else:
        for uindex in range(0, len(usercred)):
            if userlogin[0] == usercred[uindex][0]:
                if userlogin[1] == usercred[uindex][1]:
                    if not userOnline(userlogin[0]):
                        return True
    return False

def userOnline(username):
    global users
    
    for uindex in range(0, len(users)):
        if username[0] == users[uindex].name:
            return True
            
    return False

def usernameAvailable(username):
    global usercred

    if len(usercred) == 0:
        return True
    for uindex in range(0, len(usercred)):
        if username == usercred[uindex][0]:
            return False

    return True
    
def createUserAccount(userlogin):
    if usernameAvailable(userlogin):
        usercred.append(userlogin);
        print "User account created:" + userlogin[0]
        return True
    else:
        return False

