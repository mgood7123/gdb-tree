def rec(x, level = 0):
  i = ' ' * level
  for (key, a) in x.items():
    if type(a) is tuple:
      previous, current = a
      if type(current) == dict:
        print("%s%s = {" % (i, key))
        rec(current, level + 2)
        print("%s}" % i)
      else:
        print("%s%s = \n%s%sprev = %s\n%s%scurr = %s" % (i, key, i,i,previous, i,i,current))
    elif type(a) is dict:
      print("%s%s = {" % (i, key))
      rec(a, level + 2)
      print("%s}" % i)
    else:
      print("%s%s = %s" % (i,key, str(a)))
      
# credit: altendky ##python freenode

import itertools

import attr

@attr.s(frozen=True, repr=False)
class Same:
    pass

    def __repr__(self):
        return type(self).__name__

Same = Same()

@attr.s(frozen=True, repr=False)
class Missing:
    pass

    def __repr__(self):
        return type(self).__name__

Missing = Missing()


@attr.s
class Dispatch:
    collected = attr.ib(factory=dict)

    def __call__(self, key=None):
        def decorator(f):
            self.collected[key] = f

            return f
        
        return decorator

    def __getitem__(self, item):
        return self.collected[item]


dispatch = Dispatch()

# ----------------------

mark_changed_dispatch = Dispatch()

@attr.s(frozen=True, repr=False)
class Changed:
    pass

    def __repr__(self):
        return type(self).__name__

Changed = Changed()

@mark_changed_dispatch(dict)
def dict_mark_changed(this, that):
    results = {}
    if this.keys() != that.keys():
        raise Exception('assumption broken')
    for (key, a), (other_key, b) in zip(this.items(), that.items()):
        results[key] = mark_changed(a, b)
    return results

@mark_changed_dispatch(list)
def list_mark_changed(this, that):
    results = []
    for a, b in itertools.zip_longest(this, that, fillvalue=Missing):
        results.append(mark_changed(a, b))
    
    return results

@mark_changed_dispatch(str)
@mark_changed_dispatch(int)
@mark_changed_dispatch(None)
def direct_mark_changed(this, that):
    if this == that:
        return Same
    
    return (this, that)

def mark_changed(this, that):
    if type(this) != type(that):
        key = None
    else:
        key = type(this)
    
    return mark_changed_dispatch[key](this, that)

# end of credit

curr = {}
prev = {}
diff = {}

def dodict(dict):
    global curr
    global prev
    if curr:
        prev = curr
        
    global diff
    curr = dict
    if prev:
      diff = mark_changed(prev, curr)
      print("diff = {")
      rec(diff, 2)
      print("}")

dodict({'val1' : '5', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '20', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '21', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '22', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '20', 'next' : {'val1' : '5', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'}, 'val2' : '0', 'string' : '0x555q555554b44 "HI"'})
