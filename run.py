import os, sys
import cocos
from glob import glob
import pyglet

from source.scenes import *
from source.layers import *
from source.text import TextStorage

TextStorage(locale='en-us').bulk_load(glob('./assets/text/*.yaml'))

pyglet.lib.load_library('avbin')
pyglet.options['audio'] = ('openal', 'silent')
pyglet.have_avbin = True

# director init takes the same arguments as pyglet.window
cocos.director.director.init(width=800, height=600,
                             resizable=True)
hello_layer = HelloWorld()
cocos.director.director.run(HelloScene(hello_layer))