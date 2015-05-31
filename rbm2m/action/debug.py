# -*- coding: utf-8 -*-
import datetime
import urllib
import traceback


DUMP_TEMPLATE = '''Exeption: {}
Message: {}

Traceback:
{}

Additional notes:
{}
'''


def dump_filename(name):
    """
        Make timestamped filename for error dump
    """
    timestamp = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
    slug = urllib.quote_plus(str(name))
    return "{} {}.hmtl".format(timestamp, slug)


def dump_exception(exc_type, exc_val, tb, notes=None):
    """
        Dumps exception info to file along with additional notes
    """
    filename = dump_filename(exc_type)
    dump = DUMP_TEMPLATE.format(exc_type, exc_val, traceback.format_exc(tb),
                                notes or '')
    with open(filename, 'w') as f:
        f.write(dump)
