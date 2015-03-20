import pyethereum
from random import randrange, random

from helper import *

u = pyethereum.utils
t = pyethereum.tester

from pyethereum.blocks import BLOCK_REWARD

# TODO get, test the changer.

s, c = None, None  # State and contract
specials = [None, None, None]
members, proposals = None, None

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
    specials = [int(t.a0, 16), int(t.a0, 16), 0]
    check()

def check():
    assert c.changer() == specials[0]
    assert c.implementer() == specials[1]
    assert c,boardadd() == specials[2]

    assert c.member_cnt() == len(members)
    assert c.proposal_cnt() == len(proposals)

def scenario_init():
    specials = [int(t.a1,16), int(t.a1,16), int(t.a2,15)]
    c.changer_change(specials)
    check()

def add_member(add=None):
    k, a = kp()
    add = add or a + ADDR_PART*randrange(2**256/ADDR_PART)
    c.boardadd_add_member(a, sender=specials[2])
    members.append((add, None,None) if add else (add, k, a))

def add_proposal(body=None):
    body = body or map(randrange(2**256), range(randrange(1, 5)))
    c.add_proposal(body, sender=anykey())
    proposals.append((0, body, {}))

def vote_for(with_index=None, member_i=None, proposal_2i=None):
    member_i = member_i or randrange(len(members))
    proposal_2i = proposal_2i or randrange(2*len(proposals))
    info, k, a = members[member_i]
    if (with_index == None):
        with_index = (random() < 0.5)
    if with_index:  # Specified index.
        c.vote_for_i(member_i, proposal_2i, sender=a)
    else: # Implied index.
        c.vote_for(proposal_2i, sender=a)
    info, body, votes = proposals[proposal_2i/2]
    votes[proposal_2i] = True
    proposals[proposal_2i/2] = (info + HALFWAY*(proposal_2i%2), body, votes)
