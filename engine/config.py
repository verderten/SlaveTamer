from os import path
from glob import glob
import yaml
import json

from kivy.app import App


class ConfigManager:
    _db_defaults = {}
    _db_tabs = {}
    _db_settings = {}
    _name = None

    @property
    def name(self):
        return self.__class__._name

    @name.setter
    def name(self, value):
        self.__class__._name = value

    @property
    def _conffile(self):
        return self.name + '.ini'

    @property
    def _userfile(self):
        return self.name + '.yaml'

    @property
    def _conf_full_path(self):
        return path.join(self.user_data_dir, self._conffile)

    @property
    def _userconf_full_path(self):
        return path.join(self.user_data_dir, self._userfile)

    def __init__(self, name=None):
        if not name and not self.name:
            raise ModuleNotFoundError("Call manager with a name once")

        if not self.name or (name and self.name != name):
            self.name = name
            self.load_user_settings()

    def __getattr__(self, item):
        """
        Get an section__item
        """
        try:
            section, key = str(item).split('__')

        except ValueError as e:
            raise ValueError("Malformed parameter '%s'" % item)

        value = self.__class__._db_settings.get(section, {}).get(key)
        if not value:
            value = self._db_defaults.get(section, {}).get(key)

        if not value:
            raise ValueError(
                "Unknown attribute %s__%s" % (section, key))

        if section in self._db_defaults and key in self._db_defaults[section]:
            pass

        return value

    def set(self, item, value):
        try:
            section, key = str(item).split('__')
        except ValueError as e:
            raise ValueError("Malformed parameter '%s'" % item)

        self.apply_user_setting(section, key, value)

    def apply_user_setting(self, section, key, value):
        """
        Apply one setting immediately
        """
        if section in self._db_settings:
            self._db_settings[section][key] = value

        else:
            self._db_settings[section] = {key: value}

        self.update_user_settings()

    def init_user_settings(self):
        """
        Write template of user settings
        """
        with open(self._userconf_full_path, mode='w') as file:
            file.write(yaml.dump(dict(userconf={})))

    def update_user_settings(self):
        """
        Update settings on drive
        """
        with open(self._userconf_full_path, mode='w') as file:
            file.write(yaml.dump(dict(userconf=self._db_settings)))

    def load_user_settings(self):
        """
        Open handler to user settings. If none, write template
        """
        with open(self._userconf_full_path, mode='r') as file:
            settings = yaml.load(file.read())
            if not settings:
                file.close()
                self.init_user_settings()
                self.load_user_settings()

            else:
                self.__class__._db_settings = settings['userconf']

        return self

    def get_main_path(self):
        return self._conf_full_path

    user_data_dir = App.user_data_dir

    def bulk_load(self, glob):
        # load configuration profiles and default settings

        for file in glob:
            for doc in yaml.load_all(open(file, mode='r')):
                if 'appconf' in doc:

                    # update default settings
                    for k, v in doc['appconf'].get('defaults', {}).items():
                        if k in self._db_defaults:
                            self._db_defaults[k].update(v)
                        else:
                            self._db_defaults[k] = v

                    # generate config tab
                    tab_key = doc['appconf'].get("tab", "Default")
                    if tab_key not in self._db_tabs:
                        self._db_tabs[tab_key] = [{
                            'type': 'title',
                            'title': doc['appconf'].get("title", "Settings")
                        }]

                    # add new items to tab
                    for section, parms in doc['appconf'].get("content", {}).items():
                        for parm in parms:
                            parm['section'] = section

                            self._db_tabs[tab_key].append(parm)

        return self

    def build_config(self, config=None):
        """
        Store defaults and apply modified settings

        :param config: application config
        """
        for section, defs in self._db_defaults.items():
            config.setdefaults(section, defs)

        if self._db_settings:
            for section, setting_dict in self._db_settings.items():
                # ignore sections we doesn't have anymore
                if section in self._db_defaults:
                    config.setall(section, setting_dict)

    def build_settings(self, config, settings):
        for tab, json_data in self._db_tabs.items():
            settings.add_json_panel(tab, config,
                                    filename=None,
                                    data=json.dumps(json_data))
