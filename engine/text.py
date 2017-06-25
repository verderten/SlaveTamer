import jinja2
import yaml
import logging


class TextStorage:
    # id->locale->{priority:num, string:str}
    _db = {}

    def __init__(self, locale, default_locale='en-us'):
        self._locale = str(locale).lower()
        self._def_locale = default_locale

    def __getattr__(self, item):
        return self.get(item)

    def get(self, templ_id, **kwargs):
        template = None

        if templ_id in self._db:
            if self._locale in self._db[templ_id]:
                template = self._db[templ_id][self._locale]['string']

            elif self._def_locale in self._db[templ_id]:
                template = self._db[templ_id][self._def_locale]['string']

        if template:
            template = jinja2.Template(template)
            return template.render(textdb=TextStorage('en-us'), **kwargs)
        else:
            return templ_id

    def bulk_load(self, path_glob):
        """
        Bulk load YAML files into storage

        :param path_glob: array of paths
        """

        for file in path_glob:
            for doc in yaml.load_all(open(file, mode='r')):
                if 'textdb' not in doc:
                    logging.warning('%s does not contains text' % file)
                else:
                    # locale and priority of current document
                    locale = doc['textdb'].get('locale', self._def_locale)
                    priority = doc['textdb'].get('priority', 0)

                    # iterate over each string
                    for k, v in doc['textdb'].get('strings', {}).items():

                        # if key of this string exists in db
                        if k in self._db:

                            # if locale exists, select string with greater prio
                            if locale in self._db[k]:
                                if self._db[k][locale]['priority'] < priority:
                                    self._db[k][locale] = dict(
                                        priority=priority, string=v)
                        else:
                            self._db[k] = {locale: dict(priority=priority,
                                                        string=v)}

        return self
