import os
import string
from random import choice


def _generate_secret_key(length=64):
    return ''.join(
        [choice(string.ascii_letters + string.digits) for _ in range(length)]
    )


def _generate_secret_key_file(filepath=None):
    if filepath is None:
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(filepath, '.secret_key')

    secret_key = _generate_secret_key()
    with open(os.open(filepath, os.O_CREAT | os.O_WRONLY, 0o600), 'w') as f:
        f.write(secret_key)

    return secret_key


def get_secret_key(filepath=None):
    """
    We will always get a secret key, one way or another. Either find
    a cached key, generate a cached key, or just generate a non-cached key,
    sessions be damned.

    :param filepath:
    :type filepath:
    :return:
    :rtype:
    """
    if filepath is None:
        filepath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filepath = os.path.join(filepath, '.secret_key')

    secret_key = _generate_secret_key()
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            secret_key = f.read()
    else:
        try:
            secret_key = _generate_secret_key_file(filepath)
        except (OSError, IOError):
            pass

    return secret_key
