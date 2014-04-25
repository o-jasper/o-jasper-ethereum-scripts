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

## Example: [escrow](https://github.com/jorisbontje/cll-sim/blob/master/examples/escrow.cll)
Note that is pre-serpent code, and this is an informal example.

<TODO>
