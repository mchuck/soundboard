
from sound import Sound, SoundData
import pygame
import time
import json
import sys
from tabulate import tabulate
from os.path import basename
from colorama import init, Fore, Style


from commands import PlayCommand, PauseCommand, StopCommand, ExitCommand, VolumeCommand, get_parser

def run(filename):


    songs = load_file(filename)
    
    pygame.mixer.pre_init()
    pygame.mixer.init()

    sounds = [Sound(i+1, pygame.mixer, sd) for i, sd in enumerate(songs)]

    command_parser = get_parser()
    
    while True:
        print_table(sounds)
        print('Please state the command:', end=' ')

        
        command = input()
        if command == 's':
            dump_file(sounds, filename)
            print('file saved')
            break

        try:
            command_result = command_parser.parse(command)

            #TODO pattern match this in python 3.10
            if isinstance(command_result, PlayCommand):
                sound = find_sound(sounds, command_result.song_id.value)
                sound.play()
            elif isinstance(command_result, PauseCommand):
                sound = find_sound(sounds, command_result.song_id.value)
                sound.pause()
            elif isinstance(command_result, StopCommand):
                sound = find_sound(sounds, command_result.song_id.value)
                sound.stop()
            elif isinstance(command_result, VolumeCommand):
                sound = find_sound(sounds, command_result.song_id.value)
                sound.set_volume(command_result.value.value)
            elif isinstance(command_result, ExitCommand):
                break

        except Exception as ex:
            print(str(ex))


def find_sound(sounds, sound_id):
    sound = [x for x in sounds if x.id == sound_id]
    if not sound:
        raise ValueError(f"Cannot find sound with id '{sound_id}'")
    return sound[0]

def get_sound_display_data(sound):
    def colored_value(color, value):
        return color + Style.BRIGHT + str(value) + Style.RESET_ALL
    
    return [
        colored_value(Fore.YELLOW, sound.id),
        colored_value(Fore.GREEN, 'yes') if sound.is_playing() else \
            colored_value(Fore.MAGENTA, 'paused') if sound.is_paused else colored_value(Fore.RED, 'no'),
        colored_value(Fore.CYAN, basename(sound.sound_data.path)),
        colored_value(Fore.YELLOW, sound.sound_data.volume),
        colored_value(Fore.GREEN, 'yes') if sound.sound_data.looping else colored_value(Fore.RED, 'no')
    ]

def print_table(sounds):
    headers = ['Id', 'Is playing', 'File', 'Volume', 'Loop']
    data = [headers] + [get_sound_display_data(s) for s in sounds]
    print(tabulate(data, headers='firstrow', tablefmt='presto'))
            
def load_file(filename):
    with open(filename, 'r') as in_f:
        json_data = json.load(in_f)
        data = [SoundData.from_dict(d) for d in json_data]
        return data
            
def dump_file(songs, filename):
    data = [s.sound_data.to_dict() for s in songs]
    with open(filename, 'w') as out_f:
        json.dump(data, out_f)

if __name__ == "__main__":
    init() # initialize colorama
    run(sys.argv[1])
