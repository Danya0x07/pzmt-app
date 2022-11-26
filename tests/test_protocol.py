import unittest
import protocol as p
from protocol import VolumeLevel, CommandType, ReplyCode


class MyTestCase(unittest.TestCase):
    def test_build_command(self):

        success, result = p.build_command(CommandType.STOP_PLAYING, (1, 1000))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(CommandType.STOP_PLAYING)
        self.assertTrue(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(CommandType.PLAY_FINITE_TONE)
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(CommandType.PLAY_FINITE_TONE, (0, 500))
        self.assertTrue(success)
        self.assertEqual(result, '0,500\n')

        success, result = p.build_command(CommandType.PLAY_FINITE_TONE, (400, 0))
        self.assertTrue(success)
        self.assertEqual(result, '400,0\n')

        success, result = p.build_command(CommandType.PLAY_FINITE_TONE, (1000, 1000))
        self.assertTrue(success)
        self.assertEqual(result, '1000,1000\n')

        success, result = p.build_command(CommandType.PLAY_INFINITE_TONE, (0, 10))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(CommandType.PLAY_INFINITE_TONE, 600)
        self.assertTrue(success)
        self.assertEqual(result, '600\n')

        success, result = p.build_command(CommandType.SET_VOLUME, (100, 0))
        self.assertFalse(success)
        self.assertEqual(result, '0\n')

        success, result = p.build_command(CommandType.SET_VOLUME, VolumeLevel.LOW)
        self.assertTrue(success)
        self.assertEqual(result, 'v\n')

        success, result = p.build_command(CommandType.SET_VOLUME, VolumeLevel.HIGH)
        self.assertTrue(success)
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
