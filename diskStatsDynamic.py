import Library

def getDiskPerformance():
        readData = 0.00
        writeData = 0.00
        readList,_,_,_ = Library.commandExecute("iostat | sed -n '7,100p' | awk '{print $3}'")
        writeList,_,_,_ = Library.commandExecute("iostat | sed -n '7,100p' | awk '{print $4}'")
        readList = readList.splitlines()
        writeList = writeList.splitlines()
        for index in readList:
                try:
                        readData += float(index)
                except:
                        pass

        for index1 in writeList:
                try:
                        writeData += float(index1)
                except:
                        pass

        return readData,writeData



def getDiskUsage():
        totalDisk,_,_,_=Library.commandExecute(" df / | awk '{print $2}' | sed -n '2p'")
        totalUsed,_,_,_=Library.commandExecute("df / | awk '{print $3}' | sed -n '2p'")
        totalAvailable,_,_,_=Library.commandExecute("df / | awk '{print $4}' | sed -n '2p'")
        diskUsageStats,_,_,_=Library.commandExecute("df ")
        totalDisk = int(totalDisk)*1024
        totalUsed = int(totalUsed)*1024
        totalAvailable = int(totalAvailable)*1024
        return totalDisk,totalUsed,totalAvailable,diskUsageStats


a = getDiskUsage()
b = getDiskPerformance()

diskStats = {
		"totalUsed" : a[1],
	        "totalAvailable" : a[2],
		"readRate" : round(b[0],2),
		"writeRate" : round(b[1],2)

	    }
print diskStats
