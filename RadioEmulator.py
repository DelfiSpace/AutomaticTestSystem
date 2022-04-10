# Radio emulator
from PQ9Client import PQ9Client, PQ9ClientConnectionClosed
from SubSystemEmulator import SubSystemEmulator
import PQ9TestHelpers
import configparser
from threading import Thread

class RadioEmulator(SubSystemEmulator):

    def __init__(self, pq9_connection):
        super().__init__(pq9_connection, "COMMS")
        self.uplinkMessages = []
        self.TXmessageHandler = None
        
    def newRXMessage(self, msg):
        # limit the number of messages in the queue to 255
        if len(self.uplinkMessages) < 256:
            self.uplinkMessages.append(msg)
        
    def setTXMessageHandler(self, handler):
        self.TXmessageHandler = handler
            
    def checkMessage(self, msg):
        # is there a raw key in the dictionary?      
        if "_raw_" in msg:
            # turn the key into a n int array
            raw_message = eval(msg['_raw_'])
            
            # only handle messages to COMMS
            if raw_message[0] == int(PQ9TestHelpers.getAddress(self.address)):
                # is a Radio service request?
                if raw_message[3] == 25 and raw_message[4] == 1:
                    
                    # is a get RX messages number request?
                    if raw_message[5] == 3:
                        # send a PQ 9 message to tell how many messages are in the queue
                        command = {}
                        command["_send_"] = "SendRaw"
                        command["dest"] = str(raw_message[2])
                        command["src"] = PQ9TestHelpers.getAddress(self.address)
                        command["data"] = "25 2 0 " + str(len(self.uplinkMessages)) 
                        self.pq9Handler.sendFrame(command)
                        
                    # is a delete RX messages request?
                    elif raw_message[5] == 5:
                        # prepare the response message
                        command = {}
                        command["_send_"] = "SendRaw"
                        command["dest"] = str(raw_message[2])
                        command["src"] = PQ9TestHelpers.getAddress(self.address)
                        
                        # if there is at least one element, remove it
                        if len(self.uplinkMessages) > 0:
                            self.uplinkMessages.pop(0)
                            # send a PQ 9 message to tell success                        
                            command["data"] = "25 2 0" 
                        else:
                            # send a PQ message to say invalid value
                            command["data"] = "25 2 2"
                        self.pq9Handler.sendFrame(command)
        
                    # is a get RX message request?
                    elif raw_message[5] == 4:
                        if len(self.uplinkMessages) > 0:
                            # send a PQ 9 message to tell how many messages are in the queue
                            command = {}
                            command["_send_"] = "SendRaw"
                            command["dest"] = str(raw_message[2])
                            command["src"] = PQ9TestHelpers.getAddress(self.address)
                            command["data"] = "25 2 0 3 " + " ".join([str(i) for i in self.uplinkMessages[0]])
                            self.pq9Handler.sendFrame(command)
                         
                    # is a get send message request?
                    elif raw_message[5] == 9:
                        if self.TXmessageHandler != None:
                            # only extract the message payload
                            self.TXmessageHandler(raw_message[7:-2])
                        
                    else:
                        print(str(msg))
                        
                # is a telemetry service request?
                elif raw_message[3] == 3 and raw_message[4] == 1:
                    print("Telemetry request")
