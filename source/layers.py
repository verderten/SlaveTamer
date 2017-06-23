import cocos
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
        template = jinja2.Template(kwargs.get('text'))
        kwargs['text'] = template.render(
            textdb=TextStorage(locale='en-us'),
            **kwargs.pop('jinja', {}))

        super().__init__(*args, **kwargs)


class HelloWorld(PreloadedLayer):
    def __init__(self):
        super(HelloWorld, self).__init__()

        # a cocos.text.Label is a wrapper of pyglet.text.Label
        # with the benefit of being a cocosnode
        label = JinjaLabel(text=self.text_db.hello_template,
                                 anchor_x='center', anchor_y='center',
                                     jinja=dict(mimi=5))

        label.position = 320, 240
        self.add(label)
