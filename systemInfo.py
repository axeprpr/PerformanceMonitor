import Library


def getOSinfo():
        osType,_,_,_=Library.commandExecute("cat /etc/system-release | awk '{print $1,$2}'")
        osType = osType.strip()
        hostName,_,_,_=Library.commandExecute("uname -n")
	hostName = hostName.strip()
        osRevision,_,_,_=Library.commandExecute("cat /etc/system-release | awk '{print $4}'")
        osRevision = osRevision.strip()
        kernelVersion,_,_,_=Library.commandExecute("uname -r")
        return osType,hostName,osRevision,kernelVersion

def getUpTime():
        upTime,_,_,_=Library.commandExecute("uptime -p | sed -e 's/up //g'")
        upSinceDate,_,_,_=Library.commandExecute("uptime -s | awk {'print $1'}")
        upSinceTime,_,_,_=Library.commandExecute("uptime -s | awk {'print $2'}")
        return upTime,upSinceDate,upSinceTime


a = getOSinfo()
b = getUpTime()


systemInfo = {

	"osName" : a[0].strip(),
	"hostName" : a[1].strip(),
	"osVersion" : a[2].strip(),
	"kernelVersion" : a[3].strip(),
	"upSinceDate" : b[1].strip(),
	"upSinceTime" : b[2].strip()
	     }

print systemInfo

