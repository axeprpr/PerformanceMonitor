import Library

def getPhysicalMemoryInfo():
        totalMemory,_,_,_=Library.commandExecute("free -b | grep Mem | awk '{print $2}'")
        return int(totalMemory)


def getSwapMemoryInfo():
        totalMemory,_,_,_=Library.commandExecute("free -b | grep Swap | awk '{print $2}'")
        return int(totalMemory)


a = getPhysicalMemoryInfo()
b = getSwapMemoryInfo()

memoryStats = {
		"totalMemoryPhy" : a,
		"totalMemorySwp" : b,
	      }

print memoryStats
