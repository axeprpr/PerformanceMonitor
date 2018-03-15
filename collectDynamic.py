import Library
import  json
import pymongo
from pymongo import MongoClient
import json
client = MongoClient("192.168.10.111", 27017 )
db = client["PerformanceMonitor"]



cpuDynamics,_,_,_ = Library.commandExecute("python cpuStatsDynamic.py")
print cpuDynamics.strip()
cpuDynamics = json.loads(cpuDynamics.replace('\'', '\"'))
collection = db["cpuDynamics"]
collection.drop()
collection.insert(cpuDynamics)
diskDynamics,_,_,_ = Library.commandExecute("python diskStatsDynamic.py")
print diskDynamics
diskDynamics = json.loads(diskDynamics.replace('\'', '\"'))
collection = db["diskDynamics"]
collection.drop()
collection.insert(diskDynamics)
memoryDynamics,_,_,_ = Library.commandExecute("python memoryStatsDynamic.py")
print memoryDynamics
memoryDynamics = json.loads(memoryDynamics.replace('\'', '\"'))
collection = db["memoryDynamics"]
collection.drop()
collection.insert(memoryDynamics)
networkStats,_,_,_ = Library.commandExecute("python networkStats.py")
print networkStats
networkStats = json.loads(networkStats.replace('\'', '\"'))
collection = db["networkStats"]
collection.drop()
collection.insert(networkStats)
