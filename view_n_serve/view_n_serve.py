#TODO
# * Figure how to deal with block.number, block.basefee
# * check monetary ammounts.
# * Figure out if there are measure against anti-replay. In which case this is
#   just for the hell of it, and one needs to be written that checks a signature
#   itself.

from math import floor,ceil
from random import random
from sim import Contract, Simulation, Tx, stop,mktx,Block

#Everything is sent pretending to be viewer, the packet is
# just provided to the server. (TODO see above)
#
#In that case the contract would have to check signatures itself.
VIEWER="viewer"
SERVER="server"

STARTFEE = 200;
ATTEMPT_CNT = 200;

CMD_PUNISH="PUNISH"
CMD_REDEEM="REDEEM"

DESTRUCTION_ADDR = "destructo"

DIFFICULTY =0.5; #Controls 

class ViewNServe(Contract):
    """Viewing and serving to viewer"""
    def run(self, tx, contract, block):
        if tx.value < block.basefee * STARTFEE:
            stop("Insufficient fee")
        if tx.datan == 0 or tx.sender != VIEWER :
            stop("Fill tank")
        from_block = tx.data[1] #Must be in attempt range
        to_block   = tx.data[1] + ATTEMPT_CNT
        if block.number < from_block or block.number > to_block :
            stop("Outside period")
        # Messages here are actually sent by server, punish command is also requesting
        #  command for viewer.
        command = tx.data[0]
        if command == CMD_PUNISH :
            if 2*tx.value > tx.data[3] :
                stop("Over punish")
            mktx(DESTRUCTION_ADDR,2*tx.value, 0,[])
            stop("Punish")
        #Note, the server predicts if it loses and doesnt bother, of course.
        if command == CMD_REDEEM :
            if block.parenthash < DIFFICULTY : 
                stop("Lost lottery")
            mktx(tx.data[2], tx.data[3], 0,[])
            stop("Got reward")

#TODO 
block_num=0

def anyone() : #Anyone, or happens to be viewer.
    if random() < 0.5 :
        return 'anyone'
    else :
        return VIEWER
def insufficient_fee_value() : #Value < STARTFEE*block.basefee
    return 0
#    return floor(max(0,(STARTFEE-1)*random()))
def sufficient_fee_value() :  #Value > STARTFEE*block.basefee
    return ceil(STARTFEE*(1+random()))
def maybe_data() :
    if random() < 0.5 :
        return [random(),random()]
    else :
        return []

class ViewNServeRun(Simulation):

    contract = ViewNServe()
    
    def test_insufficient_fee(self) :
        tx = Tx(sender=anyone(),
                value= insufficient_fee_value(), data=maybe_data())
        self.run(tx, self.contract)
        assert self.stopped == 'Insufficient fee'

   #Includes others trying to meddle without having a transaction from VIEWER
    def test_fill(self) :
        tx = Tx(sender='others', value= sufficient_fee_value(),
                data= maybe_data())
        self.run(tx, self.contract)
        assert self.stopped == 'Fill tank'

    def test_fill_self(self) : #Of course if random data is added here, there is an issue.
        tx = Tx(sender=VIEWER, value= sufficient_fee_value())
        self.run(tx,self.contract)
        assert self.stopped == 'Fill tank'

   #Again, all these intended to send by server.
    def test_outside_period(self) :
        contract = self.contract
        tx = Tx(sender=VIEWER, value= sufficient_fee_value(),
                data=[random(),
                      block_num-ceil(ATTEMPT_CNT*(1+random())),random()])
        self.run(tx,contract)
        assert self.stopped == 'Outside period'
        
    def test_punish(self) :
        contract = self.contract
        x= 4*sufficient_fee_value()
        tx = Tx(sender=VIEWER, value= x,
                data=[CMD_PUNISH,block_num,
                      8*sufficient_fee_value(),8*x])
        self.run(tx,contract)
        assert self.stopped == 'Punish'
        
    def test_over_punish(self) :
        x = sufficient_fee_value()
        contract = self.contract
        tx = Tx(sender=VIEWER, value= x,
                data=[CMD_PUNISH,block_num,sufficient_fee_value(),x])
        self.run(tx,contract)
        assert self.stopped == 'Over punish'

    def test_claim_reward(self,parenthash = random()) :
        contract = self.contract
        tx = Tx(sender=VIEWER, value= sufficient_fee_value(),
                data=[CMD_REDEEM,block_num,8*sufficient_fee_value(),8*sufficient_fee_value()])
        self.run(tx,contract,Block(parenthash=parenthash))
        
        if parenthash < DIFFICULTY :
            assert self.stopped == 'Lost lottery'
        else :
            assert self.stopped == 'Got reward'
