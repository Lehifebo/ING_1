import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.email_generator import EmailGenerator

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), 'dummy.txt')

class TestEmailGenerator(unittest.TestCase):
    def setUp(self):
        self.email_generator = EmailGenerator(TEMPLATE_PATH, [])

    def test_read_template(self):
        # Test that the method returns the correct content of the template file
        template_content = self.email_generator.read_template(TEMPLATE_PATH)
        expected_content = '{0},\n\nSales\n{1}\nExpenses\n{2}'
        self.assertEqual(template_content, expected_content)


if __name__ == '__main__':
    unittest.main()
