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

def reset():
    global c, s, end_time
    s = t.state()
    c = s.abi_contract('assurance_ent.se', t.k0)

def check(a, n):
    assert c.balance() == a
    assert c.cnt() == n

    # Check it isnt overwriting permanents
    assert hex(c.creator())[2:-1] == t.a0
    assert hex(c.recipient())[2:-1] == t.a0
    assert c.endtime() == end_time
    assert c.min() == 20000
    assert c.max() == 30000

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
    assert c.initialize(t.a2, t.a2, s.block.timestamp  + 600, 24000, 30000, \
                        sender=any_key(t.k0)) == \
        i("not creator")

befores = None

def scenario_init():
    global end_time, befores
    befores = {}
    if s is None:
        reset()
    end_time = s.block.timestamp  + 200
    check_blank()
    assert c.initialize(t.a0, t.a0, end_time, 20000, 30000) == i("initialized")
    check(0, 0)

def pay(k, a, must_be_paid):
    global befores
    sender = any_key()
#    addr = int("0x" + u.privtoaddr(sender), 16) # hrmm keyerror?
#    befores[addr] = befores[addr] or s.block.get_balance(addr)
    
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
    check(0,0)
    n, a  = randrange(10), 0
    for j in range(n):  # Pay, but dont reach.
        ca = randrange(19999/n)
        pay(0, ca, True)
        a += ca
        check(a, j + 1)
    return a, n

def check_refund():
    check_blank()
# TODO ... yeah it is important to check the ethers arrive.
#    for addr in t.accounts: #... they're paying for gas too.
#        if addr != t.a0:
#            assert s.block.balance(addr) == befores[addr]

def scenario_underfunded():
    a, n = scenario_dont_reach()
    while s.block.timestamp < end_time:  # Reach the time.
        s.mine()
    check(a, n)
    assert c.finish(sender=any_key()) == i("underfunded")
    check_refund()

def scenario_funded(over=False):
    a,n = scenario_dont_reach()
    m = 0
    # Go to threshhold, or over if specified.
    while c.balance() < c.min() or (over and m < 3):
        ca = randrange(5000)
        if pay(0, ca, c.balance() >= c.min()):
            m += 1
        else:
            a += ca
            n += 1
            check(a,n)

    while s.block.timestamp < end_time:  # Reach the time.
        s.mine()
    check(a, n)
    assert c.finish(sender=any_key()) == i("funded")
    assert c.funded() == 1
    assert c.balance() == 0
    assert c.pay_i(0, sender=any_key(), value=randrange(25363)) == i("already funded")
    assert c.balance() == 0

def scenario_refunded():
    a, n = scenario_dont_reach()
    assert c.refund(sender=t.k0) == i("manual refund")
    check_refund()

scenario_underfunded()
scenario_funded(True)

s = None
scenario_refunded()
scenario_funded(True)
