# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import setting_manager


DEFAULT_SETTINGS = {
    'formula_yml':
        {
            'title': 'Формула рассчета цены в YML',
            'value': '((x + x/5 + 2) * 1,07) * 60',
            'data_type': 'string',
            'description': 'В переменной <code>x</code> исходная цена записи на rbm в USD'
        },

    'formula_table':
        {
            'title': 'Формула рассчета цены в XLS',
            'value': 'x*60 if x < 1000 else x*60 + 10',
            'data_type': 'string',
            'description': 'В переменной <code>x</code> исходная цена записи на rbm в USD'
        },

    'yml_description_template':
        {
            'title': 'Шаблон описания лота в YML',
            'value': '''
{{artist}} - {{title}}, {{format}}<br>
<br>
Артикул товара:{{id}}<br>
Лейбл: {{label}}<br>
Грейд: {{grade}}<br>
Примечания: {{notes}}<br>
<br>
''',
            'data_type': 'text',
            'description': '''
Доступные переменные:<br>
<code>{{id}}</code> - ID<br>
<code>{{artist}}</code> - Исполнитель<br>
<code>{{title}}</code> - Название<br>
<code>{{format}}</code> - Формат<br>
<code>{{label}}</code> - Метка<br>
<code>{{grade}}</code> - Грейд<br>
<code>{{notes}}</code> - Примечания
''',
        },
    'yml_export_limit': {
            'title': 'Ограничение количества записей в YML',
            'value': 0,
            'data_type': 'string',
            'description': '0 - без ограничений'
        }
}


class UserSettings(dict):

    """
        User settings container
    """

    def __init__(self, session):
        self.manager = setting_manager.SettingManager(session)
        self._values = self.load_values()

    def load_values(self):
        """
            Load all settings from DB
        """
        rv = {}
        for setting in self.manager.all():
            rv[setting.name] = setting.to_dict()
        return rv

    def __iter__(self):
        return iter(self._values.keys())

    def __len__(self):
        return len(self._values.keys())

    def __getitem__(self, key):
        return self._values[key]

    def __setitem__(self, key, value):
        self._values[key]['value'] = value
        entry = self.manager.get(key)
        entry.value = value

    def __delitem__(self, key):
        del self._values[key]
        self.manager.delete_by_id(key)

    def reset(self):
        """
            Reset all settings to defaults
        """
        self.manager.delete_all()
        for name, val in DEFAULT_SETTINGS.items():
            val['name'] = name
            val['default_value'] = val['value']
            self.manager.from_dict(val)
