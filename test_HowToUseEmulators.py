import PQ9Client
import PQ9Emulators
import PQ9VirtualBus
import pytest
import time
from PQ9TestHelpers import getAddress

'''
1. If you want to test a single emulator:
pq9_connection = COMMSEmulator('4')
destination = '4'

2. If you want to send commands to a module through virtual COMMS and
real OBC:
commsEmu = COMMSEmulator('4')
pq9_connection = PQ9VirtualBus(PQ9Client, commsEmu, {'4':commsEmu})
destination = 'x'
'''
def test_SinglePing(pq9_connection, destination):    
    command = {}
    command["_send_"] = "SendRaw"
    command["dest"] = destination
    command["src"] = "8"
    command["data"] = "17 1"
    startTime = time.time()
    succes, msg = pq9_connection.processCommand(command)
    elapsedTime = time.time() - startTime
    assert succes == True, "System is not responding"
    print("Elapsed time: ", round(elapsedTime * 1000, 0), " ms")
