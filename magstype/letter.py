from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import RenderContext
from kivy.properties import StringProperty
from kivy.core.window import Window

import pyttsx3

# TODO: add text to speech?  Color text?

shader = '''
$HEADER$
uniform vec2 resolution;
uniform float time;
void main(void)
{
   vec4 frag_coord = frag_modelview_mat * gl_FragCoord;
   float x = frag_coord.x;
   float y = frag_coord.y;
   float mov0 = x+y+cos(sin(time)*2.)*100.+sin(x/100.)*1000.;
   float mov1 = y / resolution.y / 0.2 + time;
   float mov2 = x / resolution.x / 0.2;
   float c1 = abs(sin(mov1+time)/2.+mov2/2.0-mov1-mov2+time);
   float c2 = abs(sin(c1+sin(mov0/1000.+time)
              +sin(y/40.+time)+sin((x+y)/100.)*3.));
   float c3 = abs(sin(c2+cos(mov1+mov2+c2)+cos(mov2)+sin(x/1000.)));
   gl_FragColor = vec4( c1,c2,c3,1.0);
}
'''


class LetterWidget(Label):
    # property to set the source code for fragment shader
    fs = StringProperty(None)

    def __init__(self, **kwargs):
        # self.canvas = RenderContext()
        super(LetterWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._tts = pyttsx3.init()
        self._tts.startLoop(False)
        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas

        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self._tick, 1 / 60.)
        # Clock.schedule_interval(self.update_glsl, 1 / 60.)

    # def on_fs(self, instance, value):
    #     # set the fragment shader to our source code
    #     shader = self.canvas.shader
    #     old_value = shader.fs
    #     shader.fs = value
    #     if not shader.success:
    #         shader.fs = old_value
    #         raise Exception('failed')

    # def update_glsl(self, *largs):
    #     self.canvas['time'] = Clock.get_boottime()
    #     self.canvas['resolution'] = list(map(float, self.size))
    #     # This is needed for the default vertex shader.
    #     win_rc = Window.render_context
    #     self.canvas['projection_mat'] = win_rc['projection_mat']
    #     self.canvas['modelview_mat'] = win_rc['modelview_mat']
    #     self.canvas['frag_modelview_mat'] = win_rc['frag_modelview_mat']


    def _tick(self, dt):
        if self.font_size > 0:
            self.font_size -= 1
        self._tts.iterate()

    def _keyboard_closed(self):
        print("Keyboard closed?!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text and  (text.isalpha() or text.isnumeric()):
            self.text = text.upper()
            self._tts.stop()
            self._tts.say(self.text)
            # self._tts.runAndWait()
            self.font_size = self.height / 2
        return True
    
    # def _on_keyboard_up(self, keyboard, keycode, text, modifiers):
    #     # if text and text.isalpha():
    #         # self.text = text.upper()
    #     # self._tts.say(self .text)
    #     # self._tts.runAndWait()
    #         # self.font_size = self.height / 2
    #     return True

class LetterApp(App):
    def build(self):
        return LetterWidget()

def main():
    LetterApp().run()

if __name__ == '__main__':
    main()