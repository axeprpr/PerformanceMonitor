from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import *
from flask.ext.jsonpify import jsonify
from pymongo import MongoClient
import pymongo
import requests
import json
import Library

app = Flask(__name__)
api = Api(app)


client = MongoClient("192.168.10.111", 27017 )
db = client["PerformanceMonitor"]


class getSystemInfo(Resource):
	def get(self):
		collection = db['systemInfo']
		systemInfo = collection.find()
		systemInfo = systemInfo[0]	
		del systemInfo["_id"]
		print type(systemInfo)
		return systemInfo


class getCpuStatics(Resource):
	def get(self):
		collection = db['cpuStatics']
		cpuInfo = collection.find()
		cpuInfo = cpuInfo[0]
		del cpuInfo["_id"]
		return cpuInfo
		

class getDiskStatics(Resource):
	def get(self):
		collection = db['diskStatics']
		diskInfo = collection.find()
		diskInfo = diskInfo[0]
		del diskInfo["_id"]
		return diskInfo
		


class getMemoryStatics(Resource):
	def get(self):
		collection = db['memoryStatics']
		memoryDynamicsmemoryInfo = collection.find()
		memoryInfo = memoryInfo[0]
		del memoryInfo["_id"]
		return memoryInfo
		


class getAllStaticData(Resource):
	def get(self):
		collection = db['systemInfo']
                systemInfo = collection.find()
                systemInfo = systemInfo[0]
                del systemInfo["_id"]
                collection = db['cpuStatics']
                cpuInfo = collection.find()
                cpuInfo = cpuInfo[0]
                del cpuInfo["_id"]
                collection = db['diskStatics']
                diskInfo = collection.find()
                diskInfo = diskInfo[0]
                del diskInfo["_id"]
                collection = db['memoryStatics']
                memoryInfo = collection.find()
                memoryInfo = memoryInfo[0]
                del memoryInfo["_id"]

		allStatic = {
			"systemInfo" : systemInfo,
			"cpuInfo" : cpuInfo,
			"diskInfo" : diskInfo,
			"memoryInfo" : memoryInfo,

		            }
		return allStatic


class getRealTimeFileMonitor(Resource):
        def get(self):
		fileMonitor,_,_,_ = Library.commandExecute("python monitorFiles.py")
		fileMonitor = json.loads(fileMonitor.replace('\'', '\"'))
		return fileMonitor

class getRealTimeProcessMonitor(Resource):
        def get(self):
                processMonitor,_,_,_ = Library.commandExecute("python monitorProcess.py")
                processMonitor = json.loads(processMonitor.replace('\"','\\\'').replace('\'', '\"'))
                return processMonitor



class addFileToMonitor(Resource):
	def get(self):
		if 'filePath' in request.args:
                        if request.args['filePath'] == "":
                                return {'Error':'Empty parameters'}
                        _,_,code,_ = Library.commandExecute("ls -lart " + request.args['filePath'])
			if code != 0:
				return {'Error' : 'File path not found'}
			else:
				_,_,code,_ = Library.commandExecute("cat monitorFilesList.txt | grep -w \"" + request.args['filePath'] + "\"")
				if code == 0:
                                	return {'Error' : 'File already Exists'}
				else:
					Library.commandExecute("echo \"" + request.args['filePath'] + "\" >> monitorFilesList.txt")
					return {'Success' : 'File added for monitoring ' + request.args['filePath']}

                else:
                        return {'Error' : 'Data not passed'}


class addProcessToMonitor(Resource):
	def get(self):
		if 'processName' in request.args:
                        if request.args['processName'] == "":
                                return {'Error':'Empty parameters'}
			else:
				_,_,code,_ = Library.commandExecute("cat monitorProcessList.txt | grep -w \"" + request.args['processName'] + "\"")
				if code == 0:
                                	return {'Error' : 'Process already added for monitoring'}
				else:
					Library.commandExecute("echo \"" + request.args['processName'] + "\" >> monitorProcessList.txt")
					return {'Success' : 'Process added for monitoring ' + request.args['processName']}
                else:
                        return {'Error' : 'Data not passed'}


class removeProcessToMonitor(Resource):
	def get(self):
		if 'processName' in request.args:
                        if request.args['processName'] == "":
                                return {'Error':'Empty parameters'}
                        else:
				lineNumber,_,_,_ = Library.commandExecute("grep -n  " + request.args['processName'] + "$ monitorProcessList.txt |sed 's/:/ /' |awk '{print $1}'")
				if lineNumber.strip() == "":
					return {"Error" : "No such process"}
				else:
					Library.commandExecute("sed -i -e  '"+ lineNumber.strip() + "d' monitorProcessList.txt")
					return {"Success" : "File removed from monitoring"}
		else:
                        return {'Error' : 'Data not passed'}
		

