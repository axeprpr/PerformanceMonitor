import subprocess
import time
import sys
import fileinput
import string
import random
import os
import socket
import datetime
from datetime import datetime

def GetNetworkInterfaces():
    ifaces = []
    f = open("/proc/net/dev")
    data = f.read()
    f.close()
    data = data.split("\n")[2:]
    for i in data:
        if len(i.strip()) > 0:
            x = i.split()
            # Interface |                        Receive                          |                         Transmit
            #   iface   | bytes packets errs drop fifo frame compressed multicast | bytes packets errs drop fifo frame compressed multicast
            k = {
                "interface" :   x[0][:len( x[0])-1],
                "tx"        :   {
                    "bytes"         :   int(x[1]),
                    "packets"       :   int(x[2]),
                    "errs"          :   int(x[3]),
                    "drop"          :   int(x[4]),
                    "fifo"          :   int(x[5]),
                    "frame"         :   int(x[6]),
                    "compressed"    :   int(x[7]),
                    "multicast"     :   int(x[8])
                },
                "rx"        :   {
                    "bytes"         :   int(x[9]),
                    "packets"       :   int(x[10]),
                    "errs"          :   int(x[11]),
                    "drop"          :   int(x[12]),
                    "fifo"          :   int(x[13]),
                    "frame"         :   int(x[14]),
                    "compressed"    :   int(x[15]),
                    "multicast"     :   int(x[16])
                }
            }
            ifaces.append(k)
    return ifaces




def printDict(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s{' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                printDict(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


def getProcessID(name):
        so,_,_,_= commandExecute("ps -ef | grep " + name + " | grep -v grep | awk '{print $2}'")
        so=so.splitlines()
        if len(so) != 1 :
                return 0
        elif len(so) == 1:
                return so
        else:
                return 0



def isConnected(hostname):
      try:
         host = socket.gethostbyname(hostname)
         s = socket.create_connection((host, 80), 2)
         return True
      except:
         return False


def commandExecute(command):
	process = subprocess.Popen(command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdout, stderr) = process.communicate()
	SUCCESS_OUTPUT=stdout
	ERROR_OUTPUT=stderr
	EXIT_CODE=process.returncode
	PROCESS_ID=process.pid
	return (SUCCESS_OUTPUT,ERROR_OUTPUT,EXIT_CODE,PROCESS_ID)





def findBetween(string, first, last):
   	try:
        	start = string.index( first ) + len( first )
        	end = string.index( last, start )
        	return string[start:end]
    	except ValueError:
        	return ""





def getProcessID(name):
	processNames,_,_,_ =commandExecute("ps -ef | grep " + name + " | grep -v grep | awk '{$1=$2=$3=$4=$5=$6=$7=\"\"; print $0}'")
	processNames = processNames.splitlines()

	so,_,_,_= commandExecute("ps -ef | grep " + name + " | grep -v grep | awk '{print $2}'")
	so=so.splitlines()
	if len(so) > 0:
                return processNames,so
	else:
		return 0,0

def getPIDstats(pid):
    try:
        if len(pid.split()) == 1:
                percentageCPU,_,_,_=commandExecute("pidstat -ru | grep -w " + pid + " | sed -n '1p' | awk {'print $8'}")
                CPUnumber,_,_,_=commandExecute("pidstat -ru | grep -w " + pid + " | sed -n '1p' | awk {'print $9'}")
                vsz,_,_,_=commandExecute("pidstat -ru | grep -w " + pid + " | sed -n '2p' | awk {'print $7'}")
                rss,_,_,_=commandExecute("pidstat -ru | grep -w " + pid + " | sed -n '2p' | awk {'print $8'}")
                percentageMEM,_,_,_=commandExecute("pidstat -ru | grep -w " + pid + " | sed -n '2p' | awk {'print $9'}")
                startTime,_,_,_=commandExecute("ps -eo pid,lstart | grep  -w " + pid + " | awk -v OFS=' ' '{print $3, $4, $5, $6}'")
                totalBytesRead,_,_,_=commandExecute("cat /proc/" + pid + "/io | grep 'read_bytes:' | awk '{print $2}'")
                totalBytesWritten,_,_,_=commandExecute("cat /proc/" + pid + "/io | grep '^write_bytes:' | awk '{print $2}'")
                kbReadPerSec,_,_,_=commandExecute("pidstat  -p ALL -dl | grep -w " + pid +" | grep -v grep |awk '{print $5}'")
                kbWrittenPerSec,_,_,_=commandExecute("pidstat  -p ALL -dl | grep -w " + pid +" | grep -v grep | awk '{print $6}'")
                datetime_object = datetime.strptime(startTime.strip(), '%b %d %H:%M:%S %Y')
                return float(percentageCPU),int(CPUnumber),int(vsz),int(rss),float(percentageMEM),datetime_object,int(totalBytesRead),int(totalBytesWritten),float(kbReadPerSec),float(kbWrittenPerSec)

        else:
                return 0.00,0,0,0,0.00,datetime.strptime(startTime.strip(), '%b %d %H:%M:%S %Y'),0,0,0.00,0.00
    except:
	return 0.00,0,0,0,0.00,0,0,0,0.00,0.00






def Find_Replace_Line(FILE,Sstr,Rstr): # Find and replace a line in file
	x = fileinput.input(files=FILE, inplace=1)
	for line in x:
		if Sstr in line:
			line = Rstr + "\n"
		print line,
	x.close()



def File_Content_Appender(FILE_PATH,STRING): # Appends the content to a file
	with open (FILE_PATH, "a") as myfile:
		myfile.write(STRING +"\n")

def File_Content_Writer(FILE_PATH,STRING): # Overwrite the conten to a file
	with open (FILE_PATH, "w") as myfile:
		myfile.write(STRING + "\n")


def yumInstaller(packageName,versionCheck=0,versionToCheck=''):
	time.sleep(2)
	yumStatus = getProcessID('yum')
	if yumStatus == 0:
		pass
	else:
		print 'KILLING'
		for index in yumStatus:
			commandExecute("kill -9 " + index)
		yumInstaller(packageName,versionCheck,versionToCheck)
	checkOutput,_,installCheck,_ = commandExecute("yum info installed " + packageName + " | grep Version")
	if installCheck == 0:
		successCheck=0
 		if versionCheck==1:
			version = findBetween(checkOutput,"Version     :","\n").strip()
			if version.strip() == versionToCheck.strip():
				successCheck=0
				print packageName + ' already installed'
				return 0
			else:
				installOutput,_,successCheck,_ = commandExecute('yum install ' + packageName + ' -y')
	
	else:
		installOutput,_,successCheck,_ = commandExecute('yum install ' + packageName + ' -y')
	
	if successCheck == 0:
		print packageName + ' installation successful\n' 
		return 0
	else:
		print packageName + ' installation failed'
		return 1




def installPackage(packageName):
	installStatus=yumInstaller(packageName)
	if installStatus == 1:
		"FATAL ERROR: " + packageName + " installation failed"
		sys.exit(10)
	


	
