# Simple on-disk memoizer
# 2010-03-17 17:41 Reece Hart <reecehart@gmail.com>

# Inspiration:
# http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
# http://code.activestate.com/recipes/576642/
# http://code.activestate.com/recipes/325205-cache-decorator-in-python-24/
# http://code.activestate.com/recipes/498110-memoize-decorator-with-o1-length-limited-lru-cache/
# Expert Python Programming p. 52

import hashlib, logging, os, pickle, pymongo, sys

from mongo_cache import mongo_cache

conn = pymongo.Connection(host='db-vpn.locusdev.net')

class memoize(object):
    """Mongo-based memoization.
    """

    import logging
    
    def __init__(self, func):
        self._func = func
        self._cache = mongo_cache(conn,'memoize',func.func_name)
        logging.info('opened mongo cache for %s (%s)' % (self._func.func_name,self._cache))

    def compute_key(self,args,kw):
        key = pickle.dumps((self._func.func_name,args,kw))
        return hashlib.sha1(key).hexdigest()

    def __call__(self, *args, **kw):
        key = '%s(%s;%s)' % (self._func.func_name, str(args), str(kw))
        # If previous key method fails, consider compute_key, like this:
        # key = self.compute_key(args,kw)
        if key not in self._cache:
            logging.info('miss: %s' % (key))
            self._cache[key] = self._func(*args,**kw)
        else:
            logging.info('hit: %s' % (key))
        return self._cache[key]


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    @memoize
    def fib(n):
        return (n > 1) and (fib(n - 1) + fib(n - 2)) or 1
    print fib(5)
    print fib(5)

    @memoize
    def exp(b,p):
        return b**p;
    print exp(2,5)
    print exp(2,5)

    print exp(b=2,p=5)
    print exp(b=2,p=5)
    print exp(p=5,b=2)