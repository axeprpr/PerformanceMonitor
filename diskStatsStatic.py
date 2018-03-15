import Library



def getDiskUsage():
        totalDisk,_,_,_=Library.commandExecute(" df / | awk '{print $2}' | sed -n '2p'")
        totalDisk = int(totalDisk)*1024
        return totalDisk


a = getDiskUsage()

diskStats = {
		"totalDisk" : a,
	    }
print diskStats
