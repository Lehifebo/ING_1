import unittest
from unittest.mock import mock_open, patch
import os
from pipeline_module.data.team import Team
from pipeline_module.output_generation.string_generator import StringGenerator
import pandas as pd


class TestStringGenerator(unittest.TestCase):

    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
