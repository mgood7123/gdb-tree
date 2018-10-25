import gdb

depth = 4

curr = {}
prev = {}
diff = {}


def valinfo(foo_val):
        c = foo_val.type.code
        gdb.write('Symbol is of type "%s" and a value of type "%s" and value "%s"\n' % (c, foo_val, foo_val.address))

def valinfo2(foo_val):
        c = foo_val.type
        gdb.write('Symbol is of type "%s" and a value of type "%s" and value "%s"\n' % (c, foo_val, foo_val.address))

#source https://stackoverflow.com/questions/16787289/gdb-python-parsing-structures-each-field-and-print-them-with-proper-value-if

def is_container(v):
    c = gdb.types.get_basic_type(v.type).code
    return (c == gdb.TYPE_CODE_STRUCT or c == gdb.TYPE_CODE_UNION)

def is_pointer(v):
    v = gdb.types.get_basic_type(v.type).code
    return (v == gdb.TYPE_CODE_PTR)

def what_type(v):
        c = v.type
        gdb.write('type "%s", ' % c)
        c = gdb.types.get_basic_type(v.type)
        gdb.write('type "%s"\n' % c)
        gdb.write('gdb.TYPE_CODE_PTR "%s"\n' % gdb.TYPE_CODE_PTR)
        gdb.write('gdb.TYPE_CODE_ARRAY "%s"\n' % gdb.TYPE_CODE_ARRAY)
        gdb.write('gdb.TYPE_CODE_STRUCT "%s"\n' % gdb.TYPE_CODE_STRUCT)
        gdb.write('gdb.TYPE_CODE_UNION "%s"\n' % gdb.TYPE_CODE_UNION)
    
def is_string(v):
    return str(v.type).startswith("char")

lineend = ';'

def print_struct_follow_pointers_inner(frame, name, value, curr, level_limit = 3, level = 0, pointers = 0):
    tmp = {}
    curr[name] = tmp

    indent = '  ' * level
    pointer_indent = '*' * pointers
    s = value
    stype = gdb.types.get_basic_type(s.type)
    

    if not is_container(s):
        gdb.write('%s%s\n' % (indent, s))
        return

    if level < level_limit:
        gdb.write('%s%s {\n' % (indent, stype,))
        level = level + 1
        indent = '  ' * level
        for k in stype.keys():
            v = s[k]
            vtype = gdb.types.get_basic_type(v.type)
            if is_pointer(v) and not is_string(v):
                try:
                    v1 = v
                    while is_pointer(v1):
                        pointers = pointers + 1
                        v1 = v1.dereference()
                        v1.fetch_lazy()
                except gdb.error:
                    gdb.write('%s%s %s = NULL%s\n' % (indent, vtype, k, lineend))
                    tmp[k] = "NULL"
                    continue
                print_struct_follow_pointers_inner(frame, k, v1, tmp, level_limit, level)
            elif is_container(v):
                print_struct_follow_pointers_inner(frame, k, v, tmp, level_limit, level)
            else:
                gdb.write('%s%s %s = %s%s\n' % (indent, vtype, k, v, lineend))
                tmp[k] = str(v)
        level = level - 1
        indent = '  ' * level
        gdb.write('%s} %s %s%s\n' % (indent, pointer_indent, name, lineend))
    else:
        gdb.write('%s%s { ... } %s %s%s\n' % (indent, stype, pointer_indent, name, lineend))

