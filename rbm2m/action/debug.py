# -*- coding: utf-8 -*-
import datetime
import traceback

from ..helpers import slugify


DUMP_TEMPLATE = '''Exeption: {}
Message: {}

Traceback:
{}

Additional notes:
{}
'''


def dump_filename(name, suffix='.html'):
    """
        Make timestamped filename for error dump
    """
    timestamp = datetime.datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
    return "{} - {}{}".format(timestamp, slugify(name), suffix)


def dump_exception(basename, exc_type, exc_val, tb, notes=''):
    """
        Dumps exception info to file along with additional notes
    """
    filename = dump_filename(basename)
    dump = DUMP_TEMPLATE.format(exc_type, exc_val, traceback.format_exc(tb), notes)
    with open(filename, 'w') as f:
        f.write(dump)
