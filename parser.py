# Модуль валидации вводимых данных

import re

NOTES = {
    'C': 132,
    'C#': 140,
    'D': 148,
    'D#': 157,
    'E': 166,
    'F': 176,
    'F#': 187,
    'G': 198,
    'G#': 210,
    'A': 222,
    'A#': 235,
    'B': 249
}


def valid_frequency(frequency):
    return 0 <= frequency <= 20000


def valid_duration(duration):
    return 0 <= duration <= 20000


def valid_interval(interval):
    return 1 <= interval <= 1024


def valid_note(note):
    octave = note[0]
    if not octave.isdigit():
        return False
    octave = int(octave)
    if 3 <= octave <= 7 and note[1:] in NOTES:
        return True


def split_sequence(sequence):
    sequence = re.split(r'[\s\n]+', sequence)
    for space in sequence:
        if space == '':
            sequence.remove('')
    return sequence


def parse_frequency(frequency):
    if frequency[0] == '-':
        frequency = frequency[1:]
        if frequency.isnumeric():
            frequency = '-' + str(frequency)
            return True, int(frequency)
    if not frequency.isnumeric():
        return False, 0
    return True, int(frequency)


def parse_duration(duration):
    if duration[0] == '-':
        duration = duration[1:]
        if duration.isnumeric():
            duration = '-' + str(duration)
            return True, int(duration)
    if not duration.isnumeric():
        return False, 0
    return True, int(duration)


def note_to_frequency(note):
    octave = int(note[0])
    note = note[1:].upper()
    if note in NOTES:
        return NOTES[note] * 2**(octave - 3)





