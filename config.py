import os
import sys


def load_config(key, pos=1):
    try:
        value = os.environ[key]
    except:
        try:
            value = sys.argv[pos]
        except:
            raise RuntimeError('Missing config for %s' % key)
    return value