# Radio emulator
from PQ9Client import PQ9Client
from RadioEmulator import RadioEmulator
import time
import configparser

if __name__ == "__main__":
    # retrieve the configuration parameters from the test initialization file
    config = configparser.ConfigParser()
    config.read('TestConfig.ini')

    # create the pq9client object using the configuration parameters
    pq9client = PQ9Client(config['PQ9EGSE']['server'], config['PQ9EGSE']['port'], int(config['PQ9EGSE']['timeout']))
    pq9client.connect()

    # create the radio emulator object and start it
    emulator = RadioEmulator(pq9client)
    emulator.start()
    
    # wait a little at the beginning
    time.sleep(3)
    
    # set a custom transmitted message handler to handle the housekeeping request
    emulator.setTXMessageHandler(lambda reply: print("Housekeeping request reply: " + str(reply)))
    
    # queue a PQ9 request to OBC (1) with a payload size (2) from Ground (8) for a housekeeping (3) request(1)
    emulator.newRXMessage([1, 2, 8, 3, 1])
    
    # wait for the message to be picked up by the OBC and a response to be generated
    time.sleep(2)

    # set a custom transmitted message handler to handle the ping request
    emulator.setTXMessageHandler(lambda reply: print("Ping request reply: " + str(reply)))
    
    # queue a PQ9 request to OBC (1) with a payload size (2) from Ground (8) for a Ping (17) request(1)
    emulator.newRXMessage([1, 2, 8, 17, 1])
    
    # wait for the message to be picked up by the OBC and a response to be generated
    time.sleep(2)
    
    # set a custom transmitted message handler to handle the housekeeping request
    emulator.setTXMessageHandler(lambda reply: print("Housekeeping request reply: " + str(reply)))
    
    # queue a PQ9 request to OBC (1) with a payload size (2) from Ground (8) for a housekeeping (3) request(1)
    emulator.newRXMessage([1, 2, 8, 3, 1])
    
    # wait some time to observe the normal OBC behaviour
    time.sleep(40)
    
    # close the radio emulator and the pq9client connection
    emulator.close()
    pq9client.close()
