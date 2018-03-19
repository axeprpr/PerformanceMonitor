import Library

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
			print "PATH " + path
			print "directoryName" + directoryName
			fileStats,_,_,_ = Library.commandExecute("ls -lart " + path + " | grep " + directoryName + "$")
			print "COMMAND " + "ls -lart " + path + " | grep " + directoryName + "$"
			fileStats = fileStats.replace("  ", " ").split(" ")

		permission = int(str(getPermission(fileStats[0][1:4])) + str(getPermission(fileStats[0][4:7])) + str(getPermission(fileStats[0][7:10])))
		if fileStats[0][0] == 'd':
			isDirectory = True
		else:
			isDirectory = False	
		fileStat = {
			"owner" : fileStats[2] ,
			"ownerGroup" : fileStats[3],
			"fileSize" : fileStats[4],
			"lastModified" : fileStats[5] + " " + fileStats[6] + " " + fileStats[7],
			"permission" : fileStats[0],
			"chmod" : permission,	
			"isDirectory" : isDirectory,
			   }
		allFilesData.append({fileN : fileStat })


Library.printDict(allFilesData)
