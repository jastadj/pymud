import pickle
import user
from tools import *
import os.path
import item

rooms = []

roomsLoaded = False

class room(object):
	def __init__(self):
		self.name = "unnamed"
		self.desc = "no description"
		self.inventory = []
	
	def addItem(self, titem):
		self.inventory.append(titem)
	
	def show(self):
		print self.name
		print self.desc
	
	def userShow(self, user):
		user.conn.sendall(self.name + "\n")
		user.conn.sendall(self.desc + "\n")
		
		istring = "\nYou see "
		if self.inventory.empty():
			istring.append("no items here.")
		else:			
			for titem in self.inventory:
				istring.append(titem.name + ",")
		
		user.conn.sendall(istring)
	
	def userEdit(self, user):
		userquit = False
		editmode = 0
		
		menustr = [ "Print Room\n",
					"Edit Name\n",
					"Edit Desc\n",
					"Done\n"]
		
		while not userquit:
			
			if editmode == 0:
				count = 1
				for menuitem in menustr:
					user.conn.sendall( str(count) + ". " + menuitem)
					count += 1
				user.conn.sendall(">")
			elif editmode == 2:
				user.conn.sendall("New Room Name:")
			elif editmode == 3:
				user.conn.sendall("New Room Desc:")		
			
			# get input from user
			data = user.conn.recv(4096)
			
			# data not valid, user disconnected?
			if not data:
				break

			usercmds = data.split()
				
			if len(usercmds) == 0:
				continue

			elif editmode == 0:
				if usercmds[0] == "1":
					self.userShow(user)
				elif usercmds[0] == "2":
					editmode = 2
				elif usercmds[0] == "3":
					editmode = 3
				elif usercmds[0] == "4":
					editmode = 4
					userquit = True
			elif editmode == 2:
				user.conn.sendall("Room Name:\n")
				user.conn.sendall( data[:-2] + "\n")
				user.conn.sendall("Keep? (y/n)")
				if userYesOrNo(user):
					self.name = data[:-2]
				editmode = 0
			elif editmode == 3:
				user.conn.sendall("Room Desc:\n")
				user.conn.sendall( data[:-2] + "\n")
				user.conn.sendall("Keep? (y/n)")
				if userYesOrNo(user):
					self.desc = data[:-2]
				editmode = 0


def lookRoom(user):
    getCurrentRoom(user).userShow(user)
            
def getCurrentRoom(user):
    return rooms[user.currentRoom]

				
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
		
def saveRooms():
    global rooms
	
    fsave = open(r'./rooms.pkl', 'wb')
    pickle.dump(rooms, fsave)
    fsave.close()
    print "Rooms saved."
