import Library
import  json
import pymongo
from pymongo import MongoClient
import json
client = MongoClient("192.168.10.111", 27017 )
db = client["PerformanceMonitor"]



cpuStatics,_,_,_ = Library.commandExecute("python cpuStatsStatic.py")
print cpuStatics.strip()
cpuStatics = json.loads(cpuStatics.replace('\'', '\"'))
collection = db["cpuStatics"]
collection.drop()
collection.insert(cpuStatics)
diskStatics,_,_,_ = Library.commandExecute("python diskStatsStatic.py")
print diskStatics
diskStatics = json.loads(diskStatics.replace('\'', '\"'))
collection = db["diskStatics"]
collection.drop()
collection.insert(diskStatics)
memoryStatics,_,_,_ = Library.commandExecute("python memoryStatsStatic.py")
print memoryStatics
memoryStatics = json.loads(memoryStatics.replace('\'', '\"'))
collection = db["memoryStatics"]
collection.drop()
collection.insert(memoryStatics)
systemInfo,_,_,_ = Library.commandExecute("python systemInfo.py")
print systemInfo
systemInfo = json.loads(systemInfo.replace('\'', '\"'))
collection = db["systemInfo"]
collection.drop()
collection.insert(systemInfo)
