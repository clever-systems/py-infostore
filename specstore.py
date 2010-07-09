import os, re, sys
from configobj import ConfigObj, flatten_errors
from validate import Validator
from pprint import pprint, pformat

def get_custom_validators():
    connection_re = re.compile('^\w+@(\d+\.\d+\.\d+\.\d+|\w(\.\w)*)(\:\d+)?$')
    def check_connection(value):
      return value

    def check_target(value, targettype):
      return value

    def check_dir(value):
      return value
    return {'connection':check_connection, 'target': check_target, 'dir': check_dir}

def listfiles(dir):
    return [x for x in os.listdir(dir) if os.path.isfile(os.path.join(dir, x))]

class InfoStore(dict):
    def __init__(self, dir):
        super(type(self), self).__init__()
        self.dir = dir
        self.types_dir = os.path.join(self.dir,'type')
        self.item_container_dir = os.path.join(self.dir,'item')
        typenames = listfiles(self.types_dir)
        for typename in typenames:
            typeinfo_file = os.path.join(self.types_dir, typename)
            typeinfo = ConfigObj(typeinfo_file, list_values=False)
            self[typename] = TypeInfo(self, typename, typeinfo)
            items_dir = os.path.join(self.item_container_dir, typename)
            itemnames = listfiles(items_dir)
            for itemname in itemnames:
                iteminfo_file = os.path.join(items_dir, itemname)
                print('File: %s' % iteminfo_file)
                print('Spec: %s' % pformat(typeinfo))
                iteminfo = ConfigObj(iteminfo_file, list_values=False, configspec = typeinfo)
                self[typename][itemname] = ItemInfo(self, itemname, iteminfo)
        validator = Validator(get_custom_validators())
        for typename, typeinfo in self.iteritems():
            for itemname, iteminfo in typeinfo.iteritems():
                result = iteminfo.info.validate(validator)
                if result != True:
                    print 'Result %s: %s' %(targettype, pformat(result))
                    print 'Errors: %s' %pformat(flatten_errors(config, result))
    def __str__(self):
        return super(type(self), self).__str__()
    def __repr__(self):
        return "%s(%s))" % (self.__class__.__name__,super(type(self), self).__repr__())

class TypeInfo(dict):
    def __init__(self, store, name, info):
        super(type(self), self).__init__()
        self.store = store
        self.name = name
        self.info = info
    def __str__(self):
        return super(type(self), self).__str__()
    def __repr__(self):
        return "%s(%s))" % (self.__class__.__name__,super(type(self), self).__repr__())

class ItemInfo():
    def __init__(self, store, name, info):
        super(type(self), self).__init__()
        self.store = store
        self.name = name
        self.info = info
    def __str__(self):
        return self.info.__str__()
    def __repr__(self):
        return "%s(%s))" % (self.__class__.__name__,self.info.__repr__())
    

