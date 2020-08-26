import asyncio
import json

class PQ9Client:

    def __init__(self, serverIP, serverPort, time):
        super().__init__()
        self.TIMEOUT = time
        self.TCP_IP = serverIP
        self.TCP_PORT = serverPort
        self.pq9reader = 0
        self.pq9writer = 0
        self.loop = 0

    def close(self):
        self.loop.run_until_complete(self.AwaitedClose())

    async def AwaitedClose(self):
        #self.pq9reader.close()
        self.pq9writer.close()
        await self.pq9writer.wait_closed()
    
    def connect(self):
        #try:
            self.loop = asyncio.new_event_loop()
            self.loop.run_until_complete(self.AwaitedConnect())
        #except ConnectionRefusedError:
            #print('timeout error')

    async def AwaitedConnect(self):
        self.pq9reader, self.pq9writer = await asyncio.open_connection(self.TCP_IP, self.TCP_PORT, loop=self.loop)
        print("PQ9Socket: Connected to "+str(self.TCP_IP)+":"+str(self.TCP_PORT))

    def sendFrame(self, inputFrame):
        self.loop.run_until_complete(self.AwaitedSendFrame(inputFrame))

    async def AwaitedSendFrame(self,inputFrame):
        cmdString = json.dumps(inputFrame) + '\n'
        #print("Sending: "+cmdString, end="")
        self.pq9writer.write(cmdString.encode())
        await self.pq9writer.drain()

    def getFrame(self):
        status, msg = self.loop.run_until_complete(self.AwaitedGetFrame())
        if(status == True):
            # return status, json.loads(msg)["_raw_"]
            return status, json.loads(msg)
        else:
            return status, []

    async def AwaitedGetFrame(self):
        try:
            rxMsg = await asyncio.wait_for(self.pq9reader.readline(), timeout=self.TIMEOUT)
            return True, rxMsg
        except asyncio.TimeoutError:
            #print("PQ9EGSE Reply Timeout!")
            return False, []

    def processCommand(self, command):
        self.sendFrame(command)
        succes, msg = self.getFrame()
        return succes, msg