class removeFileToMonitor(Resource):
	def get(self):
		if 'filePath' in request.args:
                        if request.args['filePath'] == "":
                                return {'Error':'Empty parameters'}
                        else:
				lineNumber,_,_,_ = Library.commandExecute("grep -n  " + request.args['filePath'] + "$ monitorFilesList.txt |sed 's/:/ /' |awk '{print $1}'")
				if lineNumber.strip() == "":
					return {"Error" : "No such file path"}
				else:
					Library.commandExecute("sed -i -e  '"+ lineNumber.strip() + "d' monitorFilesList.txt")
					return {"Success" : "File removed from monitoring"}
		else:
                        return {'Error' : 'Data not passed'}
		




class getRealTimeCpu(Resource):
        def get(self):
		cpuStats,_,_,_ = Library.commandExecute("python cpuStatsDynamic.py")
		cpuStats = json.loads(cpuStats.replace('\'', '\"'))
                return cpuStats

class getRealTimeDisk(Resource):
        def get(self):
		diskStats,_,_,_ = Library.commandExecute("python diskStatsDynamic.py")
		diskStats = json.loads(diskStats.replace('\'', '\"'))
                return diskStats

class getRealTimeMemory(Resource):
        def get(self):
		memoryStats,_,_,_ = Library.commandExecute("python memoryStatsDynamic.py")
		memoryStats = json.loads(memoryStats.replace('\'', '\"'))
                return memoryStats

class getRealTimeNetwork(Resource):
        def get(self):
		networkStats,_,_,_ = Library.commandExecute("python networkStats.py")
		networkStats = json.loads(networkStats.replace('\'', '\"'))
		return networkStats


class getNetConnectivity(Resource):
        def get(self):
		networkStats,_,_,_ = Library.commandExecute("python netConnect.py")
		networkStats = json.loads(networkStats.replace('\'', '\"'))
		return networkStats



class getRealTimePerInterface(Resource):
        def get(self):
		if 'interface' in request.args:
                        if request.args['interface'] == "":
                                return {'Error':'Empty parameters'}
			networkStats,_,_,_ = Library.commandExecute("python networkStats.py")
			networkStats = json.loads(networkStats.replace('\'', '\"'))
                        interfaceData = networkStats["interfaceData"]
                        for interface in interfaceData:
                                if interface['interfaceName'] == request.args['interface'].strip():
                                        return interface
                                else:
                                        continue
                        return {'Error' : 'Interface name not found'}
                else:
                        return {'Error' : 'Data not passed'}




class getTopStats(Resource):
        def get(self):
		topStats,_,_,_ = Library.commandExecute("python topStats.py")
		topStats = json.loads(topStats.replace('\'', '\"'))	
		return topStats


class getDfStats(Resource):
        def get(self):
                dfStats,_,_,_ = Library.commandExecute("python dfStats.py")
                dfStats = json.loads(dfStats.replace('\'', '\"'))       
                return dfStats



class getNetstat(Resource):
        def get(self):
                netstatOut,_,_,_ = Library.commandExecute("python netstatOut.py")
                netstatOut = json.loads(netstatOut.replace('\'', '\"'))       
                return netstatOut


class getActiveUsers(Resource):
        def get(self):
                activeUsers,_,_,_ = Library.commandExecute("python activeUsers.py")
                activeUsers = json.loads(activeUsers.replace('\'', '\"'))       
                return activeUsers



class getLastLogin(Resource):
        def get(self):
                lastLogin,_,_,_ = Library.commandExecute("python lastLogin.py")
                lastLogin = json.loads(lastLogin.replace('\'', '\"'))       
                return lastLogin

class getAllMemoryStats(Resource):
	def get(self):
		collection = db['memoryDynamics']
                currentMemory = collection.find().sort("timestamp" ,pymongo.DESCENDING)
		allMemoryStats = []
		for current in currentMemory:
			del current["_id"]
			allMemoryStats.append(current)
		return allMemoryStats

class getAllCpuStats(Resource):
	def get(self):
		collection = db['cpuDynamics']
                currentCpu = collection.find().sort("timestamp" ,pymongo.DESCENDING)
		allCpuStats = []
		for current in currentCpu:
			del current["_id"]
			allCpuStats.append(current)
		return allCpuStats


class getAllNetworkStats(Resource):
	def get(self):
		collection = db['networkStats']
                currentCpu = collection.find().sort("timestamp" ,pymongo.DESCENDING)
		allCpuStats = []
		for current in currentCpu:
			del current["_id"]
			allCpuStats.append(current)
		return allCpuStats


class getAllFileMonitor(Resource):
	def get(self):
		collection = db['fileMonitor']
		fileList,_,_,_ = Library.commandExecute("cat monitorFilesList.txt")
		fileList = fileList.splitlines()
		allFilesData = []
		for filePath in fileList:
			fileData = collection.find({"name" : filePath.strip()}).sort("timestamp" ,pymongo.DESCENDING)
			for data in fileData:
				del data["_id"]
				allFilesData.append(data)
		return allFilesData

