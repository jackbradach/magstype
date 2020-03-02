from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find

# from .sprites import CatSprite

import pyttsx3
import random
import glob
from time import sleep
# TODO: add text to speech?  Color text?

class GameWidget(Widget):
    letter_widget = ObjectProperty()
    print(letter_widget)

    def __init__(self, **kwargs):
        super(GameWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down, on_key_up=self._on_keyboard_up)
        self.scale_rate = -1
        Clock.schedule_interval(self._tick, 1 / 60.)
    
    def _tick(self, dt):
        self.letter_widget.tick(dt)

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        self.letter_widget.keyboard_down_cb(keyboard, keycode, text, modifiers)
        return True
    
    def _on_keyboard_up(self, keyboard, keycode):
        return True

    def _keyboard_closed(self):
        print("Keyboard closed?!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    

class LetterWidget(Label):

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"
    punctuation = ",./;'[]\-="

    def __init__(self, **kwargs):
        super(LetterWidget, self).__init__(**kwargs)
        self._tts = pyttsx3.init()
        self._tts.startLoop(False)
        self._bos = BucketOSounds(
            [
                "Fanfares/sfx_sounds_fanfare1.wav",
                "Fanfares/sfx_sounds_fanfare2.wav",
                "Fanfares/sfx_sounds_fanfare3.wav"
            ]
        )
        self.scale_rate = -1

    def next_letter(self):
        l = random.choice(self.letters)
        self.scale_rate = -1
        self.text = l
        self.font_size = self.height / 2
        self._tts.say(self.text)

    def tick(self, dt):
        if self.font_size == 0:
            self.next_letter()
        elif self.font_size >= 10 * self.height:
            self.next_letter()
        else:
            self.font_size += self.scale_rate
        self._tts.iterate()

    def _keyboard_closed(self):
        print("Keyboard closed?!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def keyboard_down_cb(self, keyboard, keycode, text, modifiers):
        if text and text.upper() == self.text:
            self._bos.play()
            sleep(1)
            self.next_letter()
        return True

class GameApp(App):
    def build(self):
        return GameWidget()

from typing import List

class BucketOSounds():
    """Container where you put a bunch of sounds in and it
    kicks back one at random on demand, optionally with
    a distortion applied.  This makes it easy to add some
    variety whithin categories of sounds.  It sounds hokey
    if, eg, every punch or sword hit in a game is 100%
    identical."""
    def __init__(self, res_names: List[str]=[]):
        self._sounds = []
        print(f"rn: {res_names}")
        for res_name in res_names:
            self.add(res_name)

    def add(self, res_name:str):
        res = resource_find(res_name)
        if res is None:
            raise RuntimeError(f"Couldn't find resource {res_name}")
        sound = SoundLoader.load(res)
        if sound is None:
            raise RuntimeError(f"Failed at loading sound '{res_name}'!")

        
        print(f"Added '{res_name}' ({sound.length} seconds) to bucket-o-sounds")
        self._sounds.append(sound)

    def play(self):
        sound = random.choice(self._sounds)
        sound.play()


def main():
    GameApp().run()

if __name__ == '__main__':
    main()