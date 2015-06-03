# -*- coding: utf-8 -*-
import collections.abc

from . import setting_manager


class UserSettings(collections.abc.Mapping):
    """
        User settings container
    """
    def __init__(self, session):
        self.manager = setting_manager.SettingManager(session)
        self._values = None

    @property
    def dict(self):
        """
            Dictionary containing all settings
        """
        if self._values is None:
            self._values = self.load_values()
        return self._values

    def load_values(self):
        """
            Load all settings from DB
        """
        rv = {}
        for setting in self.manager.all():
            rv[setting.name] = setting.to_dict()
        return rv

    def __iter__(self):
        return iter(self.dict)

    def __len__(self):
        return len(self.dict)

    def __getitem__(self, key):
        return self.dict[key].value

    def __setitem__(self, key, value):
        self.dict[key].value = value
        entry = self.manager.get(key)
        setattr(entry, key, value)

    def __delitem__(self, key):
        del self.dict[key]
        self.manager.delete_by_id(key)
