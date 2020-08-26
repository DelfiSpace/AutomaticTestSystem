# content of conftest.py
import pytest
import sys
import PQ9Client
import os
import PQ9TestSuite
from pytest_testconfig import config as testConfig
    
def pytest_configure(config):
    global destinationAddress
    if (config.getoption("--system") != None):
        destinationAddress = config.getoption("--system")
        config.option.htmlpath = destinationAddress + 'TestReport.html'
    else:
        destinationAddress = config.getoption("--destination")
        config.option.htmlpath = 'TestReport.html'
    
def pytest_ignore_collect(path, config):
    global destinationAddress
    if (config.getoption("--system") != None):
        return PQ9TestSuite.isTest(destinationAddress, os.path.basename(path))
    else:
        return False 

def pytest_addoption(parser):
    parser.addoption(
        "--destination", action="store", help="subsystem address", dest="destination",
    )
    parser.addoption(
        "--system", action="store", help="subsystem", dest="system",
    )
    
@pytest.fixture
def BinaryFiles():
    return testConfig['PQ9EGSE']['BinaryFiles']

@pytest.fixture
def destination(request):
    global destinationAddress
    return destinationAddress

@pytest.fixture(scope="session") #only 'make' this object once per session.
def pq9_connection():
    pq9client = PQ9Client.PQ9Client(
				testConfig['PQ9EGSE']['server'], 
				testConfig['PQ9EGSE']['port'], 
				float(testConfig['PQ9EGSE']['timeout']))
    pq9client.connect()

    yield pq9client
    pq9client.close()
