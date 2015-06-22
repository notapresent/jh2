# -*- coding: utf-8 -*-
from flask.json import JSONEncoder as BaseJSONEncoder
from sqlalchemy.ext.declarative import declarative_base as real_declarative_base

# Let's make this a class decorator
declarative_base = lambda cls: real_declarative_base(cls=cls)


@declarative_base
class Base(object):

    """
    Add some default properties and methods to the SQLAlchemy declarative base.
    """
    __table_args__ = {
        'mysql_engine': 'InnoDB',
        'mysql_charset': 'utf8',
        'mysql_collate': 'utf8_general_ci'
    }

    @property
    def columns(self):
        return [c.name for c in self.__table__.columns]

    @property
    def column_items(self):
        return dict([(c, getattr(self, c)) for c in self.columns])

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return '<{}({})>'.format(self.__class__.__name__, self.column_items)


class JsonSerializer(object):

    """A mixin that can be used to mark a SQLAlchemy model class which
    implements a :func:`to_json` method. The :func:`to_json` method is used
    in conjuction with the custom :class:`JSONEncoder` class. By default this
    mixin will assume all properties of the SQLAlchemy model are to be visible
    in the JSON output. Extend this class to customize which properties are
    public, hidden or modified before being being passed to the JSON serializer.
    """

    __json_public__ = None
    __json_hidden__ = None
    __json_modifiers__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def to_json(self):
        field_names = self.get_field_names()

        public = self.__json_public__ or field_names
        hidden = self.__json_hidden__ or []
        modifiers = self.__json_modifiers__ or dict()

        rv = dict()
        for key in public:
            rv[key] = getattr(self, key)
        for key, modifier in modifiers.items():
            value = getattr(self, key)
            rv[key] = modifier(value, self)
        for key in hidden:
            rv.pop(key, None)
        return rv


class JSONEncoder(BaseJSONEncoder):

    """Custom :class:`JSONEncoder` which respects objects that include the
    :class:`JsonSerializer` mixin.
    """

    def default(self, obj):
        if isinstance(obj, JsonSerializer):
            return obj.to_json()
        return super(JSONEncoder, self).default(obj)