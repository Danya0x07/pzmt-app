import unittest
import protocol as p



class MyTestCase(unittest.TestCase):
    def test_build_command(self):

        success, result = p.build_command(0, (1, 1000))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(0, (0, -1000))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(0, (1, -1000))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(0, None)
        self.assertTrue(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(0, (0, 1000))
        self.assertTrue(success)
        self.assertEqual(result, '0,1000\n')

        success, result = p.build_command(1, (0, 0))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(1, (0, 10))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(1, (10, 0))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(1, (1000, 1000))
        self.assertTrue(success)
        self.assertEqual(result, '1000,1000\n')

        success, result = p.build_command(2, (0, 10))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(2, (100, 0))
        self.assertTrue(success)
        self.assertEqual(result, '100,0\n')

        result = p.build_command(3, (100, 0))
        self.assertEqual(result, None)

        result = p.build_command(3, 0)
        self.assertEqual(result, 'v\n')

        result = p.build_command(3, 1)
        self.assertEqual(result, 'V\n')

    def test_parse_reply(self):

        result = p.parse_reply('0\n')
        self.assertEqual(result, p.ReplyCode.WRONG_CMD)

        result = p.parse_reply('1\n')
        self.assertEqual(result, p.ReplyCode.OK)

        result = p.parse_reply('2\n')
        self.assertEqual(result, p.ReplyCode.READY)

        result = p.parse_reply('3\n')
        self.assertEqual(result, p.ReplyCode.BUSY)

        result = p.parse_reply('30\n')
        self.assertEqual(result, p.ReplyCode.UNRECOGNIZABLE)

        result = p.parse_reply('f30\n')
        self.assertEqual(result, p.ReplyCode.UNRECOGNIZABLE)


if __name__ == '__main__':
    unittest.main()
