"""Let Django 2.2's vendored ``six`` import ``six.moves`` on Python 3.12+.

Django 2.2 ships six 1.10, whose meta-path importer only implements the
``find_module``/``load_module`` protocol that Python 3.12 removed. Several
pinned dependencies (DRF 3.9, django-cors-headers 3.0, ...) import
``django.utils.six.moves``, so without this they fail at start-up.
This adds the ``find_spec`` protocol, exactly as six 1.16 does upstream.
"""
import sys
from importlib.util import spec_from_loader

if sys.version_info >= (3, 12):
    from django.utils import six

    importer = six._importer
    cls = type(importer)
    if not hasattr(cls, "find_spec"):
        def find_spec(self, fullname, path, target=None):
            if fullname in self.known_modules:
                return spec_from_loader(fullname, self)
            return None

        def create_module(self, spec):
            return self.load_module(spec.name)

        def exec_module(self, module):
            pass

        cls.find_spec = find_spec
        cls.create_module = create_module
        cls.exec_module = exec_module
