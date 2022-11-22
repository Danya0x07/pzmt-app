from enum import IntEnum


class CommandType(IntEnum):
    STOP_PLAYING = 0
    PLAY_FINITE_TONE = 1
    PLAY_INFINITE_TONE = 2
    SET_VOLUME = 3


class ReplyCode(IntEnum):
    WRONG_CMD = 0
    OK = 1
    READY = 2
    BUSY = 3
    UNRECOGNIZABLE = -1


class VolumeLevel(IntEnum):
    HIGH = 1
    LOW = 0


def build_command(cmdtype, arg):
    if CommandType.STOP_PLAYING == cmdtype:
        if arg == None:
            return True, '0\n'
        elif arg[0] == 0 and (0 < arg[1] <= 20000):
            return True, str(arg[0]) + ',' + str(arg[1]) + '\n'
        else:
            return False, '0\n'
    if CommandType.PLAY_FINITE_TONE == cmdtype:
        if 0 < (arg[0] and arg[1]) <= 20000:
            return True, str(arg[0]) + ',' + str(arg[1]) + '\n'
        else:
            return False, '0\n'
    if CommandType.PLAY_INFINITE_TONE == cmdtype:
        if(0 < arg[0] <= 20000) and arg[1] == 0:
            return True, str(arg[0]) + ',' + str(arg[1]) + '\n'
        else:
            return False, '0\n'
    if CommandType.SET_VOLUME == cmdtype:
        if VolumeLevel.HIGH == arg:
            return 'V\n'
        if VolumeLevel.LOW == arg:
            return 'v\n'


def parse_reply(reply):
    reply = reply[:-1]
    if reply.isnumeric() and (0 <= int(reply) <= 3):
        return int(reply)
    else:
        return ReplyCode.UNRECOGNIZABLE
