# play 1
# pause 1
# stop 1
# exit


from dataclasses import dataclass

from parsy import seq, string, string_from, regex

@dataclass
class Number:
    value: int

@dataclass
class PlayCommand:
    song_id: Number

@dataclass
class PauseCommand:
    song_id: Number

@dataclass
class StopCommand:
    song_id: Number

@dataclass
class ExitCommand:
    pass

@dataclass
class SaveCommand:
    pass

@dataclass
class VolumeCommand:
    song_id: Number
    value: Number

number_literal = regex(r'-?[0-9]+').map(int).map(Number).desc('number')
space = regex(r'\s+') 


play = string_from('play', 'pl', 'p')
play_command = seq(
    _play = play + space,
    song_id = number_literal
).combine_dict(PlayCommand)

pause = string_from('pause', 'pa')
pause_command = seq(
    _pause = pause + space,
    song_id = number_literal
).combine_dict(PauseCommand)

stop = string_from('stop', 'st', 's')
stop_command = seq(
    _stop = stop + space,
    song_id = number_literal
).combine_dict(StopCommand)

volume = string_from('volume', 'vol', 'v')
volume_command = seq(
    _volume = volume + space,
    song_id = number_literal,
    value = space >> number_literal
).combine_dict(VolumeCommand)

exit_command = string_from('exit', 'e').map(lambda x: ExitCommand())
save_command = string('save').map(lambda x: SaveCommand())

def get_parser():
    command_parser = play_command | pause_command | stop_command | exit_command | volume_command | save_command
    return command_parser

if __name__ == "__main__":
    import sys
    print(get_parser().parse(sys.argv[1]))
