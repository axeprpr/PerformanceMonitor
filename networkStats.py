import Library
import socket
import re
import time
import math



remoteServer = "www.google.com"
if Library.isConnected(remoteServer):
	network = {"networkState" : "Connected"}
else:
	network = {"networkState" : "Disconnected"}



availableInterfaces,_,_,_ = Library.commandExecute("ip -o addr | awk '{split($4, a, \"/\"); print $2\" : \"a[1]}'")
availableInterfaces =  availableInterfaces.splitlines()

interfaceList = []
foundInterface = []

for index in availableInterfaces:
	interfaceName = index.split(":")[0].strip()
	if interfaceName in foundInterface:
		location = foundInterface.index(interfaceName)
		interfaceList[location].update({"IPv6" : ":".join(index.split(":")[1:])})
		pass
	else:
		foundInterface.append(interfaceName)
		interfaceList.append({"interfaceName" : interfaceName , "IPv4" : index.split(":")[1].strip()})


interfaceInfoTable,_,_,_ = Library.commandExecute("netstat -i")
interfaceInfoTable =  interfaceInfoTable.splitlines()

for interfaceData in interfaceList:
	interfaceName = interfaceData["interfaceName"]
	for interfaceTable in interfaceInfoTable:
		interfaceTable = re.sub(r'\s+',' ',interfaceTable)
		if interfaceName in interfaceTable:
			interfaceTable = interfaceTable.split(" ")
			MTU = interfaceTable[1]
			RXOK = interfaceTable[2]
			RXERR = interfaceTable[3]
			RXDRP = interfaceTable[4]
			RXOVR = interfaceTable[5]
			TXOK = interfaceTable[6]
			TXERR = interfaceTable[7]
			TXDRP = interfaceTable[8]
			TXOVR = interfaceTable[9]
			trafficInfo = {
				"RXOK"  : RXOK,
				"RXERR" :RXERR ,
				"RXDRP" :RXDRP ,
				"RXOVR" :RXOVR ,
				"TXOK"  :TXOK ,
				"TXERR" : TXERR ,
				"TXDRP" : TXDRP,
				"TXOVR" : TXOVR,
				"MTU"   : MTU,
				      }			
			interfaceData.update({"trafficInfo" : trafficInfo})
			break
		else:
			pass



INTERVAL = 1            #   1 second
AVG_LOW_PASS = 0.2      #   Simple Complemetary Filter

ifaces = {}

idata = Library.GetNetworkInterfaces()
for eth in idata:
    ifaces[eth["interface"]] = {
        "rxrate"    :   0,
        "txrate"    :   0,
        "avgrx"     :   0,
        "avgtx"     :   0,
        "toptx"     :   0,
        "toprx"     :   0,
        "sendbytes" :   eth["tx"]["bytes"],
        "recvbytes" :   eth["rx"]["bytes"]
    }

set = 0
while set<3:

    idata = Library.GetNetworkInterfaces()
    for eth in idata:
        #   Calculate the Rate
        ifaces[eth["interface"]]["rxrate"]      =   (eth["rx"]["bytes"] - ifaces[eth["interface"]]["recvbytes"]) / INTERVAL
        ifaces[eth["interface"]]["txrate"]      =   (eth["tx"]["bytes"] - ifaces[eth["interface"]]["sendbytes"]) / INTERVAL

        #   Set the rx/tx bytes
        ifaces[eth["interface"]]["recvbytes"]   =   eth["rx"]["bytes"]
        ifaces[eth["interface"]]["sendbytes"]   =   eth["tx"]["bytes"]

        #   Calculate the Average Rate
        ifaces[eth["interface"]]["avgrx"]       =   int(ifaces[eth["interface"]]["rxrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgrx"] * (1.0-AVG_LOW_PASS))
        ifaces[eth["interface"]]["avgtx"]       =   int(ifaces[eth["interface"]]["txrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgtx"] * (1.0-AVG_LOW_PASS))

        #   Set the Max Rates
        ifaces[eth["interface"]]["toprx"]       =   ifaces[eth["interface"]]["rxrate"] if ifaces[eth["interface"]]["rxrate"] > ifaces[eth["interface"]]["toprx"] else ifaces[eth["interface"]]["toprx"]
        ifaces[eth["interface"]]["toptx"]       =   ifaces[eth["interface"]]["txrate"] if ifaces[eth["interface"]]["txrate"] > ifaces[eth["interface"]]["toptx"] else ifaces[eth["interface"]]["toptx"]

    time.sleep(INTERVAL)
    final = ifaces
    set = set + 1


for interfaceData in interfaceList:
        interfaceName = interfaceData["interfaceName"]
	interfaceData.update({"bandwidthInfo" : final[interfaceName]})



listeningConnectionsList = []
listeningConnections,_,_,_ = Library.commandExecute("netstat -tulpn | sed -n 2,1000p | grep LISTEN")
listeningConnections = listeningConnections.splitlines()

for connections in listeningConnections:
        connections = re.sub(r'\s+',' ',connections)
        connection =  connections.split(" ")
	connectionData = {
				"protocol" : connection[0],
				"localAddress" : connection[3],
				"foreignAddress" : connection[4],
				"processID" : connection[6].split("/")[0],
				"service" : connection[6].split("/")[1]
	
			 }
	listeningConnectionsList.append(connectionData)


gatewayInformation,_,_,_ = Library.commandExecute("netstat -rn | grep 0.0.0.0 | awk {'print $2'}")
gatewayInformation = gatewayInformation.split("\n")
for index in gatewayInformation:
	if index != "0.0.0.0":
		gateway = index
		break

pingIPs = [ gateway,"127.0.0.1"]
pingNames = ["gateway","loopback"]

pingData = []
counter = 0
for ips in pingIPs:
	pingStats,_,_,_ = Library.commandExecute("ping " + ips + " -c 1 | grep rtt")
	pingTime = pingStats.split("/")[5]
	pingData.append({pingNames[counter] : float(pingTime)})
	counter = counter + 1


networkStats = {
	"connectionState" : network,
	"pingTimings" : pingData,
	"servicesStats" : listeningConnectionsList,
	"interfaceData" : interfaceList,
		}
print networkStats
