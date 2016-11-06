import user

def unsplit(words):
    sentence = ""
    wcount = len(words)
    for word in words:
        sentence += word
        if word != words[-1]:
            sentence += " "
    return sentence

def userYesOrNo(tuser, msg = "(y/n)"):
	
	done = False

	while not done:
		
		tuser.send(msg)
		
		# get input from user
		data = tuser.conn.recv(1024)

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

# define terminal colors
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7

TERM_ESCAPE = 0x1b

def resetColor(tuser):
	return "%c[%dm" % (TERM_ESCAPE, 0)

def setColor(tuser, tcolor, tbold = False):
	# esc[31m = red color
	# esc[31;1m = bold red color
	if not tbold:
		return "%c[%dm" %(TERM_ESCAPE, 30+tcolor)
	else:
		return "%c[%d;%dm" %(TERM_ESCAPE, 30+tcolor, 1)

	
