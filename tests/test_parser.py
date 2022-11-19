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
        self.assertFalse(p.parse_frequency('20DE0'))
        self.assertFalse(p.parse_frequency('-200'))
        self.assertFalse(p.parse_frequency('30000'))
        self.assertFalse(p.parse_frequency('ewre'))
        self.assertTrue(p.parse_frequency('0'))
        self.assertTrue(p.parse_frequency('1000'))


    def test_parse_duration(self):
        self.assertFalse(p.parse_duration('20DE0'))
        self.assertFalse(p.parse_duration('-200'))
        self.assertFalse(p.parse_duration('30000'))
        self.assertFalse(p.parse_duration('ewre'))
        self.assertTrue(p.parse_duration('0'))
        self.assertTrue(p.parse_duration('1000'))


    def test_note_to_frequency(self):
        self.assertFalse(p.note_to_frequency('100'))
        self.assertFalse(p.note_to_frequency('3D'))
        self.assertFalse(p.note_to_frequency('j#'))
        self.assertTrue(p.note_to_frequency("f#"))
        self.assertTrue(p.note_to_frequency('D'))









if __name__ == '__main__':
    unittest.main()
