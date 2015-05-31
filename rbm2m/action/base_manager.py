# -*- coding: utf-8 -*-


class BaseManager(object):
    """
        Base class for database managers
    """
    __class__ = None

    def __init__(self, session):
        self.session = session

    def get(self, item_id):
        """
            Get object by id
        """
        return self.session.query(self.__class__).get(item_id)

    def from_dict(self, d):
        """
            Create new instance with properties set from dict
        """
        obj = self.__class__(**d)
        self.session.add(obj)
        self.session.flush()
        return obj
