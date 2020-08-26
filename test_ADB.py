# ADB-specific test cases
import pytest
import sys

from PQ9TestHelpers import getAddress
import PQ9Client


def test_ADB(pq9_connection, destination):
    print("ADB specific tests")
