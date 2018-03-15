import Library
import re


cpuStaticInfo,_,_,_ = Library.commandExecute("lscpu")

cpuCores = int(Library.findBetween(cpuStaticInfo,"CPU(s):","\n").strip())


cpuDynamicInfo = re.sub(r'\s+', ' ',Library.commandExecute("mpstat | tail -1")[0])
cpuDynamicInfo = cpuDynamicInfo.split(" ")
cpuPercentUserAll = float(cpuDynamicInfo[3])
cpuPercentKernelAll = float(cpuDynamicInfo[5])
cpuPercentTotalAll = round(100.00 - float(cpuDynamicInfo[12]), 2)

perCpuStats = []

for index in range(0,cpuCores ):
	cpuDynamicInfo = re.sub(r'\s+', ' ',Library.commandExecute("mpstat -P " + str(index) + " | tail -1")[0])
	cpuDynamicInfo = cpuDynamicInfo.split(" ")
	cpuPercentUser = float(cpuDynamicInfo[3])
	cpuPercentKernel = float(cpuDynamicInfo[5])
	cpuPercentTotal = round(100 - float(cpuDynamicInfo[12]),2)
	perCpuData = {
			"cpuCore" : index,
			"cpuPercentUser" : cpuPercentUser,
			"cpuPercentKernel" : cpuPercentKernel,
			"cpuPercentTotal" : cpuPercentTotal,
		     }

	perCpuStats.append(perCpuData)



averageLoad = Library.commandExecute("uptime | awk -F'[a-z]:' '{ print $2}'")[0].split(",")
average1 = float(averageLoad[0])
average2 = float(averageLoad[1])
average3 = float(averageLoad[2])

averageLoad = {
		"averageLoad1min" : average1,
		"averageLoad5min" : average2,
		"averageLoad15min" : average3
	      }

cpuDynamicData = {
			"allCpuData" : {
						"cpuPercentUser" : cpuPercentUserAll,
						"cpuPercentKernel":cpuPercentKernelAll,
						"cpuPercentTotal":cpuPercentTotalAll,
				       },
			"perCpuData" : perCpuStats,
			"averageLoad" : averageLoad
		 }

print cpuDynamicData
