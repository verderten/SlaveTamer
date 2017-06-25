import cocos
import pyglet
import jinja2

from .text import TextStorage


class PreloadedLayer(cocos.layer.Layer):
    def __init__(self):
        super().__init__()
        self.text_db = TextStorage(locale='en-us')


class JinjaLabel(cocos.text.RichLabel):
    def __init__(self, *args, **kwargs):
        """
        RichLabel among with Jinja2 templates

        Same args like in RichLabel, but jinja argument
        to pass them into Jinja. Default variable textdb
        is passed representing TextStorage
        """
        self._jinja_args = kwargs.pop('jinja', {})
        self._template = kwargs.get('text', "")

        template = jinja2.Template(self._template)
        kwargs['text'] = template.render(textdb=TextStorage(locale='en-us'),
                                         **self._jinja_args)

        super().__init__(*args, **kwargs)

    def update(self, new_template=None, **kwargs):
        if new_template:
            self._template = new_template

        if kwargs:
            self._jinja_args.update(kwargs)

        template = jinja2.Template(self._template)
        self.element.text = template.render(
            textdb=TextStorage(locale='en-us'),
            **self._jinja_args)


class BackgroundLayer(PreloadedLayer):
    def __init__(self, image):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image(image)

    def draw(self):
        wsx, wsy = cocos.director.director.get_window_size()

        pyglet.gl.glColor4ub(255, 255, 255, 255)
        pyglet.gl.glPushMatrix()
        self.transform()
        self.img.blit(0, 0, width=wsx, height=wsy)
        pyglet.gl.glPopMatrix()


class GUILayer(PreloadedLayer):
    def __init__(self, config, callback_class):
        """
        Class for rendering GUI based on custom dict configs

        :param config: configuration
        :param callback_class: class with methods and attributes that will hold
        GUI events
        """
        super().__init__()

    def draw(self):
        wsx, wsy = cocos.director.director.get_window_size()
        cols = 10
        rows = 10



class HelloWorld(PreloadedLayer):
    is_event_handler = True

    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        self.label = JinjaLabel(text=self.text_db.mouse_movement,
                                anchor_x='center', anchor_y='center',
                                jinja=dict(x=0, y=0, action=""))

        self.position = 320, 240
        self.add(self.label)

    def update_text(self, x, y, type):
        self.label.update(x=x, y=y, type=type)

    def on_mouse_motion(self, x, y, dx, dy):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass

    def on_mouse_press(self, x, y, buttons, modifiers):
        self.posx, self.posy = cocos.director.director.get_virtual_coordinates(x, y)
        self.update_text(self.posx, self.posy, str(buttons) + str(modifiers))
