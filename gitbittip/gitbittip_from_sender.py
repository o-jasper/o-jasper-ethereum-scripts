from sim import Contract, Simulation, Tx, stop,mktx,Block
from random import randint, random

#Constants
BASE_FEES    = 400
INITIAL_USER = 0
DIV          = 1024

# State data.
I_USER            = 1000
I_LAST_PAYOUT     = 1001
I_FIRST_RECIPIENT = 10000
# Commands:
C_EXTRACT          = 1
C_CHANGE_RECIPIENT = 3  # Change or set recipient, or change wage.
C_CHANGE_USER      = 4

class GitBitTip(Contract):
    def run(self, tx, contract, block):
        if tx.value < block.basefee*BASE_FEES:
            stop

        duration = block.timestamp - contact.storage[I_LAST_PAYOUT]
        contract.storage[I_LAST_PAYOUT] = block.timestamp

        i = I_FIRST_RECIPIENT # First listed first served.
        while contract.storage[i] != 0:
            mktx(contract.storage[I_FIRST_RECIPIENT + i],
                 (contract.storage[I_FIRST_RECIPIENT + i+1]*duration)/DIV, 0, [])
            i = i + 2
        
        user = contract.storage[I_USER]
        if tx.sender != user or (user == 0 and tx.sender == INITIAL_USER):
            stop("Denied")
        
        if tx.data[0] == C_EXTRACT:
            mktx(tx.data[1], tx.data[2], 0, [])
            stop("Extracted")
        if tx.data[0] == C_CHANGE_RECIPIENT:
            i = I_FIRST_RECIPIENT + 2*tx.data[1]
            contract.storage[i]   = tx.data[2]
            contract.storage[i+1] = tx.data[3]
            stop("Recipient changed/added")
        if tx.data[0] == C_CHANGE_USER:
            contract.storage[I_USER] = tx.data[1]
            stop("User changed")

class GitBitTipState:
    last_payout = 0
    user       = INITIAL_USER
    recipients = {}
    txs = []

    def assert_state(self, contract):
        I_USER            = 1000
        I_LAST_PAYOUT     = 1001
        I_FIRST_RECIPIENT = 10000

        assert contract.storage[I_LAST_PAYOUT] == last_payout
        assert user == (INITIAL_USER if contract.storage[I_USER] == 0 else contract.storage[I_USER])
        i = 0 
        while i < len(contract.txs):
            assert contract.txs[i][0] == self.txs[i][0]
            assert contract.txs[i][1] == self.txs[i][1]
            i += 1
        for i in self.recipients:
            assert self.recipients[i][0] == contract.storage[i + 0]
            assert self.recipients[i][1] == contract.storage[i + 1]


class Poke:
    def __init__(self, user, time):
        self.user = user
        self.time = time
    
    def run(self, state):
        duration = self.time - state.last_payout
        i = 0
        while i in state.recipients:
            state.txs.append((state.recipients[i][1], (state.recipients[i][2]*duration)/DIV))
            i + 1
        state.last_payout = self.time

    def tx(self):
        return Tx(sender=self.user, value=BASE_FEES)
    def block(self):
        return Block(timestamp=self.time)
    
class Extract:
    def __init__(self, user, time, to, value):
        self.user = user
        self.time = time
        self.to = to
        self.value = value
        
    def run(self, state):
        state.poke(self.time)
        if self.user == state.user:
            state.txs.append((self.to,self.value))

    def tx(self):
        return Tx(sender=self.user, value=BASE_FEES,
                  data=[C_EXTRACT, self.to, self.value])
    def block(self):
        return Block(timestamp=self.time)
    
class ChangeRecipient:
    def __init__(self, user, time, i, to, wage):
        self.user = user
        self.time = time
        self.i = i
        self.to = to
        self.wage = wage

    def run(self, state):
        state.poke(self.time)
        if self.user == state.user:
            state.recipients[i] = (self.to, self.wage)

    def tx(self):
        return Tx(sender=self.user, value=BASE_FEES,
                  data=[C_CHANGE_RECIPIENT, self.i, self.to, self.wage])
    def block(self):
        return Block(timestamp=self.time)

class ChangeUser:
    def __init__(self, user, time, to_user):
        self.user = user
        self.time = time
        self.to_user = to_user
        
    def run(self, state):
        state.poke(time)
        if self.user == state.user:
            state.user = self.to_user
    
    def tx(self):
        return Tx(sender=self.user, value=BASE_FEES,
                  data=[C_CHANGE_USER, self.to_user])
    def block(self):
        return Block(timestamp=self.time)


def random_command(time, user_cnt=3, recipient_cnt=16, r = randint(1,4)):
    user = randint(1,user_cnt)
    if   r == 1:
        return Poke(user, time)
    elif r == 2:
        return Extract(user, time, randint(1, recipient_cnt), random())
    elif r == 3:
        return ChangeRecipient(user, time, randint(1, recipient_cnt),
                               randint(1, user_cnt), random())
    elif r == 4:
        return ChangeUser(user, time, randint(1, user_cnt))

# To end the script, simply extract everything and let it die.
class GitBitTipRun(Simulation):

    #Run a command and assert the correct state.
    def run_assert(self, contract, state, command):
        command.run(state)
        self.run(command.tx(), contract, command.block())
        state.assert_state(contract)
    
    def test_sequence(self, n=100):
        contract = GitBitTip()
        state    = GitBitTipState()
        time=0
        i=0
        while i < n:
            time += random()
            i += 1
            self.run_assert(contract, state, random_command(time))
