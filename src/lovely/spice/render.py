import sys
import os.path
import argparse
import logging
import shutil
from jinja2 import Environment, FileSystemLoader, StrictUndefined


logger = logging.getLogger(__name__)


class Renderer(object):

    def __init__(self, templatePath, contextPath, targetPath):
        self.templatePath = templatePath
        self.targetPath = targetPath
        self.contextPath = contextPath
        self._buildEnv()
        self._loadContext()

    def renderAll(self):
        self._cleanupTarget()
        folder = os.path.relpath(self.templatePath,
                                 os.path.dirname(self.templatePath))
        for t in self.env.list_templates():
            template = self.env.get_template(t)
            path = os.path.realpath(os.path.join(self.targetPath,
                                                 folder,
                                                 t))
            parent = os.path.dirname(path)
            if not os.path.exists(parent):
                logger.debug('creating folder %s', parent)
                os.makedirs(parent)
            with file(path, 'w+') as f:
                logger.debug('generating %s', t)
                template.stream(self.context).dump(f)

    def _cleanupTarget(self):
        for subdir in os.listdir(self.targetPath):
            path = os.path.abspath(os.path.join(self.targetPath, subdir))
            logger.debug('removing folder %s', path)
            shutil.rmtree(path)

    def _buildEnv(self):
        loader = loader = FileSystemLoader(self.templatePath)
        self.env = Environment(loader=loader,
                               undefined=StrictUndefined)

    def _loadContext(self):
        path = os.path.abspath(self.contextPath)
        with file(path, 'rb') as f:
            self.context = PyReader.load(f)


class PyReader(object):

    @classmethod
    def load(cls, f):
        l = {}
        g = {}
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
    Renderer(args.template_path,
             args.context_path,
             args.target_path).renderAll()
