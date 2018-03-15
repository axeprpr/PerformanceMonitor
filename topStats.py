import Library
import re


topOutput,_,_,_ = Library.commandExecute("top -b -n 1")
topOutput = topOutput.split("  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND")
topOutput = topOutput[-1]
topOutputList = topOutput.splitlines()

topStats = []

for processes in topOutputList:
	processes = re.sub(' +',' ',processes)
	processData = processes.split(" ")
	if len(processData) == 13:
		processData.pop(0)
	elif len(processData) == 1:
		continue
	processStat = {
		"pid" : processData[0],
		"user" : processData[1],
		"vss" : processData[4],
		"rss" : processData[5],
		"percentCpu" : processData[8],
		"percentMem" : processData[9],
		"time" : processData[10],
		"command" : processData[11],
	      }	
	topStats.append(processStat)

Library.printDict(topStats)
