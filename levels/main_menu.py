import sys

from kivy.uix.screenmanager import ScreenManager, Screen


class MainMenuScreen(ScreenManager):
    pass


# Declare both screens
class MenuScreen(Screen):
    def on_quit_button(self):
        """
        Quit button on main screen
        :return:
        """
        sys.exit(0)


class SettingsScreen(Screen):
    pass

