from Mongo_Loader import hashing_pass
import hashlib
import pytest

def test_hashing_pass():
    password = "Churchill!1"
    hashed_password = hashing_pass(password)
    # SHA256 out puts 64 characters , making usre the out put is as expected 
    assert len(hashed_password) == 64

    # Checking hashes are different 
    wrong_pass = "1!Churchill"
    wrong_hashed = hashing_pass(wrong_pass)

    assert password != wrong_hashed




