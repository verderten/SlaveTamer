import cocos
import os

from .music import MusicManager


class HelloScene(cocos.scene.Scene):
    def __init__(self, *args):
        super(HelloScene, self).__init__(*args)

        self.music = MusicManager()
        self.music.load(os.path.join(os.path.dirname(__file__),
                                     '../assets/audio/music/border.ogg'))
        self.music.play()