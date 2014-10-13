from __future__ import unicode_literals, absolute_import
import os
import sys

from sandbox import settings
from sandbox.settings import *

sys.path.insert(0, os.path.join(os.path.dirname(settings.__file__), '..'))