class getAllProcessMonitor(Resource):
	def get(self):
		collection = db['processMonitor']
		processList,_,_,_ = Library.commandExecute("cat monitorProcessList.txt")
                processList = processList.splitlines()
		allProcessData = []
		for processName in processList:
			print processName
		        pIds = Library.getProcessID(processName)
			if pIds[1] == 0:
		                continue
			else:
				for pid in pIds[1]:
					print pid
					print {"name" : processName.strip(),"processId" : int(pid)}
					processData = collection.find({"name" : processName.strip(),"processId" : int(pid.strip())})
					for data in processData:
						del data["_id"]
						allProcessData.append(data)
		return allProcessData


class getAllDiskStats(Resource):
	def get(self):
		collection = db['diskDynamics']
                currentDisk = collection.find().sort("timestamp" ,pymongo.DESCENDING)
		allDiskStats = []
		for current in currentDisk:
			del current["_id"]
			allDiskStats.append(current)
		return allDiskStats




class getCurrentMemory(Resource):
	def get(self):
		collection = db['memoryDynamics']
		currentMemory = collection.find().sort("timestamp" ,pymongo.DESCENDING)[0]
		del currentMemory["_id"]
		print currentMemory
		return currentMemory


class getCurrentCpu(Resource):
	def get(self):
		collection = db['cpuDynamics']
		currentCpu = collection.find().sort("timestamp" ,pymongo.DESCENDING)[0]
		del currentCpu["_id"]
		print currentCpu
		return currentCpu



class getNetworkStats(Resource):
        def get(self):
                collection = db['networkStats']
                networkStats = collection.find().sort("timestamp" ,pymongo.DESCENDING)[0]
                del networkStats["_id"]
                return networkStats


class getCurrentDisk(Resource):
        def get(self):
                collection = db['diskDynamics']
                currentDisk = collection.find().sort("timestamp" ,pymongo.DESCENDING)[0]
                del currentDisk["_id"]
                return currentDisk


class getPerInterfaceStats(Resource):
        def get(self):
		if 'interface' in request.args:
			if request.args['interface'] == "":
				return {'Error':'Empty parameters'}
			collection = db['networkStats']
			networkStats = collection.find().sort("timestamp" ,pymongo.DESCENDING)[0]
			del networkStats["_id"]
			interfaceData = networkStats["interfaceData"]
			for interface in interfaceData:
				if interface['interfaceName'] == request.args['interface'].strip():
					return interface
				else:
					continue
			return {'Error' : 'Interface name not found'}
		else:
			return {'Error' : 'Data not passed'}


api.add_resource(getSystemInfo, '/getSystemInfo') 
api.add_resource(getCpuStatics, '/getCpuStatics')
api.add_resource(getMemoryStatics, '/getMemoryStatics') 
api.add_resource(getDiskStatics, '/getDiskStatics') 
api.add_resource(getAllStaticData, '/getAllStaticData') 
api.add_resource(getTopStats, '/getTopStats') 
api.add_resource(getDfStats, '/getDfStats') 
api.add_resource(getNetstat, '/getNetstat') 
api.add_resource(getActiveUsers, '/getActiveUsers') 
api.add_resource(getLastLogin, '/getLastLogin') 
api.add_resource(getCurrentMemory, '/getCurrentMemory')
api.add_resource(getCurrentCpu, '/getCurrentCpu')
api.add_resource(getCurrentDisk, '/getCurrentDisk')
api.add_resource(getNetworkStats, '/getNetworkStats')
api.add_resource(getPerInterfaceStats, '/getPerInterfaceStats')
api.add_resource(getRealTimeCpu, '/getRealTimeCpu')
api.add_resource(getRealTimeDisk, '/getRealTimeDisk')
api.add_resource(getRealTimeMemory, '/getRealTimeMemory')
api.add_resource(getRealTimeNetwork, '/getRealTimeNetwork')
api.add_resource(getRealTimePerInterface, '/getRealTimePerInterface')
api.add_resource(getNetConnectivity, '/getNetConnectivity')
api.add_resource(getRealTimeFileMonitor, '/getRealTimeFileMonitor')
api.add_resource(getRealTimeProcessMonitor, '/getRealTimeProcessMonitor')
api.add_resource(addFileToMonitor, '/addFileToMonitor')
api.add_resource(addProcessToMonitor, '/addProcessToMonitor')
api.add_resource(removeProcessToMonitor, '/removeProcessToMonitor')
api.add_resource(removeFileToMonitor, '/removeFileToMonitor')
api.add_resource(getAllMemoryStats, '/getAllMemoryStats')
api.add_resource(getAllCpuStats, '/getAllCpuStats')
api.add_resource(getAllDiskStats, '/getAllDiskStats')
api.add_resource(getAllNetworkStats, '/getAllNetworkStats')
api.add_resource(getAllFileMonitor, '/getAllFileMonitor')
api.add_resource(getAllProcessMonitor, '/getAllProcessMonitor')




if __name__ == '__main__':
     app.run(port=5002)

		

