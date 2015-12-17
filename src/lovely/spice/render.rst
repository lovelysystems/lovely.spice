==============
renderer tests
==============

The Renderer
============

A Renderer class is one generic implementation to render templates located in
the given template environment to one defined path.

To use a renderer we need a template environment. This can be created by the
function `loadEnv`::

    >>> import os
    >>> import tempfile
    >>> b = tempfile.mkdtemp(prefix='templates_')
    >>> with open(os.path.join(b, 'one.ini'), 'w+') as f:
    ...     f.write('one {{var}}')

    >>> from lovely.spice import render
    >>> env = render.loadEnv(b)
    >>> env
    <jinja2.environment.Environment object at 0x...>

    >>> env.list_templates()
    ['one.ini']

The template environment does also follow symlinks::

    >>> source = os.path.join(b, 'one.ini')
    >>> target = os.path.join(b, 'two.ini')
    >>> os.symlink(source, target)

    >>> env = render.loadEnv(b)
    >>> env.list_templates()
    ['one.ini', 'two.ini']

the sencond required parameter for a Renderer is the context. A context can by
loaded by the PyReader class::

    >>> cdir = tempfile.mkdtemp()
    >>> c = os.path.join(cdir, 'context.py')
    >>> with open(c, 'w+') as f:
    ...     f.write('var = "eins"')

    >>> context = render.PyReader.loadFile(c)
    >>> context
    {'var': 'eins'}

The renderer supports one public method called `render`. This method renders
the template with the given name located in the initially given template
envinronment to the given target path::

    >>> t = tempfile.mktemp()
    >>> renderer = render.Renderer(env, context)
    >>> renderer.render('one.ini', t)
    >>> with open(t, "r") as f:
    ...     f.read()
    'one eins'


The FolderRenderer
==================

The FolderRenderer is one specific renderer to render *all* templates from
given template folder recoursively into target folder by using a context
loaded from the given context.

Create one template folder (b), one context file (c) and one target folder
(t). The template folder (b) contains one template called 'one.ini' and the
context file will provide the required variable called 'var'::

    >>> import os
    >>> import tempfile
    >>> b = tempfile.mkdtemp(prefix='templates_')
    >>> with open(os.path.join(b, 'one.ini'), 'w+') as f:
    ...     f.write('one {{var}}')

    >>> cdir = tempfile.mkdtemp()
    >>> c = os.path.join(cdir, 'context.py')
    >>> with open(c, 'w+') as f:
    ...     f.write('var = "eins"')

    >>> t = tempfile.mkdtemp(prefix='target_')

Now initialize one renderer and render all templates within the given template
folder::

    >>> r = render.FolderRenderer(b, c, t)
    >>> r.render()

The target folder will now contain a subfolder called like the given template
folder and within that folder is the generated file::

    >>> for f in os.walk(t):
    ...     print f
    ('.../target_...', [], ['one.ini'])

The template has been rendered properly::

    >>> with open(os.path.join(t, 'one.ini'), 'r') as f:
    ...     print f.read()
    one eins

If one template requires one not existing variable the renderer will fail::

    >>> with open(os.path.join(b, 'one.ini'), 'w+') as f:
    ...     f.write('one {{varX}}')

    >>> r = render.FolderRenderer(b, c, t)
    >>> r.render()
    Traceback (most recent call last):
    UndefinedError: 'varX' is undefined

The created files in the target folder will have the same filename as their
templates so the templatePath MUST NOT be same as the targetPath::

    >>> r = render.FolderRenderer(b, c, b)
    Traceback (most recent call last):
    Exception: templatePath MUST NOT be targetPath

The given context file might contain imports of other files::

    >>> c = tempfile.mktemp(prefix='context_', suffix='.py')
    >>> with open(c, 'w') as f:
    ...     f.write('from common import *\nvar = "eins"')

    >>> common = os.path.join(cdir, 'common.py')
    >>> with open(common, 'w+') as f:
    ...     f.write('varX = "exists"')

    >>> r = render.FolderRenderer(b, c, t)
    >>> r.render()

    >>> with open(os.path.join(t, 'one.ini'), 'r') as f:
    ...     print f.read()
    one exists


The FileRenderer
================

The FileRenderer is one specific renderer to render *one* template from
given templatePath into targetPath by using a context
loaded from the given context::

    >>> r = render.FileRenderer(b + '/one.ini', c, t + "/rendered.ini")
    >>> r.render()

    >>> with open(os.path.join(t, 'rendered.ini'), 'r') as f:
    ...     print f.read()
    one exists

The templatePath and the targetPath MUST NOT be equal::

    >>> r = render.FileRenderer(b + '/one.ini', c, b + "/one.ini")
    Traceback (most recent call last):
    Exception: templateFile MUST NOT be targetFile
