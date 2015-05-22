# -*- coding: utf-8 -*-
def to_unicode(unicode_or_str):
    """
    Takes a str or unicode and always returns a unicode

    :param unicode_or_str: unicode or str
    :return: unicode
    """
    if isinstance(unicode_or_str, str):
        value = unicode_or_str.decode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of unicode


def to_str(unicode_or_str):
    """
    Takes str or unicode and always returns a str

    :param unicode_or_str: unicode or str
    :return: unicode
    """
    if isinstance(unicode_or_str, unicode):
        value = unicode_or_str.encode('utf-8')
    else:
        value = unicode_or_str
    return value  # Instance of str
