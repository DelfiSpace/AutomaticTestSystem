import asyncio
import json

class PQ9Client:

    def __init__(self, serverIP, serverPort, timeout):
        super().__init__()
        self.TIMEOUT = timeout
        self.TCP_IP = serverIP
        self.TCP_PORT = serverPort
        self.pq9reader = 0
        self.pq9writer = 0
        self.loop = 0
        self.closed = True

    def close(self):
        try:
            self.closed = True
            self.loop.run_until_complete(self.AwaitedClose())
        except RuntimeError:
            pass # ignore exception
        except RuntimeWarning:
            pass # ignore warning

    async def AwaitedClose(self):
        self.pq9writer.close()
        await self.pq9writer.wait_closed()
    
    def connect(self):
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.AwaitedConnect())

    async def AwaitedConnect(self):
        self.pq9reader, self.pq9writer = await asyncio.open_connection(self.TCP_IP, self.TCP_PORT, loop=self.loop)
        self.closed = False

    def sendFrame(self, inputFrame):
        cmdString = json.dumps(inputFrame) + '\n'
        self.pq9writer.write(cmdString.encode())

    def getFrame(self):
        if self.closed:
           raise PQ9ClientConnectionClosed('Connection closed')
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
            return False, []

    def processCommand(self, command):
        self.sendFrame(command)
        succes, msg = self.getFrame()
        return succes, msg

class PQ9ClientConnectionClosed(Exception):
    """Exception raised by PQ9Client.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message=""):
        self.message = message
        super().__init__(self.message)
