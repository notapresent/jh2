# -*- coding: utf-8 -*-
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
