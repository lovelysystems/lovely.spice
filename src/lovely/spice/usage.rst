===============
Spice CLI Usage
===============

This module provides a simple CLI::

The -h argument displays the general usage::

    >>> o, e = run('bin/render', '-h')
    >>> print o
    usage: render [-h] template_path context_path target_path
    Render templates with given context into target folder
    positional arguments:
      template_path  The directory containing the templates to use.
      context_path   The path to the python file defining the context.
      target_path    The directory where the rendered files will be stored.
    optional arguments:
      -h, --help     show this help message and exit

