# pylint: disable=import-outside-toplevel,too-many-arguments
import argparse
import pathlib
import subprocess
import sys


# determine if running in an interactive environment
import __main__

INTERACTIVE = False

try:
    __main__.__file__
except AttributeError:
    INTERACTIVE = True

def cli():
    """ qLEET test command line interface """
    return
