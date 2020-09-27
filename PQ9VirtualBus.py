import PQ9Client
import PQ9Emulators
import queue

class PQ9VirtualBus():
    '''
    If you want to use multiple emulators, or want to mix real hardware and virtual emulators,
    use VirtualBus. VirtualBus.processCommand() is like PQ9Client.processCommand()
    '''

    def __init__(self, master, commEmulator, emulatorDict):
        '''
        Input:
            master		PQ9Client (if a real OBC is used) / OBCEmulator
            commsEmulator	
            emulatorDict	a dict of all emulators {'addr1': emulator 1, 'addr 2': emulator2, ...}
        '''

        self.master = master
        self.comm = commEmulator
        self.emuDict = emulatorDict
        self.fo = open('VirtualBusLog.pq9', 'w')
        self.postProcessFrame = {}

    def processCommand(self, cmd):
        '''
        Put a command in the RX buffer of commEmulator, and then run the scheduler.
        If the scheduler is paused, take a command from the TX buffer of commEmulator and return.
        It can only process a SINGLE command at this stage, but can be expanded

        Input:
            master		PQ9Client (if a real OBC is used) / OBCEmulator
            commsEmulator	
            emulatorDict	a dict of all emulators {'addr1': emulator 1, 'addr 2': emulator2, ...}
        '''

        self.comm.RXBuffer.put(cmd)
        self.scheduler()
        return True, self.comm.TXBuffer.get()

    def scheduler(self):
       '''
        Take a frame from the master. If needed, transfer the frame to a hardware module / emulator
        and send the reply to the master. scheduler() also logs every frames on the bus and may insert faults

        If an emulator returns 'pause' as its state, scheduler() will return and gives control to user's code. 
        In this case, scheduler() will not send the reply until restart, so it can capture as many frames on the bus as possible.
      '''

        if self.postProcessFrame != {}:
            self.master.sendFrame(postProcessFrame)
            self.postProessFrame = {}

        while True:
            cmd = self.master.getFrame()
            self.fo.write(cmd)
            if type(master) == PQ9Client: # There is a real OBC
                if cmd['dest'] in emuDict:
                    state, reply = self.emuDict[cmd['dest']].processCommand(cmd)
                else:
                    continue
            elif type(master) == PQ9Emulator: # There is a virtual OBC
                if cmd['dest'] in emuDict:
                    state, reply = self.emuDict[cmd['dest']].processCommand(cmd)
                else:
                    state, reply = self.master.processCommand(cmd)

            if state == 'pause':
                self.postProessFrame = reply
                return
            else:
                self.master.sendFrame(reply)