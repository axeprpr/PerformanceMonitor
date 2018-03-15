import Library
import re


cpuStaticInfo,_,_,_ = Library.commandExecute("lscpu")

cpuArchitecture = Library.findBetween(cpuStaticInfo,"Architecture:","\n").strip()
cpuOperationMode = Library.findBetween(cpuStaticInfo,"CPU op-mode(s):","\n").strip().split(",")
cpuCores = int(Library.findBetween(cpuStaticInfo,"CPU(s):","\n").strip())
threadsPerCore = int(Library.findBetween(cpuStaticInfo,"Thread(s) per core:","\n").strip())
coresPerSocket = int(Library.findBetween(cpuStaticInfo,"Core(s) per socket:","\n").strip())
numberOfSockets = int(Library.findBetween(cpuStaticInfo,"Socket(s):","\n").strip())
cpuVendor = Library.findBetween(cpuStaticInfo,"Vendor ID:","\n").strip()
cpuModel = Library.findBetween(cpuStaticInfo,"Model name:","\n").strip()

cpuStaticData = {
			"cpuArchitecture":cpuArchitecture,
			"cpuOperationMode":cpuOperationMode,
			"cpuCores":cpuCores,
			"threadsPerCore":threadsPerCore,
			"coresPerSocket":coresPerSocket,
			"numberOfSockets":numberOfSockets,
			"cpuVendor":cpuVendor,
			"cpuModel":cpuModel
		}


print cpuStaticData

