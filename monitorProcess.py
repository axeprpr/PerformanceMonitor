import Library
import pymongo
from pymongo import MongoClient
import json
import datetime

client = MongoClient("192.168.10.111", 27017 )
db = client["PerformanceMonitor"]
collection = db["processMonitor"]



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
			"totalBytesRead" : pidStats[6],
			"totalBytesWritten" : pidStats[7],
			"kbReadPerSec" : pidStats[8],
			"kbWrittenPerSec" : pidStats[9],
			"timestamp" : int(datetime.datetime.now().strftime('%s')),
			"name" : processName,
			       }
		collection.insert(processStats)
                del processStats["_id"]
		del processStats["timestamp"]
		processNameData.append(processStats)
		counter = counter + 1
	allProcessData.append({processName : processNameData})
print allProcessData
