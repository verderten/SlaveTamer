import pyglet


class MusicManager:
    def __init__(self):
        self.file = None
        self.player = None

    def load(self, filename):
        self.file = pyglet.media.load(filename)

    def play(self):
        if self.file:
            self.player = self.file.play()