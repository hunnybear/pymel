import os, sys

class ModuleInterceptor(object):
    """
    This class is used to intercept an unset attribute of a module to perfrom a callback. The
    callback will only be performed if the attribute does not exist on the module. Any error raised
    in the callback will cause the original AttributeError to be raised.
        
        >>> def cb( module, attr):
        >>>     if attr == 'this':
        >>>         print "intercepted"
        >>>     else:
        >>>         raise ValueError        
        >>> sys.modules[__name__] = ModuleInterceptor(__name__, cb)
    
    The class does not work when imported into the main namespace.    
    """
    def __init__(self, moduleName, callback):
        self.module = __import__( moduleName , globals(), locals(), [''] )
        self.callback = callback
    def __getattr__(self, attr):
        try:
            return getattr(self.module, attr)
        except AttributeError, msg:
            try:
                self.callback( self.module, attr)
            except:
                raise AttributeError, msg
#-----------------------------------------------
#  Pymel Internals
#-----------------------------------------------
def pythonToMel(arg):
    if isinstance(arg,basestring):
        return '"%s"' % cmds.encodeString(arg)
    elif isIterable(arg):
        return '{%s}' % ','.join( map( pythonToMel, arg) ) 
    return unicode(arg)
            
def capitalize(s):
    return s[0].upper() + s[1:]

def uncapitalize(s):
    return s[0].lower() + s[1:]
                        
  

def cacheProperty(getter, attr_name, fdel=None, doc=None):
    """a property type for getattr functions that only need to be called once per instance.
        future calls to getattr for this property will return the previous non-null value.
        attr_name is the name of an attribute in which to store the cached values"""
    def fget(obj):
        val = None
    
        if hasattr(obj,attr_name):            
            val = getattr(obj, attr_name)
            #print "cacheProperty: retrieving cache: %s.%s = %s" % (obj, attr_name, val)
            
        if val is None:
            #print "cacheProperty: running getter: %s.%s" %  (obj, attr_name)
            val = getter(obj)
            #print "cacheProperty: caching: %s.%s = %s" % (obj, attr_name, val)
            setattr(obj, attr_name, val )
        return val
                
    def fset(obj, val):
        #print "cacheProperty: setting attr %s.%s=%s" % (obj, attr_name, val)
        setattr(obj, attr_name, val)

    return property( fget, fset, fdel, doc)

def moduleDir():
    return os.path.dirname( os.path.dirname( sys.modules[__name__].__file__ ) )
    #return os.path.split( sys.modules[__name__].__file__ )[0]