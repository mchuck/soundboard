import pygame
from typing import ClassVar, List
from dataclasses import dataclass, field


@dataclass
class SoundData:
    path_key: ClassVar = 'path'
    volume_key: ClassVar = 'volume'
    looping_key: ClassVar = 'loop'
    catalog_key: ClassVar = 'catalog'

    path: str
    volume: str
    looping: str
    catalog: str = None

    def to_dict(self):
        return {
            self.path_key: self.path,
            self.volume_key: self.volume,
            self.looping_key: self.looping,
            self.catalog_key: self.catalog
        }

    @staticmethod
    def from_dict(value):
        path = value[SoundData.path_key]
        volume = value[SoundData.volume_key]
        looping = value[SoundData.looping_key]
        catalog = value[SoundData.catalog_key]
        return SoundData(path, volume, looping, catalog)

class Sound(object):
   
    def __init__(self, id, mixer, sound_data: SoundData):
        self.id = id
        self.mixer = mixer
        self.sound_data = sound_data
        self.sound = None
        self.current_channel = None
        self.is_paused = False

    def play(self):
        if not self.sound:
            self.sound = pygame.mixer.Sound(self.sound_data.path)
        if not self.__is_assigned():
            self.current_channel = self.mixer.find_channel()
            self.current_channel.set_volume(self.sound_data.volume / 100)

        if not self.is_paused:
            loops_arg = -1 if self.sound_data.looping else 0
            self.current_channel.play(self.sound, loops=loops_arg)
        else:
            self.current_channel.unpause()
            self.is_paused = False

    def is_playing(self):
        return bool(self.__is_assigned() and self.current_channel.get_busy() and not self.is_paused)

    def __is_assigned(self):
        return bool(self.current_channel)
        
    def pause(self):
        if self.is_playing():
            self.current_channel.pause()
            self.is_paused = True

    def stop(self):
        if self.__is_assigned():
            self.current_channel.stop()
            self.current_channel = None

    def set_volume(self, new_volume):
        self.sound_data.volume = new_volume
        if self.__is_assigned():
            self.current_channel.set_volume(new_volume / 100)




