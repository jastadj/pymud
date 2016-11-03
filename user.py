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

def saveUsers():
    global usercred
       
    fsave = open(r'./usercreds.pkl', 'wb')
    pickle.dump(usercred, fsave)
    fsave.close()
    print "Users saved."

def validLogin(userlogin):
	global usercred
	if len(userlogin) != 2:
		return False
	else:
		for user in usercred:
			if userlogin[0] in user[0]:
				if userlogin[1] in user[1]:
					if not userOnline(userlogin[0]):
						return True
	return False

def userOnline(username):
	global users
	
	for user in users:
		if username == user.name:
			return True
			
	return False

def usernameAvailable(username):
	global usercred

	if len(usercred) == 0:
		return True
	for user in usercred:
		if username in user[0]:
			return False
		else:
			return True
