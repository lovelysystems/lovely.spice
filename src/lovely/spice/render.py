import sys
import os.path
import argparse
import logging
import shutil
from jinja2 import Environment, FileSystemLoader, StrictUndefined


logger = logging.getLogger(__name__)


def loadEnv(path):
    """ Load environment for given path
    """
    loader = loader = FileSystemLoader(path)
    return Environment(loader=loader, undefined=StrictUndefined)


class FolderRenderer(object):
    """ Render all templates to target
    """

    def __init__(self, templatePath, contextPath, targetPath):
        self.templatePath = templatePath
        self.targetPath = targetPath
        self.contextPath = contextPath

    def renderAll(self):
        self._cleanupTarget()
        folder = os.path.relpath(self.templatePath,
                                 os.path.dirname(self.templatePath))
        context = PyReader.loadFile(self.contextPath)
        env = loadEnv(self.templatePath)
        renderer = Renderer(env, context)
        for t in env.list_templates():
            path = os.path.realpath(os.path.join(self.targetPath,
                                                 folder,
                                                 t))
            self._createContainingFolder(path)
            renderer.render(t, path)

    def _createContainingFolder(self, path):
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            logger.debug('creating folder %s', parent)
            os.makedirs(parent)

    def _cleanupTarget(self):
        for subdir in os.listdir(self.targetPath):
            path = os.path.abspath(os.path.join(self.targetPath, subdir))
            logger.debug('removing folder %s', path)
            shutil.rmtree(path)


class Renderer(object):

    def __init__(self, env, context):
        self.env = env
        self.context = context

    def render(self, tempPath, targetPath):
        template = self.env.get_template(tempPath)
        with file(targetPath, 'w+') as f:
            logger.debug('generating %s', tempPath)
            template.stream(self.context).dump(f)


class PyReader(object):

    @classmethod
    def loadFile(cls, path, l={}, g={}):
        absPath = os.path.abspath(path)
        with file(absPath, 'rb') as f:
            return cls.load(f)

    @classmethod
    def load(cls, f, l={}, g={}):
        sys.path.append(os.path.dirname(f.name))
        exec(f, g, l)
        if '__all__' in l:
            # only attributes listed in __all__ are allowed
            allowed = set(l['__all__'])
            for k in list(l.keys()):
                if k not in allowed:
                    del l[k]
        else:
            # remove all keys starting with _
            for k in list(l.keys()):
                if k.startswith('_'):
                    del l[k]
        return l


def main():
    logging.basicConfig(level=logging.DEBUG)
    parser = argparse.ArgumentParser(
        description="Render templates with given context into target folder",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
    parser.add_argument(
        'template_path',
        help='The directory containing the templates to use.')
    parser.add_argument(
        'context_path',
        help='The path to the python file defining the context.')
    parser.add_argument(
        'target_path',
        help='The directory where the rendered files will be stored.')
    args = parser.parse_args()
    FolderRenderer(
        args.template_path,
        args.context_path,
        args.target_path).renderAll()
