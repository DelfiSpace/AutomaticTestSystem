import queue

class PQ9Emulator:
    '''
    Template of emulators. 
    To use an emulator, try XXXEmulator.processCommand(), which is like PQ9Client.processCommand()
    '''

    def __init__(self, addr):
        '''Input: address number (string) of the emulator on PQ9 bus'''

        self.services = {'17':self.PingService, '3':self.HouseKeepingService} #TODO
        self.addr = addr

    def processCommand(self, cmd):
        '''
        Call a service to process the command. 
        This function will be rewritten in the emulator for OBC.

        Input: 
            cmd	the dictationary of the command. It has to use 'SendRaw'
        Output: 
            state	it can be True/False/'pause'
            reply	the dictationary of the reply
        '''

        # Extract information from the command
        rawMsg, cmdSrc, cmdDest, serviceNum, cmdPayload = self.FrameToData(cmd)

        # Verification
        assert cmdDest == self.addr, "processCommand(): This command is not for %s, but for %s!" % (self.addr, cmdDest)
        assert serviceNum in self.services, "processCommand(): I don't have service %s" % serviceNum

        # Process the command
        state, replyPayload = self.services[serviceNum](cmdPayload)

        # Set the reply
        reply = self.DataToFrame(self.addr, cmdSrc, replyPayload)

        return state, reply

    def FrameToData(self, cmd):
        '''
        Extract information from the command

        Input: 
            cmd		the dictationary of the command. It has to use 'SendRaw'
        Output:
            rawMsg		list of each bit in the raw command
            payload		list of each bit in the payload of the command
            src, dest,serviceNum	information in the command
        '''

        # TODO: fix the server so there are no 2 similar keys
        if '_raw_' in cmd:
            rawMsg = cmd['_raw_'].split()
            src = rawMsg[0]
            dest = rawMsg[2]
            serviceNum = rawMsg[3]
            payload = rawMsg[3:]
        elif 'data' in cmd:
            rawMsg = cmd['data'].split()
            src = cmd['src']
            dest = cmd['dest']
            serviceNum = rawMsg[0]
            payload = rawMsg
        else:
            assert False, "FrameToData(): 'SendRaw' rather than %s should be used" % cmd['_send_']
        return rawMsg, src, dest, serviceNum, payload

    def DataToFrame(self, src, dest, payload):
        '''
        Integrate a PQ9Frame according to the information

        Input:
            payload		list of each bit in the payload of the frame
            src, dest,serviceNum	information in the frame
        Output: 
            reply		the dictationary of the frame. It uses 'SendRaw'
        '''

        # TODO: fix the server so there are no 2 similar keys
        reply = {}
        reply['_send_'] = "SendRaw"
        reply['dest'] = dest
        reply['src'] = src
        reply['data'] = ' '.join(payload)
        reply['_raw_'] = ' '.join([src, str(len(payload)+3), dest] + payload)
        return reply

    def PingService(self, cmdPayload):
        return True, ['17', '2']

    def HouseKeepingService(self, cmdPayload): # TODO
        return True, ['3', '2', '0']


class COMMSEmulator(PQ9Emulator):

    def __init__(self, addr):
        PQ9Emulator.__init__(self, addr)
        self.services['20'] = self.RadioService
        self.RXBuffer = queue.Queue()
        self.TXBuffer = queue.Queue()

    def RadioService(self, cmdPayload): 
        '''
        If master sends a frame to COMMS, this service saves the dictationary of the frame in TXBuffer 
        and returns 'pause' so the PQ9VirtualBus stops. Then users can check status of COMMS.
        If master takes a frame frome COMMS, this service takes the dictationary of the frame from RXBuffer.
        TODO: to be expanded

        Input:
            cmdPayload		list of each bit in the payload of the command
        Output: 
            state		True/False/'pause'
            replyPayload	list of each bit in the payload of the frame
        '''

        if cmdPayload[1] == '9': # OBC sends a frame
            TXFrame = self.DataToFrame(cmdPayload[2], cmdPayload[4], cmdPayload[5:])
            self.TXBuffer.put(TXFrame)
            return 'pause', ['20', '0'] # palse the virtual bus
        elif cmdPayload[1] == '4': # OBC takes a frame
            if self.RXBuffer.empty():
                return True, ['20', '0']
            else:
                RXFrame = self.RXBuffer.get()
                rawMsg, src, dest, serviceNum, payload = self.FrameToData(RXFrame)
                replyPayload = ['20', '0']
                replyPayload.extend(rawMsg)
                return True, replyPayload
