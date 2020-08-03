# content of test_sysexit.py
import pytest
import PQ9Client
import time
import json
from PQ9TestHelpers import getAddress

def test_SoftReset(pq9_connection, destination):
    print("This function tests the board Soft Reset by requesting the board uptime, performing a soft reset and requesting the uptime again.")
    print()
    
    command = {}
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])
    if( uptimeBeforeReset < 3 ):
        time.sleep(3 - uptimeBeforeReset)
        succes, msg = pq9_connection.processCommand(command)
        assert succes == True, "Error: System is not responding"
        uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])
    print("Uptime before reset:", uptimeBeforeReset, "s")
    
    command["_send_"] = "Reset"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    command["Type"] = "Soft"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "System is not responding"
    time.sleep(1)
    
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeAfterReset = int(json.loads(msg["Uptime"])["value"])
    assert uptimeAfterReset < 2, "Error: Board did not reset"
    print("Uptime after reset:", uptimeAfterReset, "s")
    print("Soft Reset successful")

def test_HardReset(pq9_connection,destination):
    print("This function tests the board Hard Reset by requesting the board uptime, performing a hard reset and requesting the uptime again.")
    print()
    
    command = {}
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])
    if( uptimeBeforeReset < 3 ):
        time.sleep(3 - uptimeBeforeReset)
        succes, msg = pq9_connection.processCommand(command)
        assert succes == True, "Error: System is not responding"
        uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])
    print("Uptime before reset:", uptimeBeforeReset, "s")
        
    command["_send_"] = "Reset"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    command["Type"] = "Hard"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "System is not responding"
    time.sleep(1)
    
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeAfterReset = int(json.loads(msg["Uptime"])["value"])
    assert uptimeAfterReset < 2, "Error: Board did not reset"
    print("Uptime after reset:", uptimeAfterReset, "s")
    print("Hard Reset successful")

def test_PowerCycle(pq9_connection, destination):
    print("This function tests the board power cycle by requesting the board uptime, performing a power cycle and requesting the uptime again.")
    print()
    
    command = {}
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])

    if( uptimeBeforeReset < 3 ):
        time.sleep(3 - uptimeBeforeReset)
        succes, msg = pq9_connection.processCommand(command)
        assert succes == True, "Error: System is not responding"
        uptimeBeforeReset = int(json.loads(msg["Uptime"])["value"])
    print("Uptime before reset:", uptimeBeforeReset, "s")
        
    command["_send_"] = "Reset"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    command["Type"] = "PowerCycle"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "System is not responding"
    time.sleep(1)
    
    command["_send_"] = "GetTelemetry"
    command["Destination"] = destination
    command["Source"] = "EGSE"
    succes, msg = pq9_connection.processCommand(command)
    assert succes == True, "Error: System is not responding"
    uptimeAfterReset = int(json.loads(msg["Uptime"])["value"])
    assert uptimeAfterReset < 2, "Error: Board did not reset"
    print("Uptime after reset:", uptimeAfterReset, "s")
    print("Power Cycle successful")
