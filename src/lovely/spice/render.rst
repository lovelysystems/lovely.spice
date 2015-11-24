============
The renderer
============

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

    >>> from lovely.spice import render
    >>> r = render.Renderer(b, c, t)
    >>> r.renderAll()

The target folder will now contain a subfolder called like the given template
folder and within that folder is the generated file::

    >>> for f in os.walk(t):
    ...     print f
    ('.../target_...', ['templates_...'], [])
    ('.../target_.../templates_...', [], ['one.ini'])

The template has been rendered properly::

    >>> folder = os.path.relpath(b, os.path.dirname(b))
    >>> with open(os.path.join(t, folder, 'one.ini'), 'r') as f:
    ...     print f.read()
    one eins

If one template requires one not existing variable the renderer will fail::

    >>> with open(os.path.join(b, 'one.ini'), 'w+') as f:
    ...     f.write('one {{varX}}')

    >>> r = render.Renderer(b, c, t)
    >>> r.renderAll()
    Traceback (most recent call last):
    UndefinedError: 'varX' is undefined

The given context file might contain imports of other files::

    >>> c = tempfile.mktemp(prefix='context_', suffix='.py')
    >>> with open(c, 'w') as f:
    ...     f.write('from common import *\nvar = "eins"')

    >>> common = os.path.join(cdir, 'common.py')
    >>> with open(common, 'w+') as f:
    ...     f.write('varX = "exists"')

    >>> r = render.Renderer(b, c, t)
    >>> r.renderAll()

    >>> with open(os.path.join(t, folder, 'one.ini'), 'r') as f:
    ...     print f.read()
    one exists

