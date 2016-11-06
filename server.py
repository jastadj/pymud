# Socket server in python using select function
 
import time
import pickle
import os.path
import socket, select
from tools import *
from thread import *
import user
import room
import item
import game
import command

def doLogin(conn):
    
    global doshutdown
    
    # prompt login
    conn.send('login:')
    userlogin = ["",""]
    mode = 0
    mode_getlogin = 0
    mode_getpass = 1
    mode_user = 2
    mode_newusername = 7
    mode_newuserpass1 = 8
    mode_newuserpass2 = 9
    mode_done = 5
    currentuser = None
    currentusercred = None
    
    #infinite loop so that function do not terminate and thread do not end.
    while mode != mode_done:
         
        #Receiving from client
        data = conn.recv(1024)
        #reply = 'login prompt...' + data
        if not data:
            break
     
        
        usercmd = data[:-2]
        
        if len(usercmd) == 0:
            continue;

        # LOGIN VERIFICATION STUFF
        if mode == mode_getlogin:
            userlogin[0] = usercmd
            # debug shutdown
            if userlogin[0] == "shutdown":
                conn.sendall("commanding server shutdown\n")
                shutdownServer(None)
            
            # if user login is new
            if user.usernameAvailable(userlogin[0]):
                mode = mode_newusername
                conn.sendall("User name available.  Create new user?(y/n)")
            else:
                mode = mode_getpass
                conn.sendall("password:")
            
        elif mode == mode_getpass:
            userlogin[1] = usercmd
            
            currentusercred = user.validLogin(userlogin)
            
            if currentusercred != None:
                mode = mode_user
                conn.sendall("Successful login!\n")
            else:
                if user.userOnline(userlogin[0]):
                    conn.sendall("User is already logged in!\n")
                else:
                    conn.sendall("Invalid username/password!\n")
                conn.sendall("login:")
                mode = mode_getlogin
        elif mode == mode_newusername:
            if usercmd == "y":
                # check to make sure that user name is doable
                if not user.validUsername(userlogin[0]):
                    conn.sendall("That username is not valid!\n")
                    conn.sendall("Letters only, no spaces.\n")
                    mode = mode_getlogin
                    continue
                conn.sendall("Enter new user password:")
                mode = mode_newuserpass1
            elif usercmd == "n":
                conn.sendall("login:")
                mode = mode_getlogin
            else:
                conn.sendall("Not a valid option!  (y/n)")
        elif mode == mode_newuserpass1:
            userlogin[1] = usercmd
            conn.sendall("Enter new user password again:")
            mode = mode_newuserpass2
        elif mode == mode_newuserpass2:
            if usercmd != userlogin[1]:
                conn.sendall("Passwords do not match!\n")
                conn.sendall("login:")
                mode = mode_getlogin
            else:
                currentusercred = user.createUserAccount(userlogin)
                if currentusercred == None:
                    conn.sendall("Error creating user account!\n")
                    mode = mode_getlogin
                    continue
                else:
                    conn.sendall("User " +currentusercred.ulogin + " created.\n")
                    mode = mode_user
        
        
        # log in to user and start main loop
        if mode == mode_user:
            if currentusercred != None:
                currentuser = user.loadUser(currentusercred)
                if currentuser == None:
                    conn.sendall("Error loading user file!\n")
                    mode = mode_getlogin
                    conn.sendall("login:")
                    continue
                currentuser.dologin(conn)
                conn.sendall("logged in as:" + currentusercred.ulogin + "\n")
                user.users.append(currentuser)
                print currentuser.cred.ulogin + " logged in."
                mode = mode_done
                game.handleUser(currentuser)
                
                
            
     
    #came out of loop
    #print "disconnected:"
    #print conn.getpeername()
    if currentuser != None :
        user.users.remove(currentuser)
    conn.close()



def serverBroadcast(msg):
    mystr = "[SERVER]: " + msg
    print mystr
    for uindex in range(0, len(user.users) ):
         user.users[uindex].send(mystr + "\n")
    

def saveServer():
    user.saveAllUsers()
    room.saveRooms()
    serverBroadcast("Server saved.")
    
    return True
    
def shutdownServer(tuser):
    
    global shutdown
    
    doshutdown = True
    
    if tuser != None:
        print tuser.cred.ulogin + " commanded server shutdown"
    
def start():
    
    global doshutdown
    
    # server setup
    SERVER_TIMEOUT = 5
    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 8888
     
    # create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)



    # load users
    user.loadUserCredentials()

    # load rooms
    room.loadRooms()


    while not doshutdown:
        
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select( CONNECTION_LIST,[],[], SERVER_TIMEOUT)
        
        for sock in read_sockets:
             
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                sockfd.send("%c[%dmHELLO!\n" %(0x1B, 32))
                sockfd.send("%c[%dm>" %(0x1b, 37))
                 
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    # echo back the client message
                    if data:
                        sock.send('OK ... ' + data)
                        
                        usercmd = data[:-2]
                        
                        if usercmd == "shutdown" or usercmd == "s":
                            doshutdown = True
                        elif usercmd == "test":
                            sock.send("main test")
                        elif usercmd == "login" or usercmd == "l":
                            CONNECTION_LIST.remove(sock)
                            start_new_thread(doLogin ,(sock,))
                        else:
                            sock.send(">")
                    else:
                        print "Client (%s, %s) is offline" % addr
                        sock.close()
                        CONNECTION_LIST.remove(sock)
                 
                # client disconnected, so remove from socket list
                except:
                    #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
    
    print "Shutting down..."
    server_socket.close()

if __name__ == "__main__":
    doshutdown = False
    
    start()