def print_struct_follow_pointers(frame, foo_sym, value, curr, level_limit = 3, level = 0):
    curr = {}
    indent = '  ' * level
    s = value
    stype = gdb.types.get_basic_type(s.type)
    pointers = 0

    if not is_container(s):
        gdb.write('%s%s\n' % (indent, s))
        return curr

    if level < level_limit:
        gdb.write('%s%s {' % (indent, stype,))
        gdb.write('\n')
        level = level + 1
        indent = '  ' * level

        for k in stype.keys():
            v = s[k]
            vtype = gdb.types.get_basic_type(v.type)
            if is_pointer(v) and not is_string(v):
                try:
                    v1 = v.dereference()
                    v1.fetch_lazy()
                    pointers = pointers + 1
                except gdb.error:
                    gdb.write('%s%s %s = NULL%s\n' % (indent, vtype, k, lineend))
                    curr[k] = "NULL"
                    continue
                print_struct_follow_pointers_inner(frame, k, v1, curr, level_limit, level, pointers)
            elif is_container(v):
                print_struct_follow_pointers_inner(frame, k, v, curr, level_limit, level, pointers)
            else:
                gdb.write('%s%s %s = %s%s\n' % (indent, vtype, k, v, lineend))
                curr[k] = str(v)
        level = level - 1
        indent = '  ' * level
        gdb.write('%s} ' % indent)
    else:
        gdb.write('%s%s { ... } ' % (indent, stype,))
    ptr = foo_sym.value

    footype = gdb.types.get_basic_type(foo_sym.value(frame).type)
    
    ptrtype = gdb.types.get_basic_type(ptr(frame).type)
    if ptrtype.code == gdb.TYPE_CODE_PTR:
        ptr = ptr(frame).dereference
        ptrtype = gdb.types.get_basic_type(ptr().type)
        gdb.write('*')
        while ptrtype.code == gdb.TYPE_CODE_PTR:
            ptr = ptr().dereference
            ptrtype = gdb.types.get_basic_type(ptr().type)
            gdb.write('*')
    if footype.code == gdb.TYPE_CODE_PTR:
        gdb.write(' ')
    gdb.write('%s%s\n' % (foo_sym.name, lineend))
    return curr

# source https://stackoverflow.com/questions/23578312/gdb-pretty-printing-with-python-a-recursive-structure/23970415?s=2|8.2641#23970415

def syminfo(foo_sym):
        gdb.write('Symbol "%s" found and is of type "%s" and a value of type "%s" and value "%s"\n' % (foo_sym.name, foo_sym.type, foo_sym.value, foo_sym.value()))

#shall check if a dict contains only X values
def rec_(x, level = 0):
  nones = 0
  i = ' ' * level
  for (key, a) in x.items():
    if a is Same:
      nones = nones + 1
    if type(a) is tuple:
      previous, current = a
      level = level + 2
      i = ' ' * level
      if type(previous) == dict:
        rec_(previous, level + 2)
      if type(current) == dict:
        rec_(current, level + 2)
      level = level - 2
      i = ' ' * level
    elif type(a) is dict:
      obtained_len = rec_(a, level + 2)
      if obtained_len == len(a):
        nones = nones + 1
  return nones

def rec(x, level = 0):
  i = ' ' * level
  for (key, a) in x.items():
    if type(a) is tuple:
      previous, current = a
      gdb.write("%s%s = \n" % (i,key))
      level = level + 2
      i = ' ' * level
      gdb.write("%sprev = " % i)
      if type(previous) == dict:
        if previous == {}:
          gdb.write("empty\n")
        else:
          gdb.write("{\n")
          rec(previous, level + 2)
          gdb.write("%s}\n" % (i))
      else:
        gdb.write("%s\n" % previous)
      gdb.write("%scurr = " % (i))
      if type(current) == dict:
        if current == {}:
          gdb.write("empty\n")
        else:
          gdb.write("{\n")
          rec(current, level + 2)
          gdb.write("%s}\n" % (i))
      else:
        gdb.write("%s\n" % current)
      level = level - 2
      i = ' ' * level
    elif type(a) is dict:
      gdb.write("%s%s = " % (i, key))
      if a == {}:
          gdb.write("NULL\n")
      else:
        if len(a) == rec_(a):
          gdb.write("Same\n")
        else:
          gdb.write("{\n")
          rec(a, level + 2)
          gdb.write("%s}\n" % i)
    else:
      gdb.write("%s%s = %s\n" % (i,key, str(a)))
      
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

