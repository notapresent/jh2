# -*- coding: utf-8 -*-
import datetime
import os
import re
import traceback
from unicodedata import normalize

from rbm2m.util import to_unicode
from rbm2m.helpers import make_config

DUMP_TEMPLATE = '''Exeption: {}
Message: {}

Traceback:
{}

Additional notes:
{}
'''

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(to_unicode(text.lower())):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def dump_filename(name, suffix='.html'):
    """
        Make timestamped filename for error dump
    """
    timestamp = datetime.datetime.utcnow().strftime('%d-%m-%Y %H_%M_%S')
    return "{} - {}{}".format(timestamp, slugify(name), suffix)


def dump_exception(basename, exc_type, exc_val, tb, notes=''):
    """
        Dumps exception info to file along with additional notes
    """
    config = make_config()
    filename = dump_filename(basename)
    filepath = os.path.join(config.LOGS_DIR, filename)
    dump = DUMP_TEMPLATE.format(exc_type, exc_val, traceback.format_exc(tb), notes)
    with open(filepath, 'w') as f:
        f.write(dump)
