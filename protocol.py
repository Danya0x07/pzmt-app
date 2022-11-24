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


def build_command(cmdtype, arg=None):
    if cmdtype == CommandType.STOP_PLAYING and arg is None:
        return True, '0\n'

    if cmdtype == CommandType.PLAY_FINITE_TONE and type(arg) == tuple\
            and len(arg) == 2 and type(arg[0]) == int and type(arg[1]) == int:
        return True, '{},{}\n'.format(arg[0], arg[1])

    if cmdtype == CommandType.PLAY_INFINITE_TONE and type(arg) == int:
        return True, str(arg) + '\n'

    if cmdtype == CommandType.SET_VOLUME and type(arg) == VolumeLevel:
        if arg == VolumeLevel.HIGH:
            return True, 'V\n'
        if arg == VolumeLevel.LOW:
            return True, 'v\n'

    return False, '0\n'


def parse_reply(reply):
    if len(reply) < 2 and reply[-1] != '\n':
        return ReplyCode.UNRECOGNIZABLE

    reply = reply[:-1]
    try:
        reply = int(reply)
        reply_code = ReplyCode(reply)
    except ValueError:
        return ReplyCode.UNRECOGNIZABLE
    else:
        return reply_code
