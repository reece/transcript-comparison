# Simple on-disk memoizer
# 2010-03-17 17:41 Reece Hart <reecehart@gmail.com>

# Inspiration:
# http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# http://code.activestate.com/recipes/576642/
# http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
# http://code.activestate.com/recipes/498110-memoize-decorator-with-o1-length-limited-lru-cache/
# Expert Python Programming p. 52

import atexit, logging, os, shelve, sys

class memoize(object):
    """Decorator that caches a function's return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """

    import logging
    logging.basicConfig(level=logging.DEBUG)
    logger = logging
    
    def __init__(self, func):
        self._func = func
        dir='/tmp/memoize-%d' % (os.getuid())
        if not os.path.exists(dir):
            os.mkdir(dir,0700)                      # Is there a EAFP way to do this?
        cache_fn = os.path.join(dir,'%s.cache' % self._func.func_name)
        self.cache = shelve.open(cache_fn)
        self.logger.debug('opened cache for %s (%s)' % (self._func.func_name,cache_fn))
        atexit.register( lambda : self.cache.close() )

    def __call__(self, *args):
        #key = str(frozenset(args))
        # TODO: this is a lame key
        # consider pickle.dumps(function,args,kw) 
        key = str(args)
        if not self.cache.has_key(key):
            self.logger.debug('miss: %s(%s)' % (self._func.func_name,key))
            self.cache[key] = value = self._func(*args)
        else:
            self.logger.debug('hit: %s(%s)' % (self._func.func_name,key))
        return self.cache[key]


if __name__ == "__main__":
    @memoize
    def fib(n):
        return (n > 1) and (fib(n - 1) + fib(n - 2)) or 1
    print fib(5)
    print fib(5)
