import Library

allPids,_,_,_ = Library.commandExecute("ps -eaf | awk {'print $2'} | sed -n '2,$p'")
allPids = allPids.splitlines()

allPidStats = []

for pid in allPids:
	pidStats = Library.getPIDstats(pid)
	print pid
	processStats = {
			"processID" : pid,
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
	allPidStats.append(processStats)

Library.printDict(allPidStats)



