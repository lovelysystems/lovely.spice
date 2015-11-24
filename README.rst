============
lovely spice
============

lovely.spice is a template renderer package to generate files from given
template path and given context file.


Usage
=====

usage: render [-h] template_path context_path target_path

Render templates with given context into target folder

positional arguments:
 | template_path  |   The directory containing the templates to use
 | context_path   |   The path to the python file defining the context
 | target_path    |   The directory where the rendered files will be stored

optional arguments:
  -h, --help     show this help message and exit


Development
===========

Run bootstrap::

    $ python bootstrap.py -v 2.3.1

And run buildout the project to generate the required scripts and command line
tools::

    $ bin/buildout -N

Run tests::

    $ bin/test
