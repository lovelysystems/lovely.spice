import unittest
import doctest


def setUp(test):
    pass


def tearDown(test):
    pass


def create_suite(testfile,
                 layer=None,
                 level=None,
                 setUp=setUp,
                 tearDown=tearDown,
                 cls=doctest.DocFileSuite,
                 encoding='utf-8'):
    suite = cls(
        testfile, tearDown=tearDown, setUp=setUp,
        optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
        encoding=encoding)
    if layer:
        suite.layer = layer
    if level:
        suite.level = level
    return suite


def test_suite():
    return unittest.TestSuite((
        create_suite('render.rst'),
    ))
