import room
from tools import *

def roomEdit(tuser, troom):
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
		for i in range(0, len(troom.exits)):
			estr = ""
			if troom.exits[i] == None:
				estr = "None"
			else:
				estr = str( troom.exits[i] )
			tuser.send("%d.) %s - %s\n" % (i, room.DIRECTIONS[i], estr) )
		
		# print room
		troom.userShow(tuser)
		
		# print menu mode
		if editmode == 0:
			titlestr = "Edit Menu for Room #%d" % room.getRoomID(troom)
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
		data = tuser.receive(4096)
		
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
				troom.userShow(tuser)
				editmode = 0
			elif menustr[editmode] == "Done":
				userquit = True
			continue
		# else, user is in an option, get further input
		if menustr[editmode] == "Print Room":
			troom.userShow(tuser)
			editmode = 0
		elif menustr[editmode] == "Edit Name":
			tuser.send("New Room Name:\n")
			tuser.send(data[:-2] + "\n")
			if userYesOrNo(tuser):
				troom.name = data[:-2]
				editmode = 0
		elif menustr[editmode] == "Edit Desc":
			tuser.send("New Room Description:\n")
			tuser.send(data[:-2]+"\n")
			if userYesOrNo(tuser):
				troom.desc = data[:-2]
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
			if tdir < 0 or tdir >= len(room.DIRECTIONS):
				tuser.send("%d is an invalid direction!\n" % tdir)
				edit = 0
				continue
			elif troom.exits[tdir] != None:
				tuser.send("That direction is not empty!\n")
				editmode = 0
				continue
			tuser.send("New room in direction: %s?" % room.DIRECTIONS[ int(usercmds[0]) ])
			if userYesOrNo(tuser):
				# create new room in direction
				newroom = room.room()
				room.rooms.append( newroom)
				if not troom.connectRoom(newroom, tdir):
					print "Error connecting rooms!"
				print "New room created, ID:" + str(room.getRoomID(newroom))
				#attach new room inversely
				
				editmode = 0
			else:
				editmode = 0
