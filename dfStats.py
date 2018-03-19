import Library
import re


dfOutput,_,_,_ = Library.commandExecute("df")
dfOutput = dfOutput.split("Filesystem               1K-blocks     Used  Available Use% Mounted on")
dfOutput = dfOutput[-1]
dfOutputList = dfOutput.splitlines()

dfStats = []

for disks in dfOutputList:
	disks = re.sub(' +',' ',disks)
	if disks.strip() == "":
		continue
	diskData = disks.split(" ")
	diskStat = {
		"filesystem" : diskData[0],
		"size" : int(diskData[1]),
		"used" : int(diskData[2]),
		"available" : int(diskData[3]),
		"usePercent" : int(diskData[4].replace("%","")),
		"mountPoint" : diskData[5],
		   }
	dfStats.append(diskStat)



Library.printDict(dfStats)

