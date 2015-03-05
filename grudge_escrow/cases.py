## TODO make it abi_contract, and fix everything up for it being that.

import pyethereum, random
t = pyethereum.tester

from random import randrange

def i(str):
    s,f = 0, 1
    for i in range(len(str)):
        s += f*ord(str[len(str)-i-1])
        f *= 256
    for i in range(32 - len(str)): # Right pad instead of left.
        s *= 256;
    return s

def stri(i):
    s = []
    while i > 0:
        s += chr(i%256)
        i /=256
    return "".join(reversed(s))

s = t.state()
c = s.abi_contract('grudge-escrow.se', t.k0)

def reset(a):
    global c,s
    s = t.state()
    c = s.abi_contract('grudge-escrow.se', t.k0, a)

def check(a, ready=False, customer=False):
    0
#    assert s.block.get_balance(c) == a
#    if not ready:
#        assert s.block.get_storage_data(c, 0x20) == 0
#        assert s.block.get_storage_data(c, 0x40) == 0
#    if customer:
#        assert hex(s.block.get_storage_data(c, 0x60))[2:-1] == customer
#    else:
#        assert s.block.get_storage_data(c, 0x60) == 0
    # Check it isnt overwriting permanents
#    assert hex(s.block.get_storage_data(c, 0x00))[2:-1] == t.a0

def random_addr(disallow=None):
    if not disallow:
        disallow = []
    elif not isinstance(disallow, list):
        disallow = [disallow]
    i = randrange(len(t.keys) - len(disallow))
    while t.keys[i] in disallow:
        i += 1
    assert i < len(t.keys)
    return t.keys[i]

def scenario_insufficient(r=True, a=1000):
    if r: reset(1000)

    assert c.buy(value=randrange(2343), sender=random_addr()) == i("no offer yet")
    
    check(a if r else 0)
    assert c.change_deal(2000, 1000, value=(0 if r else a), sender=t.k0) == i("price changed")
#    assert s.block.get_storage_data(c, 0x20) == 3000
#    assert s.block.get_storage_data(c, 0x40) == 1000
#    assert s.block.get_storage_data(c, 0x60) == 0
    assert c.buy(value=2500, sender=random_addr()) == i("too early")

    s.mine(100) #, random_addr())
    
    check(a, True)

    assert c.buy(value=2500, sender=random_addr()) == i("insufficient") 
    check(a, True)

def scenario_sufficient(r=True, a=1000):
    scenario_insufficient(r)
    check(a, True)

    assert c.buy(sender=t.k2, value=3000) == i("bought")
    check(a + 3000, True, t.a2)

    assert c.release(sender=t.k4, value=3) == i("stranger")  # Guy meddling.
    check(a + 3000, True, t.a2)

    assert c.release(sender=t.k2) == i("released")
    check(0)

scenario_sufficient()
#assert s.send(t.k8, c, 0, [7000, 500])  # Meddling.
# check(0)

scenario_sufficient(False) # Tests reviving.
