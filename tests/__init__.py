# pylint: disable=import-outside-toplevel,too-many-arguments


# determine if running in an interactive environment
from qleet.interface import dashboard

INTERACTIVE = False

try:
    dashboard.__file__
except AttributeError:
    INTERACTIVE = True


def cli():
    """qLEET test command line interface"""
    return
