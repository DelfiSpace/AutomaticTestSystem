# EPS-specific test cases
import pytest
import sys

sys.path.insert(1, '../Generic')

from PQ9TestHelpers import getAddress
import PQ9Client

        
def test_EPS():
    print("EPS specific tests")