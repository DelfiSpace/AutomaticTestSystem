global suite 

suite = { 
'OBC': ['test_OBC.py', 'test_PingService.py', 'test_ResetService.py', 'test_SoftwareUpdateService.py'],
'EPS': ['test_EPS.py', 'test_PingService.py', 'test_ResetService.py', 'test_SoftwareUpdateService.py'],
'ADB': ['test_ADB.py', 'test_PingService.py', 'test_ResetService.py', 'test_SoftwareUpdateService.py'],
'ADCS': ['test_ADCS.py', 'test_PingService.py', 'test_ResetService.py', 'test_SoftwareUpdateService.py'], 
'COMMS': ['test_COMMS.py', 'test_PingService.py', 'test_ResetService.py', 'test_SoftwareUpdateService.py']
}
    
def isTest(system, test):
    global suite

    # string in the list
    if test in suite[system]:
        return False
    else:
        return True