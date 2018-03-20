import Library
import pymongo
from pymongo import MongoClient
import json
import datetime

client = MongoClient("192.168.10.111", 27017 )
db = client["PerformanceMonitor"]
collection = db["fileMonitor"]


processNameData,_,_,_ = Library.commandExecute("cat monitorFilesList.txt")
fileList = processNameData.splitlines()




allFilesData = []

def getPermission(permission):
	num = 0
	if 'r' in permission:
		num = num + 4
	if 'w' in permission:
		num = num + 2
	if 'x' in permission:
		num = num + 1
	return num

for fileN in fileList:
	fileStats,_,_,_ = Library.commandExecute("ls -lart " + fileN)
	if fileStats.strip() == "":
		pass
	else:
		fileStats = fileStats.split(" ")
		if fileStats[0].strip() == "total":
			fileD = fileN.split("/")
			fileD = ' '.join(fileD).split()
			path = ""
			for paths in range(len(fileD) - 1):
				path = path + "/" + fileD[paths].strip()
			if path.strip() == "":
				path = "/"
			directoryName = fileD[-1]
			fileStats,_,_,_ = Library.commandExecute("ls -lart " + path + " | grep " + directoryName + "$")
			fileStats = fileStats.replace("  ", " ").split(" ")

		permission = int(str(getPermission(fileStats[0][1:4])) + str(getPermission(fileStats[0][4:7])) + str(getPermission(fileStats[0][7:10])))
		if fileStats[0][0] == 'd':
			isDirectory = "True"
		else:
			isDirectory = "False"	
		if fileStats[4].strip() == "":
			filesize = fileStats[5]
			lastModified = fileStats[6] + " " + fileStats[7] + " " + fileStats[8]
		else:
			filesize = fileStats[4]
			lastModified = fileStats[5] + " " + fileStats[6] + " " + fileStats[7]
		 
		fileStat = {
			"owner" : fileStats[2] ,
			"ownerGroup" : fileStats[3],
			"fileSize" : filesize,
			"lastModified" : lastModified,
			"permission" : fileStats[0],
			"chmod" : permission,	
			"isDirectory" : isDirectory,
			"name" : fileN,
			"timestamp" : int(datetime.datetime.now().strftime('%s')),
			   }
		collection.insert(fileStat)
		del fileStat["_id"]
		allFilesData.append(fileStat)

print  allFilesData 

