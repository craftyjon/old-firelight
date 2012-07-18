import kivy
kivy.require('1.3.0')

from kivy.uix.floatlayout import FloatLayout
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty


class FireControl(FloatLayout):
    '''Create a controller that receives a custom widget from the kv lang file.

    Add an action to be called from the kv lang file.
    '''
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'


class FireControlApp(App):

    def build(self):
        return FireControl(info='Hello world')

if __name__ in ('__android__', '__main__'):
    FireControlApp().run()
