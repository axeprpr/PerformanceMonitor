import Library
import re

lastLogin,_,_,_ = Library.commandExecute("lastlog -u root | sed -n '2p'")
lastLogin = re.sub(" +"," ",lastLogin)
lastLogin = lastLogin.split(" ")

time = ""
for index in lastLogin[3:]:
	time = time + index.strip() + " "

lastLoginData = {
	"username" :lastLogin[0] ,
	"terminal" : lastLogin[1],
	"Address" : lastLogin[2],
	"time" : time,

		}

print lastLoginData

