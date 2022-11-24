import unittest

import parser as p


class MyTestCase(unittest.TestCase):
    def test_valid_frequency(self):
        self.assertFalse(p.valid_frequency(-100))
        self.assertFalse(p.valid_frequency(30100))
        self.assertTrue(p.valid_frequency(0))
        self.assertTrue(p.valid_frequency(5000))
    def test_valid_duration(self):
        self.assertFalse(p.valid_duration(-100))
        self.assertFalse(p.valid_duration(20001))
        self.assertTrue(p.valid_duration(0))
        self.assertTrue(p.valid_duration(1000))

    def test_valid_interval(self):
        self.assertFalse(p.valid_interval(0))
        self.assertFalse(p.valid_interval(2000))
        self.assertTrue(p.valid_interval(1))
        self.assertTrue(p.valid_interval(16))

    def test_valid_note(self):
        self.assertFalse(p.valid_note('qqqq'))
        self.assertFalse(p.valid_note('9B'))
        self.assertFalse(p.valid_note('0G#'))
        self.assertFalse(p.valid_note('6E#'))
        self.assertFalse(p.valid_note('5DZ'))
        for i in range(3, 8):
            for note in p.NOTES.keys():
                self.assertTrue(p.valid_note(str(i) + note))

    def test_split_sequence(self):
        self.assertEqual(p.split_sequence('200'), ['200'])
        self.assertEqual(p.split_sequence('  200 30043 43542 '), ['200', '30043', '43542'])
        self.assertEqual(p.split_sequence('200\n340\n2\n'), ['200', '340', '2'])
        self.assertEqual(p.split_sequence('\n \n\n  200\n23\n\n 434  \n\n578\n 4342  4324\n \n\n  '),
                         ['200', '23', '434', '578', '4342', '4324'])

    def test_parse_frequency(self):
        success, result = p.parse_frequency('20DE0')
        self.assertFalse(success)
        self.assertEqual(result, 0)

        success, result = p.parse_frequency('ewre')
        self.assertFalse(success)
        self.assertEqual(result, 0)

        success, result = p.parse_frequency('0')
        self.assertTrue(success)
        self.assertEqual(result, 0)

        success, result = p.parse_frequency('1000')
        self.assertTrue(success)
        self.assertEqual(result, 1000)

        success, result = p.parse_frequency('30000')
        self.assertTrue(success)
        self.assertEqual(result, 30000)

        success, result = p.parse_frequency('-200')
        self.assertTrue(success)
        self.assertEqual(result, -200)


    def test_parse_duration(self):
        success, result = p.parse_duration('20DE0')
        self.assertFalse(success)
        self.assertEqual(result, 0)

        success, result = p.parse_duration('ewre')
        self.assertFalse(success)
        self.assertEqual(result, 0)

        success, result = p.parse_duration('0')
        self.assertTrue(success)
        self.assertEqual(result, 0)

        success, result = p.parse_duration('1000')
        self.assertTrue(success)
        self.assertEqual(result, 1000)

        success, result = p.parse_duration('30000')
        self.assertTrue(success)
        self.assertEqual(result, 30000)

        success, result = p.parse_duration('-200')
        self.assertTrue(success)
        self.assertEqual(result, -200)

    def test_note_to_frequency(self):
        for i in range(3, 8):
            for note in p.NOTES.keys():
                self.assertEqual(p.note_to_frequency(str(i) + note), p.NOTES[note] * 2**(i - 3))


if __name__ == '__main__':
    unittest.main()
