curr = []
prev = []
diff = []
diff_curr = []
diff_curr2 = []
diff_prev = []
def rec(x, level = 0):
    i = ' ' * level
    for item, val in zip(x[::2], x[1::2]):
        if isinstance(val, list):
            print("%s%s = [" %(i,item))
            rec(val, level + 2)
            print("%s]" %(i))
        else:
            print("%s%s = %s" %(i, item, val))
def cmp(a1, b1, a2, b2, curr, first = False):
    if first == True:
      curr = []
      first = False
    if type(b1) != list or type(b2) != list:
      if type(b1) != list and type(b2) != list:
        if b1 == b2:
          if a1 is not None:
            curr.append(a1)
          else:
            curr.append(None)
          curr.append(b1)
        else:
          curr.append(None)
          curr.append(None)
      else:
        curr.append(None)
        curr.append(None)
    if type(b1) == list and type(b2) == list:
        if a1 is not None:
            curr.append(a1)
        tmp = []
        curr.append(tmp)
        ita = iter(b1)
        itb = iter(b2)
        for (x1, x2), (y1, y2) in zip(zip(ita, ita), zip(itb, itb)):
          curr = cmp(x1,x2,y1,y2, tmp)
    return curr
def dolist(list):
    global curr
    global prev
    if curr:
        prev = curr
    global diff_curr
    global diff_curr2
    global diff_prev
    if diff_curr:
        diff_prev = diff_curr
    curr = list
    print("curr = [")
    rec(curr, 2)
    print("]")
    print("prev = [")
    rec(prev, 2)
    print("]")
    if prev:
      diff_curr = cmp(None, curr, None, prev, diff_curr, True)
      print("diff_curr = [")
      rec(diff_curr, 2)
      print("]")
      print("diff_prev = [")
      rec(diff_prev, 2)
      print("]")
      if diff_prev:
        diff_curr2 = cmp(None, diff_curr, None, diff_prev, diff_curr, True)
        print("diff_curr2 = [")
        rec(diff_curr2, 2)
        print("]")
    print("curr = %s" % curr)
    print("prev = %s" % prev)
    print("dfc1 = %s" % diff_curr)
    print("dfp1 = %s" % diff_prev)
    print("dfc2 = %s" % diff_curr2)
dolist(['val1', '5', 'next', 'NULL', 'val2', '0', 'string', '0x555555554b44 "HI"'])
dolist(['val1', '20', 'next', 'NULL', 'val2', '0', 'string', '0x555555554b44 "HI"'])
dolist(['val1', '21', 'next', 'NULL', 'val2', '0', 'string', '0x555555554b44 "HI"'])
dolist(['val1', '22', 'next', 'NULL', 'val2', '0', 'string', '0x555555554b44 "HI"'])
dolist(['val1', '20', 'next', ['val1', '5', 'next', 'NULL', 'val2', '0', 'string', '0x555555554b44 "HI"'], 'val2', '0', 'string', '0x555q555554b44 "HI"'])
