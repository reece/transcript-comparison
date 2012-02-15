#!/usr/bin/env python

import exceptions, logging, pymongo

class mongo_cache(object):
    def __init__(self,connection,database,collection):
        self._conn = connection
        self._db = database
        self._coll = collection
        self._c = connection[database][collection]

    @property
    def connection(self):
        return self._conn
    @property
    def database(self):
        return self._db
    @property
    def collection(self):
        return self._coll

    def set_default(self,value):
        self.default_value = value

    def __unicode__(self):
        return '%s/%s/%s' % (self.connection,self.database,self.collection)
    def __str__(self):
        return unicode(self).encode('utf-8')

    def __setitem__(self,key,value):
        self._c.insert( {'key': key, 'value': value} )
        logging.info('%s[%s]: writing apx %d bytes' % (self,key,len(str(value))))
        #self._c.update( {'key': key}, {'key': key, 'value': value}, upsert=True )

    def __getitem__(self,key):
        try:
            value = self._c.find({'key': key}).next()['value']
            logging.info('%s[%s]: read apx %d bytes' % (self,key,len(str(value))))
            return value
        except StopIteration:
            try:
                return self.default_value
            except:
                pass
            raise KeyError("key `%s' doesn't exist" % (key))

    def __len__(self):
        return self._c.count()

    def __iter__(self):
        return self._c.find()

    def __delitem__(self,key):
        return self._c.remove({'key':key})

    def __contains__(self,key):
        return self._c.find_one({'key':key}) != None


if __name__ == '__main__':
    conn = pymongo.Connection(host='db-vpn.locusdev.net')
    mc = mongo_cache(conn,'test','pymongo_cache')
    rec = { 'street': '458 Brannan St', 'zip': '94107' }

    print '\n-----------'
    del mc['address']
    print 'address?', 'address' in mc
    mc['address'] = rec
    print 'address?', 'address' in mc, mc['address']

    #mc.set_default(None)
