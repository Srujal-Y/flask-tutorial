import os
import subprocess
import sys
from flask import Blueprint
import click

bp = Blueprint('cli', __name__, cli_group=None)


def pybabel(*args):
    return subprocess.run(
        [sys.executable, '-m', 'babel.messages.frontend', *args],
        check=False
    ).returncode


@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if pybabel('extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot',
               '.'):
        raise RuntimeError('extract command failed')
    if pybabel('init', '-i', 'messages.pot', '-d', 'app/translations', '-l',
               lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""
    if pybabel('extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot',
               '.'):
        raise RuntimeError('extract command failed')
    if pybabel('update', '-i', 'messages.pot', '-d', 'app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    if pybabel('compile', '-d', 'app/translations'):
        raise RuntimeError('compile command failed')
