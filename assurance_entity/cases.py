import pyethereum
from random import randrange
u = pyethereum.utils
t = pyethereum.tester

def i(str):
    s,f = 0, 1
    for j in range(len(str)):
        s += f*ord(str[len(str)-j-1])
        f *= 256
    for j in range(32 - len(str)): # Right pad instead of left.
        s *= 256;
    return s

def stri(j):
    s=""
    while j > 0:
        s += chr(j%256)
        j /=256
    return "".join(reversed(s))

def any_key(disallow=None):
    if not disallow:
        disallow = []
    elif not isinstance(disallow, list):
        disallow = [disallow]
    i = randrange(len(t.keys) - len(disallow))
    while t.keys[i] in disallow:
        i += 1
    assert i < len(t.keys)
    return t.keys[i]

s = None
c = None

minv = 2*10**12
maxv = 3*10**12
duration = 200

def reset():
    global c, s, end_time
    print("creating")
    if s is None:
        s = t.state()
    c = s.abi_contract('assurance_ent.se', t.k0)

def check(a, n):
    assert c.balance() == a
    assert c.cnt() == n

    # Check it isnt overwriting permanents
    assert hex(c.creator())[2:-1] == t.a0
    assert hex(c.recipient())[2:-1] == t.a0
    assert c.endtime() == end_time
    assert c.min() == minv
    assert c.max() == maxv

    assert c.refund(sender=any_key(t.k0)) == i("only creator/self")
    assert c.initialize(t.a2, t.a2, s.block.timestamp  + 600, 24000, 30000) == \
           i("already initialized")

def check_blank():
    assert c.balance() == 0
    assert c.recipient() == 0
    assert c.endtime() == 0
    assert c.min() == 0
    assert c.max() == 0
    assert c.cnt() == 0
    assert hex(c.creator())[2:-1] == t.a0
    assert c.pay_i(0, sender=t.k0, value=randrange(46364)) == i("not ready")
    assert c.initialize(t.a2, t.a2, s.block.timestamp  + 600, randrange(minv), maxv+3, \
                        sender=any_key(t.k0)) == i("not creator")

befores = None

def scenario_init():
    global end_time, befores
    if c is None:
        reset()
    befores = {}
    for addr in t.accounts:
        befores[addr] = s.block.get_balance(addr)
    print("scenario: init")        
    end_time = s.block.timestamp  + duration
    check_blank()
    befores[t.a0] = s.block.get_balance(t.a0)
    assert c.initialize(t.a0, t.a0, end_time, minv, maxv) == i("initialized")
    check(0, 0)

def pay(k, a, must_be_paid):
    global befores
    sender = any_key()

    got =  c.pay_i(k, sender=sender, value=a)
    if got == i("index paid"):
        assert hex(c.fund_addr_i(k))[2:-1] == sender
        return False
    elif got == i("paid"):
        return False
    
    assert must_be_paid
    if k > 2**64:
        assert got == i("unrealistic")
    else:
        assert got == i("hit max") and c.balance() + a > c.max()
    return True

def scenario_dont_reach():
    scenario_init()
    print("scenario: dont_reach")    
    check(0,0)
    n, a  = randrange(10), 0
    for j in range(n):  # Pay, but dont reach.
        ca = randrange((minv-1)/n)
        pay(0, ca, True)
        a += ca
        check(a, j + 1)
    return a, n

def check_refund():
    check_blank()
    for addr in t.accounts: #... they're paying for gas too. Better if accounted for.
        if addr != t.a0:
            assert abs(s.block.get_balance(addr) - befores[addr]) < 10**6
    assert abs(s.block.get_balance(t.a0) - befores[t.a0]) < 10**6

def scenario_underfunded():
    a, n = scenario_dont_reach()
    print("scenario: underfunded")    
    while s.block.timestamp < end_time:  # Reach the time.
        s.mine()
    check(a, n)
    assert c.finish(sender=any_key()) == i("underfunded")
    check_refund()

def scenario_funded(over=False):
    a,n = scenario_dont_reach()
    print("scenario: funded")
    m = 0
    # Go to threshhold, or over if specified.
    while c.balance() < c.min() or (over and m < 3):
        ca = randrange(maxv/10)
        if pay(0, ca, c.balance() >= c.min()):
            m += 1
        else:
            a += ca
            n += 1
            check(a,n)

    while s.block.timestamp < end_time:  # Reach the time.
        s.mine()
    check(a, n)
    # Check funded stuff.
    assert c.finish(sender=any_key()) == i("funded")
    assert c.funded() == 1
    assert c.balance() == 0
    assert c.pay_i(0, sender=any_key(), value=randrange(25363)) == i("already funded")
    assert c.balance() == 0

    #sa = 0
    #for addr in t.accounts:
    #    sa += (befores[addr] - s.block.get_balance(addr))
    # TODO sum of this should be gas cost plus mining income.

def scenario_refunded():
    a, n = scenario_dont_reach()
    print("scenario: refunded")
    assert c.refund(sender=t.k0) == i("manual refund")
    check_refund()

c = None
#scenario_underfunded()
scenario_funded(True)
print('---') # Gotta have a new one, because old one kept in place if success.
c = None
scenario_refunded()
scenario_funded(True)
