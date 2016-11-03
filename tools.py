import user

def unsplit(words):
    sentence = ""
    wcount = len(words)
    for word in words:
        sentence += word
        if word != words[-1]:
            sentence += " "
    return sentence

def userYesOrNo(user):
	
	done = False

	while not done:
		# get input from user
		data = user.conn.recv(1024)

		# data not valid, user disconnected?
		if not data:
			return False

		usercmds = data.split()
			
		if len(usercmds) == 0:
			return False

		if usercmds[0][0] == 'y' or usercmds[0][0] == 'Y':
			return True
		elif usercmds[0][0] == 'n' or usercmds[0][0] == 'N':
			return False
		else:
			user.conn.sendall("(Y/N)")
