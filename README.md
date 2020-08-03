# AutomaticTestSystem

This repository contains the automatic test scripts used for the different subsystems of Delfi-PQ.

## Installation

These scripts are based upon pyTest, pyTest TestConfig and pyTest-HTML. Before you can execute these tests, you need to install them by typing:
`pip install pytest pytest-html pytest-config`

## Execution

You can run a system test (EPS in this example) by typing:
`pytest --subsystem=EPS` 

This command will run all tests associated to the EPS. You can also:
`pytest --destination=EPS test_PingService.py`
this will run the test_PingService.py test script on the destination sus-system.


