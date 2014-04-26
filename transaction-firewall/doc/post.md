Idea is to classify the effects of an action. That may be wether or not the
effects warrant human intervention, require note in a log, or generally the
'severity' of the effect, or it may be a bug.

The classifiers can be placed as such:

<img src="tx-firewall.png">

The input could be random data, and the whole thing 'mere' simulation for the
purpose of testing. Everything could be a simulation so the user knows which
classifiers where triggered.

The input classifier(`I`), program(`P`) pair is already a test, of just `P`.

The `I`, output-classifier(`O`) tests the contract(`C`). Of course things may be
incorrect output for `P`, but still be something that has to pass the test of
`O`, however, the things `I` decides still affect `O`.

`I` itself is potentially affected by `C`

So how do we classify, in a way that is very clear? Firstly, the classifiers
should have different levels of specificness, because if you go too specific,
you essentially reimplement the contract. Also, this allows people trying to
assess the `C` to start at the simpler promises of the classifiers. Also it
should clarify the logic.

## The approach

The approach is to have statements that gather data into variables. Firstly,
the transaction and contract information. Then in the second stage, 
transactions information from the contract, and post-run contract info.

This information is put together into boolean logic statements, each with a
name, which classify, by the statements being true/false.

Under each name, a new set of potential classifications are possible, and
the process is repeated.

## Example to illustrate: [escrow](https://github.com/jorisbontje/cll-sim/blob/master/examples/escrow.cll)
Note that is pre-serpent code!

#### Input firewall
We will write down the test in code essentially. However, the intention for 
execution is that `bug` and `note` infact just log the information, not
terminating.

    def input_firewall(tx, promise, contract):
       
        fee = 100*block.basefee
        state = contract.storage[1000]
        
        if tx.value < fee:  # (Obsolete due to gas, of course!)
            bug("Not enough for fee")
            
        if tx.value > fee and not promise.what == PAYING:
            bug(In excess of fee")
        
        if promise.to_address != contract.address:
            bug("Sending to wrong address")

        if promise.to_name != contract_name(contract.address):
            bug("Name suddenly changed?!")

        if promise.what == PAYING:
            if state != 1:
                bug("Contract not in buying stage")
            
            if contract.PRICE != promise.price:
                bug("Disagreement on price")
            
            if tx.value > contract.PRICE:
                bug("Paying more than you need too")
            if tx.value < contract.PRICE:
                bug("Not paying enough")
            
            if not own(tx.sender):  # Refunds would end up in wrong place.
                bug("Dont own that address")

        elif promise.what == VERIFYING:
            if tx.sender == contract.VERIFIER:
                bug("Only verifier can verify!")
                if own(contract.VERIFIER):
                    note("You do own the verifier address, but not being used")

        elif promise.what == REFUND:  # Poking for refund.
            if state != 1:
                bug("It is not in the verifying/refund state!")

            if state == 1 and block.timestamp <= 30 * 86400 + contract.storage[1003]:
                bug("Its too early for a refund")

If you look at the code, note that you could follow any branch of logic
separately, they're not interconnected. Which is fortunate, because this
check for transactions going into the contract is longer than the contract
itself.

It should not be seen as python code, but as pseudocode representing the
below graph:

**TODO GRAPH**

Quite a few of the clauses could imply lost money if violated. The contract
doesnt support getting more out than was intended to be paid. Essentially 
this means ether can only be stolen by messing up `tx.to_address`
(a wrong `tx.sender` cant actually be done because you cant sign
transactions coming from senders whoms' privkeys you do not have)

`tx.to_address` is maybe one of the hardest to check, as the program can fake
its promise aswel as the address the transaction sends too. I imagine ethereum
could add a toplevel naming system, and `contract_name(address)` returns 
the name. This can be checked with `promise.to_name` and the promised name 
featured prominently in the GUI.(or whatever)


#### 

## Fuzz testing note

One thing about fuzz testing is that it can be hard to find realistic
test cases, that find corner cases. It is in principle possible to take the
states of instances of the contract on the blockchain, and transactions to them,
and subject those to random variations and test with those cas
