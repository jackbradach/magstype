from kivy.clock import Clock
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import RenderContext
from kivy.properties import StringProperty
from kivy.core.window import Window

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


class WordWidget(Label):

    def __init__(self, **kwargs):
        super(LetterWidget, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

        # call the constructor of parent
        # if they are any graphics object, they will be added on our new canvas

        # We'll update our glsl variables in a clock
        Clock.schedule_interval(self._tick, 1 / 60.)

    def _tick(self, dt):
        if self.font_size > 0:
            self.font_size -= 1

    def _keyboard_closed(self):
        print("Keyboard closed?!")
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if text:
            self.text = text.upper()
        self.font_size = 512
        return True

cLetterlass WordGameApp(App):
    def build(self):
        return WordWidget()

def main():
    WordGameApp().run()

if __name__ == '__main__':
    main()