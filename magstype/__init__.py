__version__ = '0.1.0'

import kivy.resources
from pkg_resources import resource_filename
respath = resource_filename(__name__, 'resources')
kivy.resources.resource_add_path(respath)
