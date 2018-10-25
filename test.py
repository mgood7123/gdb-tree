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
        if a == b:
            results[key] = a
            continue

        results[key] = mark_changed(b, a)
    return results

@mark_changed_dispatch(list)
def list_mark_changed(this, that):
    results = []
    for a, b in itertools.zip_longest(this, that, fillvalue=Missing):
        results.append(mark_changed(b, a))
    
    return results

@mark_changed_dispatch(str)
@mark_changed_dispatch(int)
@mark_changed_dispatch(None)
def direct_mark_changed(this, that):
    if this == that:
        return this
    
    return Changed

def mark_changed(that, this):
    if type(this) != type(that):
        key = None
    else:
        key = type(this)
    
    return mark_changed_dispatch[key](this, that)


curr = {}
prev = {}
diff = {}
diff_curr = {}
diff_curr2 = {}
diff_prev = {}

def dodict(dict):
    global curr
    global prev
    if curr:
        prev = curr
        
    global diff_curr
    global diff_curr2
    global diff_prev
    if diff_curr:
        diff_prev = diff_curr
        
    curr = dict
    print("curr = [")
    #rec(curr, 2)
    print("]")

    print("prev = [")
    #rec(prev, 2)
    print("]")

    if prev:
      diff_curr = mark_changed(curr, prev)
    
      print("diff_curr = [")
      #rec(diff_curr, 2)
      print("]")
    
      print("diff_prev = [")
      #rec(diff_prev, 2)
      print("]")
      if diff_prev:
        diff_curr2 = mark_changed(diff_curr, diff_prev)
        print("diff_curr2 = [")
        #rec(diff_curr2, 2)
        print("]")
    
    print("curr = %s" % curr)
    print("prev = %s" % prev)
    
    print("dfc1 = %s" % diff_curr)
    print("dfp1 = %s" % diff_prev)
    print("dfc2 = %s" % diff_curr2)

dodict({'val1' : '5', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '20', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '21', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '22', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'})
dodict({'val1' : '20', 'next' : {'val1' : '5', 'next' : 'NULL', 'val2' : '0', 'string' : '0x555555554b44 "HI"'}, 'val2' : '0', 'string' : '0x555q555554b44 "HI"'})
