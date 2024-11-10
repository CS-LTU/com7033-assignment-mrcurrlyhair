import unittest
from app import hashing_pass



class TestHashingPass(unittest.TestCase):

# Testing if the same password hashed is equal to one another  
    def test_hashing_pass_consistency(self):
        input_text = "Test_password"
        hash1 = hashing_pass(input_text)
        hash2 = hashing_pass(input_text)
        self.assertEqual(hash1, hash2, "Hash does not match.")


# Testing if different passwords have different hashes
    def test_hashing_pass_diff_input(self):
        input_text1 = "test_password"
        input_text2 = "password_test"
        hash1 = hashing_pass(input_text1)
        hash2 = hashing_pass(input_text2)
        self.assertNotEqual(hash1, hash2, "Different inputs , should be different hashes")


# Testing length of the hash, SHA256 should equal 64 characters
    def test_hashing_pass_length(self):
        input_text = "test_password"
        hashed_output = hashing_pass(input_text)
        self.assertEqual(len(hashed_output), 64, "Hash length is incorrect.")

if __name__ == '__main__':
    unittest.main()
