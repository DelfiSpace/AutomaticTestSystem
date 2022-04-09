# Generic Sub-System Emulator
from PQ9Client import PQ9Client, PQ9ClientConnectionClosed
import time
import configparser
from threading import Thread

class SubSystemEmulator:

    def __init__(self, pq9_connection, source):
        self.pq9Handler = pq9_connection
        self.src = source
        self.running = False
        
    def start(self):
        self.running = True
        self.processThread = Thread(target=self.task, args=())
        self.processThread.start()
    
    def close(self):
        self.running = False
        self.processThread.join()
           
    def task(self):
        try:
            while self.running:
                success, msg = self.pq9Handler.getFrame()
                if success == True:
                    self.checkMessage(msg)
        except PQ9ClientConnectionClosed:
            pass

    def checkMessage(self, msg):
        print(msg)
