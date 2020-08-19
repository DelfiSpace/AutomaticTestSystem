# EPS-specific test cases
import pytest
import sys
import json
import time

from PQ9TestHelpers import getAddress
import PQ9Client

def getBusVoltageVariable(i):
   switcher={
      '1':"Bus1Voltage",
      '2':"Bus2Voltage",
      '3':"Bus3Voltage",
      '4':"Bus4Voltage",
      }
   return str(switcher.get(i,0))

def getBusState(i):
   switcher={
      '1':"Bus1State",
      '2':"Bus2State",
      '3':"Bus3State",
      '4':"Bus4State",
      }
   return str(switcher.get(i,0))

def getBusError(i):
   switcher={
      '1':"Bus1Error",
      '2':"Bus2Error",
      '3':"Bus3Error",
      '4':"Bus4Error",
      }
   return str(switcher.get(i,0))
   
def test_EPS(pq9_connection, destination):
    print("EPS specific tests")
    
def test_EPSPowerBus(pq9_connection, destination):
    
    ret1 = commandBus(pq9_connection, destination, "1")
    ret2 = commandBus(pq9_connection, destination, "2")
    ret3 = commandBus(pq9_connection, destination, "3")
    ret4 = commandBus(pq9_connection, destination, "4")
    
    # print eventual errors (if any)
    if ret1 != "":
    	print(ret1)
    if ret2 != "":
    	print(ret2)
    if ret3 != "":
    	print(ret3)
    if ret4 != "":
    	print(ret4)
    
    # make the test fail in case an error message was returned
    assert (ret1 == "") and (ret2 == "") and (ret3 == "") and (ret4 == "")
            
def t_EPSPowerBusWrongBus(pq9_connection, destination):
    commandPBC = {}
    commandPBC["_send_"] = "SendRaw"
    commandPBC["dest"] = getAddress(destination)
    commandPBC["src"] = getAddress('EGSE')
    for i in range(256):
        if (i == 1) or (i == 2) or (i == 3) or (i == 4):
            continue
        commandPBC["data"] = "1 1 " + str(i) + " 1"
        succes, msg = pq9_connection.processCommand(commandPBC)
        assert succes == True, "Error: System is not responding"
        # check that the correct response was received
        assert msg["_received_"] == "PowerBusReply", "Incorrect response: expected \"PowerBusReply\" but found " + msg["_received_"]
        assert json.loads(msg["PowerBus"])["value"] == "Error", "Incorrect response: expected \"Error\" but found " + json.loads(msg["PowerBus"])["value"]

def commandBus(pq9_connection, destination, bus):
    commandPBC = {}
    commandPBC["_send_"] = "PowerBusControl"
    commandPBC["Destination"] = destination
    commandPBC["Source"] = "EGSE"
    commandPBC["PowerBus"] = bus
    commandPBC["State"] = "ON"
    
    commandTLM = {}
    commandTLM["_send_"] = "GetTelemetry"
    commandTLM["Destination"] = destination
    commandTLM["Source"] = "EGSE"
    
    succes, msg = pq9_connection.processCommand(commandPBC)
    if succes != True:
        return "Error: System is not responding to bus control request"
        
    # check that the correct response was received
    if msg["_received_"] != "PowerBusReply":
        return "Incorrect response: expected \"PowerBusReply\" but found " + msg["_received_"]
    if json.loads(msg["PowerBus"])["value"] != bus:
        return "Incorrect response: expected \"" + bus + "\" but found " + json.loads(msg["PowerBus"])["value"]
    if json.loads(msg["State"])["value"] != "ON":
        return "Incorrect response: expected \"ON\" but found " + json.loads(msg["State"])["value"]

    # sleep to give time for the change to be captured in telemetry
    time.sleep(1.3)
	
	# acquire telemetry to check
    succes, msg = pq9_connection.processCommand(commandTLM)
    if succes != True:
        return "Error: System is not responding to telemetry request"
        
    # check if the bus voltage is reasonable
    busVoltage = float(json.loads(msg[getBusVoltageVariable(bus)])["value"])
    if busVoltage < 2.7:
    	return "Bus " + bus + " voltage too low: " + str(busVoltage) + " V (supposed to be ON)"
    
    # check if bus state is correct
    busState = json.loads(msg[getBusState(bus)])["value"]
    if busState != "ON":
        return "Bus " + bus + " not ON (supposed to be ON)"
    
    # check if bus status is correct
    busStatus = json.loads(msg[getBusError(bus)])["value"]
    if busStatus != "Active":
        return "Bus " + bus + " not Active (supposed to be Active)"
    
    commandPBC["PowerBus"] = bus
    commandPBC["State"] = "OFF"
    succes, msg = pq9_connection.processCommand(commandPBC)
    if succes != True:
        return "Error: System is not responding to bus control request"
    # check that the correct response was received
    if msg["_received_"] != "PowerBusReply":
        return "Incorrect response: expected \"PowerBusReply\" but found " + msg["_received_"]
    if json.loads(msg["PowerBus"])["value"] != bus:
        return "Incorrect response: expected \"" + bus + "\" but found " + json.loads(msg["PowerBus"])["value"]
    if json.loads(msg["State"])["value"] != "OFF":
        return "Incorrect response: expected \"OFF\" but found " + json.loads(msg["State"])["value"]

    # sleep to give time for the change to be captured in telemetry
    time.sleep(1.3)
    
    # acquire telemetry to check
    succes, msg = pq9_connection.processCommand(commandTLM)
    if succes != True:
        return "Error: System is not responding to telemetry request"
    
    # check if the bus voltage is reasonable
    busVoltage = float(json.loads(msg[getBusVoltageVariable(bus)])["value"])
    if busVoltage > 0.1:
        return "Bus " + bus + " voltage too high: " + str(busVoltage) + " V (supposed to be OFF)"
    
    # check if bus state is correct
    busState = json.loads(msg[getBusState(bus)])["value"]
    if busState != "OFF":
        return "Bus " + bus + " not OFF (supposed to be OFF)"
    
    # check if bus status is correct
    busStatus = json.loads(msg[getBusError(bus)])["value"]
    if busStatus != "Active":
        return "Bus " + bus + " not Active (supposed to be Active)"
    
    return ""