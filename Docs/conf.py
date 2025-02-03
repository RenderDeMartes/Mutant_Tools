# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
from __future__ import absolute_import
import sys, os

sys.path.insert(0, os.path.abspath('..'))
mutant_path = 'C://Users//Esteban//Documents//maya//2022//scripts//rigging'
sys.path.append(mutant_path)
import Mutant_Tools
global Mutant_Tools
maya_cmds = 'C://Program Files//Autodesk//Maya2022//Python37//Lib//site-packages'
sys.path.append(maya_cmds)
import maya

class Mock(object):

    __all__ = []

    def __init__(self, signature, *args, **kwargs):
        self._signature = signature

    def __repr__(self):
        return self._signature

    def __call__(self, *args, **kwargs):
        return Mock('%s()' % (self._signature,))

    def __getattr__(self, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        else:
            return Mock('%s.%s' % (self._signature, name))

#.\make.bat html

MOCK_MODULES = ['maya', 'maya.mel', 'shiboken2.shiboken2', 'pyside2uic', 'maya.OpenMaya', 'maya.api', 'maya.OpenMayaAnim', 'shiboken2', 'maya.api.OpenMaya', 'maya.cmds',
                'MayaNode']
for module in MOCK_MODULES:
    sys.modules[module] = Mock(module)


project = 'Mutant_Tools'
copyright = '2023, Esteban Rodriguez'
author = 'Esteban Rodriguez'
release = '1.20'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo',
              'sphinx.ext.autosummary', 'sphinx.ext.extlinks',
              'sphinx.ext.intersphinx',
              'sphinx.ext.viewcode', 'sphinx.ext.inheritance_diagram',
              'sphinx.ext.coverage']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
