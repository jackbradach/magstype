from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.properties import StringProperty
from kivy.core.window import Window

import pyttsx3
import random

# TODO: add text to speech?  Color text?

class LetterWidget(Label):

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numbers = "1234567890"
    punctuation = ",./;'[]\-="

    def __init__(self, **kwargs):
        super(LetterWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._tts = pyttsx3.init()
        self._tts.startLoop(False)
        self.scale_rate = -1
        Clock.schedule_interval(self._tick, 1 / 60.)

    def next_letter(self):
        l = random.choice(self.letters)
        self.scale_rate = -1
        self.text = l
        self.font_size = self.height / 2
        self._tts.say(self.text)

    def _tick(self, dt):
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
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text.upper() == self.text:
            rate = self._tts.getProperty('rate')
            self._tts.setProperty('rate', rate + 25)
            for i in range(0, 3):
                self._tts.say(self.text + "!")
            self.scale_rate = 100
            self._tts.setProperty('rate', rate)
            self.font_color = 'green'
        return True
    
    # def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
    #     # if text and text.isalpha():
    #         # self.text = text.upper()
    #     # self._tts.say(self .text)
    #     # self._tts.runAndWait()
    #         # self.font_size = self.height / 2
    #     return True

class GameApp(App):
    def build(self):
        return LetterWidget()

def main():
    GameApp().run()

if __name__ == '__main__':
    main()