import unittest

import parser as p


class MyTestCase(unittest.TestCase):
    def test_valid_frequency(self):
        self.assertFalse(p.valid_frequency(-100))
        self.assertFalse(p.valid_frequency(30100))
        self.assertTrue(p.valid_frequency(0))
        self.assertTrue(p.valid_frequency(5000))

if __name__ == '__main__':
    unittest.main()
