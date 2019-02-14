
from abc import ABC, abstractmethod


class Note(ABC):

    def __init__(self, pitch, duration):
        super().__init__()
        self.pitch = pitch
        self.duration = duration

    # @abstractmethod
    # def do_something(self):
    #     pass


class MidiNote(Note):

    pitch: int

    duration: int

    velocity: int

    def __init__(self, pitch, duration_ticks, velocity):
        super().__init__(pitch, duration_ticks)
        self.pitch = pitch
        self.duration = duration_ticks
        self.velocity = velocity
