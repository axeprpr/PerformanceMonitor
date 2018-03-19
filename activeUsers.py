import Library
import re

whoOutput,_,_,_ = Library.commandExecute("who")
whoOutputList = whoOutput.splitlines()
#print whoOutputList

activeUsers = []

for who in whoOutputList:
	who = re.sub(' +',' ',who)
	who = who.split(" ")
	whoStat = {
	  "user" : who[0],
	  "pseudoTErminal" : who[1],
	  "date" : who[2],
	  "time" : who[3],
	  "remoteAddress" : who[4],
		  }
	activeUsers.append(whoStat)

Library.printDict(activeUsers)
