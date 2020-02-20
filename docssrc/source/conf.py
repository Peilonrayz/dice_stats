import pathlib
import sys
import datetime

FILE_PATH = pathlib.Path(__file__).absolute()

# Add documentation for tests
TLD = FILE_PATH.parent.parent.parent
sys.path.insert(0, str(TLD))

project = 'dice_stats'
author = 'Peilonrayz'
copyright = f'{datetime.datetime.now().year}, {author}'
release = '0.0.1'

master_doc = 'index'
templates_path = ['_templates']
exclude_patterns = []

doctest_global_setup = '''
from fractions import Fraction

from dice_stats import Dice, Range
'''

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.graphviz',
    'sphinx.ext.githubpages',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
    'sphinx_rtd_theme',
    'sphinx_markdown_builder',
]
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None)
}

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

set_type_checking_flag = True