def do_dot(foo_sym, frame):
    foo_val = foo_sym.value
    if foo_val(frame).type.code == gdb.TYPE_CODE_PTR:
        foo_val = foo_val(frame).dereference
        while foo_val().type.code == gdb.TYPE_CODE_PTR:
            foo_val = foo_val().dereference
    global curr
    global prev
    if curr:
        prev = curr
        
    global diff
        
    curr = print_struct_follow_pointers(frame, foo_sym, foo_val(), curr, depth)
    if prev:
      diff = mark_changed(prev, curr)
    
      gdb.write("diff = ")
      if len(diff) == rec_(diff):
        gdb.write("Same\n")
      else:
        gdb.write("{\n")
        rec(diff, 2)
        gdb.write("}\n")
        rec_(diff, 2)
        
    #gdb.write("curr = %s\n" % curr)
    #gdb.write("prev = %s\n" % prev)
    gdb.write("diff = %s\n" % diff)

    

def not_running():
    gdb.write('The program is not being run.\n')

def pc(name):
    val = None
    try:
        val = gdb.parse_and_eval('$pc')
    except:
        return None
    return long(val)

def frame():
    val = None
    try:
        val = gdb.parse_and_eval('$pc')
    except:
        return None
    return long(val)

def check_block(block):
    if block is None:
        gdb.write('block is None.\n')

def find_global(name, pcval, frame):
    block = gdb.block_for_pc(pcval).global_block
    if block is None:
        gdb.write('block is None.\n')
    found = False
    for symbol in block:
        if symbol.name == str(name):
            found = True
            do_dot(symbol, frame)
    if found == False:
        gdb.write('No symbol "%s" in global block.\n' % str(name))
    return found

def find_local(name, pcval, frame):
    block = gdb.block_for_pc(pcval)
    if block is None:
        gdb.write('block is None.\n')
    found = False
    for symbol in block:
        if symbol.name == str(name):
            found = True
            do_dot(symbol, frame)
    if found == False:
        gdb.write('No symbol "%s" in local block.\n' % str(name))
    return found
    
def find_frame_current(name, pcval, frame):
    try:
        node = gdb.current_frame().read_var(name)
        do_dot(node, frame)
    except:
        gdb.write('No symbol "%s" in local frame.\n' % str(name))
            
def find_context_global(name, pcval, frame):
    try:
        node = gdb.lookup_global_symbol(str(name))
        do_dot(node, frame)
    except:
        gdb.write('No symbol "%s" in global context.\n' % str(name))
            
def find_context_local(name, pcval, frame):
    try:
        node = gdb.lookup_symbol(str(name), block)
        do_dot(node, frame)
    except:
        gdb.write('No symbol "%s" in local context.\n' % str(name))

scope_global = object()
scope_local = object()
scope_frame_current = object()
scope_context_global = object()
scope_context_local = object()

things = {
    scope_global: find_global,
    scope_local: find_local,
    scope_frame_current: find_frame_current,
    scope_context_global: find_context_global,
    scope_context_local: find_context_local
}

class Tree(gdb.Command):

    def __init__(self):
        super(Tree, self).__init__('tree', gdb.COMMAND_DATA, gdb.COMPLETE_SYMBOL, False)

    def do_invoke(self, name):
        pcval = pc(name)
        if pcval is None:
            gdb.write('Could not find "%s": ' % str(name))
            not_running()
            return
        frame = gdb.selected_frame ()
        gdb.write('Finding "%s"\n' % str(name))
        if things[scope_local](name, pcval, frame) is False:
            if things[scope_global](name, pcval, frame) is False:
                if things[scope_frame_current](name, pcval, frame) is False:
                    if things[scope_context_local](name, pcval, frame) is False:
                        if things[scope_context_global](name, pcval, frame) is False:
                            return False
        return True
        
    def invoke(self, argument, from_tty):
        args = argument.split()
        if len(args)< 1:
            return
        for arg in args[0:]:
            self.do_invoke(arg)

Tree()
