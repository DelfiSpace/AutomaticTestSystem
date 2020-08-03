# OBC-specific test cases
import pytest
import sys

from PQ9TestHelpers import getAddress
import PQ9Client


def test_OBC(pq9_connection, destination):
    print("OBC specific tests")
