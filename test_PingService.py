# Test class to test the Ping service
import pytest
import PQ9Client
import time
from PQ9TestHelpers import getAddress

def test_SinglePing(pq9_connection, destination):
    command = {}
    command["_send_"] = "Ping"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    startTime = time.time()
    succes, msg = pq9_connection.processCommand(command)
    elapsedTime = time.time() - startTime
    assert succes == True, "System is not responding"
    print("Elapsed time: ", round(elapsedTime * 1000, 0), " ms")
    
def test_MultiplePing(pq9_connection, destination):
    repeat = 1000
    command = {}
    command["_send_"] = "Ping"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    count = 0
    startTime = time.time()
    for i in range(repeat):
        succes, msg = pq9_connection.processCommand(command)
        if (succes == True):
        	count+= 1
    elapsedTime = time.time() - startTime
    print("Elapsed time: ", round(elapsedTime * 1000, 0), " ms")
    print("Responses ", count, "/", repeat)
    assert count == repeat, "Missing reponses"    

def test_PingWithExtraBytes(pq9_connection, destination):
    repeat = 254
    command = {}
    command["_send_"] = "SendRaw"
    command["dest"] = getAddress(destination)
    command["src"] = getAddress('EGSE')   
    count = 0
    startTime = time.time()
    for i in range(repeat):
        command["data"] = "17 1" + ( " 0" * i)
        succes, msg = pq9_connection.processCommand(command)
        #report if one frame is missing
        if (succes != True):
        	print("Frame", i, "not received:", command)
        else:
        	count+= 1
    elapsedTime = time.time() - startTime
    print("Elapsed time: ", round(elapsedTime * 1000, 0), " ms")
    print("Responses ", count, "/", repeat)
    assert count == repeat, "Missing reponses"
