# "extend" the python path to allow a package/namespace to be
# rooted at multiple directories
# e.g.,
# locus-pipe/lib/locus/...
# locus-python/lib/locus/...
# see http://docs.python.org/library/pkgutil.html

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)
