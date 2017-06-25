import yaml
import logging
from os import path

from kivy.core.audio import SoundLoader


class AudioStorage:
    # id->locale->{priority:num, file:str}
    _db = {}
    _player = None
    _music_player = None
    _music_curr = None

    def __init__(self, locale, default_locale='en-us'):
        self._locale = str(locale).lower()
        self._def_locale = default_locale

    def __getattr__(self, item):
        """
        Play sound one time anyway

        :param item: sound id
        """
        self._player = SoundLoader.load(self.get(item))
        self._player.play()
        return self

    play = __getattr__

    def music(self, item):
        """
        Change music in player or continue playing existing one

        :param item: sound id
        """
        if self._music_curr != item:
            if self._music_player:
                self._music_player.stop()
                self._music_player.unload()

            self._music_player = SoundLoader.load(self.get(item))
            self._music_player.loop = True
            self._music_player.play()

            self._music_curr = item

        return self

    def get(self, templ_id, **kwargs):
        template = None

        if templ_id in self._db:
            if self._locale in self._db[templ_id]:
                template = self._db[templ_id][self._locale]['file']

            elif self._def_locale in self._db[templ_id]:
                template = self._db[templ_id][self._def_locale]['file']

        if template:
            return template
        else:
            return templ_id

    def bulk_load(self, path_glob):
        """
        Bulk load YAML files into storage

        :param path_glob: array of paths
        """

        for file in path_glob:
            for doc in yaml.load_all(open(file, mode='r')):
                if 'sounddb' not in doc:
                    logging.warning('%s does not contains sounds' % file)
                else:
                    # locale and priority of current document
                    locale = doc['sounddb'].get('locale', self._def_locale)
                    priority = doc['sounddb'].get('priority', 0)

                    # iterate over each string
                    for k, v in doc['sounddb'].get('sounds', {}).items():

                        v = path.join(path.dirname(file), v)

                        # if key of this string exists in db
                        if k in self._db:

                            # if locale exists, select string with greater prio
                            if locale in self._db[k]:
                                if self._db[k][locale]['priority'] < priority:
                                    self._db[k][locale] = dict(
                                        priority=priority, file=v)
                        else:
                            self._db[k] = {locale: dict(priority=priority,
                                                        file=v)}

        return self
