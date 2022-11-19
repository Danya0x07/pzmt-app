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
    if not frequency.isnumeric():
        return False
    return 0 <= int(frequency) <= 20000


def parse_duration(duration):
    if not duration.isnumeric():
        return False
    return 0 <= int(duration) <= 20000


def note_to_frequency(note):

    if re.search(r'\d+', note) is not None:
        return False
    note = note.upper()
    if note in NOTES:
        return NOTES[note]





