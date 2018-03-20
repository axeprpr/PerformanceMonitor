import Library

remoteServer = "www.google.com"
if Library.isConnected(remoteServer):
        network = {"networkState" : "Connected"}
else:
        network = {"networkState" : "Disconnected"}

print network
