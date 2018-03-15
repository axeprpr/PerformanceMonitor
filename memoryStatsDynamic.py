import Library

def getPhysicalMemoryInfo():
        totalMemory,_,_,_=Library.commandExecute("free -b | grep Mem | awk '{print $2}'")
        usedMemory,_,_,_=Library.commandExecute("free -b | grep Mem | awk '{print $3}'")
        freeMemory,_,_,_=Library.commandExecute("free -b | grep Mem | awk '{print $4}'")
        avaialbleMemory,_,_,_=Library.commandExecute("free  | grep Mem | awk '{print $7}'")
        return int(totalMemory),int(usedMemory),int(freeMemory),int(avaialbleMemory)


def getSwapMemoryInfo():
        totalMemory,_,_,_=Library.commandExecute("free -b | grep Swap | awk '{print $2}'")
        usedMemory,_,_,_=Library.commandExecute("free -b | grep Swap | awk '{print $3}'")
        freeMemory,_,_,_=Library.commandExecute("free -b | grep Swap | awk '{print $4}'")
        return int(totalMemory),int(usedMemory),int(freeMemory)


a = getPhysicalMemoryInfo()
b = getSwapMemoryInfo()

memoryStats = {
		"usedMemoryPhy" : a[1],
		"freeMemoryPhy" : a[2],
		"availableMemoryPhy" : a[3],
		"usedMemorySwp" : b[1],
		"freeMemorySwp" : b[2],

	      }

print memoryStats
