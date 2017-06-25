from glob import glob

from kivy.app import App
import kivy.core.gl
from kivy.atlas import Atlas

from engine.text import TextStorage
from engine.audio import AudioStorage
from engine.scripts import ScriptLoader
from engine.images import ImageStorage

from levels import *

TextStorage(locale='en-us').bulk_load(glob('./assets/text/*.yaml'))
AudioStorage(locale='en-us').bulk_load(glob('./assets/audio/*.yaml'))
ImageStorage(locale='en-us').bulk_load(glob('./assets/images/*.yaml'))
ScriptLoader().bulk_load(glob('./levels/scripts/*.kv'))


class SlaveTamerApp(App):
    def __init__(self):
        self.text = TextStorage(locale='en-us')
        self.img = ImageStorage(locale='en-us')
        self.audio = AudioStorage(locale='en-us')

        super().__init__()

    def build(self):
        return main_menu.MainMenuScreen()

    def on_pause(self):
        return True

if __name__ == '__main__':
    SlaveTamerApp().run()

