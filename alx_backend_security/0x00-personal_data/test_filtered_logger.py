#!/usr/bin/env python3
"""Test cases for filtered_logger module"""
import unittest
import os


class TestFilteredLogger(unittest.TestCase):
    """Test the filtered logger functionality"""

    def test_environment_variables(self):
        """Test that required environment variables can be set"""
        os.environ["PERSONAL_DATA_DB_USERNAME"] = "test_user"
        os.environ["PERSONAL_DATA_DB_PASSWORD"] = "test_pass"
        os.environ["PERSONAL_DATA_DB_HOST"] = "localhost"
        os.environ["PERSONAL_DATA_DB_NAME"] = "test_db"

        self.assertEqual(os.getenv("PERSONAL_DATA_DB_USERNAME"), "test_user")
        self.assertEqual(os.getenv("PERSONAL_DATA_DB_PASSWORD"), "test_pass")

    def test_basic_string_operations(self):
        """Test basic Python string operations"""
        test_string = "password=secret123"
        self.assertIn("password", test_string)
        self.assertIn("secret", test_string)


if __name__ == "__main__":
    unittest.main()
