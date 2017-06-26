from glob import glob

from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
import kivy.core.gl

from kivy.core.window import Window


from engine.text import TextStorage
from engine.audio import AudioStorage
from engine.scripts import ScriptLoader
from engine.images import ImageStorage
from engine.config import ConfigManager

from levels import *


conf = ConfigManager('slavetamer').bulk_load(glob('./levels/config/*.yaml'))

TextStorage(locale=conf.app__locale).bulk_load(glob('./assets/text/*.yaml'))
AudioStorage(locale=conf.app__locale).bulk_load(glob('./assets/audio/*.yaml'))
ImageStorage(locale=conf.app__locale).bulk_load(glob('./assets/images/*.yaml'))
ScriptLoader().bulk_load(glob('./levels/scripts/*.kv'))


class SlaveTamerApp(App):
    def __init__(self):
        self.conf = ConfigManager()
        super().__init__()

        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False

        self.text = TextStorage(locale=self.conf.app__locale)
        self.img = ImageStorage(locale=self.conf.app__locale)
        self.audio = AudioStorage(locale=self.conf.app__locale)

    def get_application_config(self, *args):
        return super().get_application_config(self.conf.get_main_path())

    def build(self):
        if self.conf.graphics__fullscreen == '1':
            Window.fullscreen = 'auto'
        else:
            Window.fullscreen = False

        return main_menu.MainMenuScreen()

    def build_config(self, config):
        # build default configuration
        return self.conf.build_config(config)

    def build_settings(self, settings):
        # build settings panel
        return self.conf.build_settings(self.config, settings)

    def close_settings(self, settings=None):
        # close and save settings
        super().close_settings(settings)

    def on_pause(self):
        return True

    def on_config_change(self, config, section, key, value):
        self.conf.apply_user_setting(section, key, value)

if __name__ == '__main__':
    SlaveTamerApp().run()
