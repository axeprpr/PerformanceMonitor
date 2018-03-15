import Library

processNameData,_,_,_ = Library.commandExecute("cat monitorProcessList.txt")
processNameList = processNameData.splitlines()

allProcessData = []

for processName in processNameList:
	processNameData = []
	pIds = Library.getProcessID(processName)
	if pIds[1] == 0:
		continue	
	counter = 0
	for index in pIds[1]:
		pidStats = Library.getPIDstats(index)
		processStats = {
			"processString" : pIds[0][counter].strip(),
			"processId" : int(pIds[1][counter]),
			"percentageCPU" : pidStats[0],
			"CPUnumber" : pidStats[1],
			"vsz" : pidStats[2],
			"rss" : pidStats[3],
			"percentageMEM" : pidStats[4],
			"timeStamp" : pidStats[5],
			"totalBytesRead" : pidStats[6],
			"totalBytesWritten" : pidStats[7],
			"kbReadPerSec" : pidStats[8],
			"kbWrittenPerSec" : pidStats[9],
			       }
		processNameData.append(processStats)
		counter = counter + 1
	allProcessData.append({processName : processNameData})

Library.printDict(allProcessData)
