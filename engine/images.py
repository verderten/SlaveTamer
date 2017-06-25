import yaml
import logging
from os import path

from kivy.atlas import Atlas


class ImageStorage:
    # id->locale->{priority:num, file:str}
    _db = {}

    def __init__(self, locale, default_locale='en-us'):
        self._locale = str(locale).lower()
        self._def_locale = default_locale

    def __getattr__(self, item):
        return self.get(item)

    def get(self, templ_id):
        template = None

        if templ_id in self._db:
            if self._locale in self._db[templ_id]:
                template = self._db[templ_id][self._locale]['file']

            elif self._def_locale in self._db[templ_id]:
                template = self._db[templ_id][self._def_locale]['file']

        if template:
            return template
        else:
            return self.get('empty')

    def bulk_load(self, path_glob):
        """
        Bulk load YAML files into storage

        :param path_glob: array of paths
        """

        for file in path_glob:
            for doc in yaml.load_all(open(file, mode='r')):
                if 'imagedb' not in doc:
                    logging.warning('%s does not contains images' % file)
                else:
                    # locale and priority of current document
                    locale = doc['imagedb'].get('locale', self._def_locale)
                    priority = doc['imagedb'].get('priority', 0)

                    # iterate over each string
                    for k, v in doc['imagedb'].get('images', {}).items():

                        v = path.join(path.dirname(file), v)

                        # if key of this string exists in db
                        if k in self._db:

                            # if locale exists, select image with greater prio
                            if locale in self._db[k]:
                                if self._db[k][locale]['priority'] < priority:
                                    self._db[k][locale] = dict(
                                        priority=priority, file=v)
                        else:
                            self._db[k] = {locale: dict(priority=priority,
                                                        file=v)}

                    # apply atlases found in yaml
                    for k, v in doc['imagedb'].get('atlases', {}).items():
                        atl = Atlas(path.join(path.dirname(file), v))

                        for k, v in atl.textures.items():
                            atl_path = 'atlas://%s/%s' % (
                                str(atl.filename).split('.atlas')[0].strip('./'),
                                k)

                            # if key of this string exists in db
                            if k in self._db:

                                # if locale exists, select image with greater prio
                                if self._db[k][locale]['priority'] < priority:
                                    self._db[k][locale] = dict(
                                        priority=priority, file=atl_path)
                            else:
                                self._db[k] = {locale: dict(priority=priority,
                                                            file=atl_path)}

        return self
