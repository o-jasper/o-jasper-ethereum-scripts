import pyethereum
from random import randrange, random

from helper import *

u = pyethereum.utils
t = pyethereum.tester

from pyethereum.blocks import BLOCK_REWARD

def kp(i=None):
    k,a = insecure_keypair(i)
    s.send(t.k0, a, 10**14)
    return k,a

# TODO get, test the changer.

s, c = (None, None)   # State and contract
specials = [None, None, None]
members, proposals = None, None

P16 = 2**16
P64 = 2**64
ADDR_PART = 2**160

def reset():
    global c, s, end_time
    global specials, members, proposals
    print("creating")
    if s is None:
        s = t.state()
    before_gas = s.block.gas_used
    c = s.abi_contract('board.se', t.k0)
    print('cga', s.block.gas_used - before_gas, s.block.gas_used, before_gas)
    members, proposals = [], []
    specials = [int(t.a0, 16), 0, int(t.a0, 16)]
    check()

def check(no_remove=True):
    assert c.changer() == specials[0]
    assert c.implementer() == specials[1]
    assert c,boardadd() == specials[2]

    assert c.member_cnt() == len(members)  # Check counts of members/votes
    if no_remove:  # While no-one was removed.
        assert c.member_i() == len(members)
    assert c.proposal_cnt() == len(proposals)
    # Checks the members.
    for i in range(len(members)):
        val, _,a = members[i]
        got = antineg(c.member(i))
        assert got == val, (got, val)
        if a:
            assert got % ADDR_PART == int(a,16)
    # Checks the proposals.
    for i in range(len(proposals)):
        info, body, f,a = proposals[i]
        assert antineg(c.proposal_info(i)) == info, (antineg(c.proposal_info(i)), info)
        assert c.proposal_body_len(i) == len(body), (c.proposal_body_len(i), len(body))
        assert info % P16 == len(body)

def scenario_init():
    global specials
    reset()
    c.changer_change([0,0,0], sender=t.k1)  # Shouldnt do anything; no rights.
    check()
    for _ in range(randrange(1, 4)):
        add_member()  # Should just work.(should use t,k0) 
    for _ in range(randrange(1, 4)): #(doesnt care about special positions)
        add_proposal()

    specials = [int(t.a1,16), int(t.a1,16), int(t.a2,16)]
    c.changer_change(specials, sender=t.k0)
    check()

def add_member(add=None):
    k, a = (None,None) if add else kp()
    add = add or int(a, 16) + ADDR_PART*randrange((2**256)/ADDR_PART)
    members.append((add, k, a))
    c.boardadd_add_member(add, sender=priv_of(specials[2]))        

def add_proposal(body=None):
    body = body or map(lambda(_): randrange(2**256), range(randrange(1, 5)))
    c.add_proposal(body, sender=any_key())
    proposals.append((len(body), body, {}, {}))

def vote_for(with_index=None, member_i=None, proposal_i=None, pro=None, to=None):
    if pro == None:
        pro = (random() < 0.5)
    if to == None:
        to  = (random() < 0.5)
    proposal_i = proposal_i or randrange(len(proposals))
    
    member_i = member_i or randrange(len(members))
    proposal_4i = 4*proposal_i + (1 if pro else 0) + (2 if to else 0)
    info, k, a = members[member_i]

    if (with_index == None): # Shouldnt matter if index used.
        with_index = (random() < 0.5)
    if with_index:  # Specified index.
        c.vote_i(member_i, proposal_4i, sender=k)
    else: # Implied index.
        c.vote(proposal_4i, sender=k)

    info, body, fo,ag = proposals[proposal_4i/4]
    # If changed.. 
    if to != (fo if pro else ag).get(member_i, False):
        (fo if pro else ag)[member_i] = to  # Remember..
        # Add /substract.
        info += P16*(+P64 if pro else -P64)
    
    proposals[proposal_4i/4] = (info, body, fo,ag)

def scenario_addmembers():
    scenario_init()
    for _ in range(randrange(1, 4)):
        add_member()  # Should just work.(should use t,k1 now)
    check()

def scenario_add_proposal():
    scenario_addmembers()
    for _ in range(randrange(1, 4)):
        add_proposal()
    check()

def scenario_vote():
    scenario_add_proposal()
    for _ in range(randrange(1,6)):
        vote_for()
    check()

scenario_vote()
