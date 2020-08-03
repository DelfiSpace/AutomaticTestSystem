# AutomaticTestSystem

This repository contains the automatic test scripts used for the different subsystems of Delfi-PQ.

## Installation

These scripts are based upon pyTest, pyTest TestConfig and pyTest-HTML. Before you can execute these tests, you need to install them by typing:

`pip install pytest pytest-html pytest-config`

## Configuration

To execute the test scripts, you need to first configure the EGSE url, port and the timeout. To do this, please copy and rename _TestConfig.ini.example_ to _TestConfig.ini_ and edit the system-specific settings. **Do not commit** the renamed file to the repository as it contains system-specific settings.

When running the test locally, a timeout of 0.5s is reasonable but when running it via a remote connection, increase the timeout to few seconds (2-5) depending on the network performances. 

## Execution

You can run a system test (EPS in this example) by typing:

`pytest --subsystem=EPS` 

This command will run all tests associated to the EPS. You can also:

`pytest --destination=EPS test_PingService.py`

this will run the test_PingService.py test script on the destination sus-system.


