# Radio emulator
from PQ9Client import PQ9Client
from RadioEmulator import RadioEmulator
import time
import configparser

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('TestConfig.ini')

    pq9client = PQ9Client(config['PQ9EGSE']['server'], config['PQ9EGSE']['port'], int(config['PQ9EGSE']['timeout']))
    pq9client.connect()

    emulator = RadioEmulator(pq9client)
    emulator.start()
    
    time.sleep(3)
    # queue a PQ9 request to OBC (1) from Ground (8) for a housekeeping (3) request(1)
    emulator.newRXMessage([1, 5, 8, 3, 1])
    
    # queue a PQ9 request to OBC (1) from Ground (8) for a Ping (17) request(1)
    emulator.newRXMessage([1, 5, 8, 17, 1])
    
    # queue a PQ9 request to OBC (1) from Ground (8) for a housekeeping (3) request(1)
    emulator.newRXMessage([1, 5, 8, 3, 1])
    
    print("sent")
    time.sleep(120)
    

    emulator.close()
    
    
    