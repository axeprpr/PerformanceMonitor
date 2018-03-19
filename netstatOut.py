import Library
import re


netstatOutput,_,_,_ = Library.commandExecute("netstat -anp | grep CONNECTED")
netstatOutputList = netstatOutput.splitlines()

netstatData = []

for netStat in netstatOutputList:
	netStat = re.sub(" +"," ",netStat)
	netData = netStat.split(" ")
        netstats = {
		"proto" : netData[0],
		"refCnt" : netData[1],
		"flags" : netData[2] + " " + netData[3],
		"type" : netData[4],
		"state" : netData[5],
		"iNode" : netData[6],
		"pid" : netData[7].split("/")[0],
		"program" : netData[7].split("/")[-1],
		"path" : netData[-1],

		   }	
	netstatData.append(netstats)

Library.printDict(netstatData)
	

