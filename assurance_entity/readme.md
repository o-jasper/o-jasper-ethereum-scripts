**NOTE** still needs more porting to PoC8, particularly, the web stuff.

# Assurance Ethereum entity. 

Assurance Ethereum entity.

* Creator creates, then initiates, sets it up, sets recipient, sets block
  number it will have to succeed/fail, sets minimum success amount.

* Anyone can help fund.

* Before deadline, creator can refund.

* Anything occuring after the deadline sends the funds to the project if
  success, and refunds otherwise.

### Potential expansions
Some of these might be doable by simply connecting to other contracts. But
that might not be gas-efficient.

* Stages; if funded, it goes to stage 1, stage 2 needs something to be
  triggered. That might mean more funding, votes from existing funders or
  just keeping the same funding, but allowing some funders to cut their losses
  if they lose faith.
  
  There could be multiple stages this way.

* Dividents: paying for stuff like stocks. Need some rules about how much to do 
  dividents. 
  
  Not *particularly* happy with use of stocks currently, but then
  oculus-like events suck too.

## Tests
Just one that does a case test. 

Do **not** think it has high enough certainty for use. 

It is bound to need quite a lot of rewriting towards better contract writing.
Like formalizing the commands, efficiency, getting rid of the `refund` variable
being used as it is now..

Otherwise for security, need to try think of ways to break it, analyse the code,
and throw more random stuff at it in tests.

# TODO (note: only if i take it further)

* Go PoC7..
  + Get rid of that awful `refund` variable doing control flow.
  + Some static checks.

* Ensure cant attack by making many tiny contributions, *later* costing too much gas.
  (contribution minimum)

* The refund button should hide if you cannot control it. Also, refunding after the
  whole thing.

* More thurrough case test.
  + All logical paths.
  + Fuzz-test?
  + Reading well/annotating?

* It is not pretty enough.

* Show everything, and safety-off switch. NOTE: the safeties are merely some extra
  checks, do not imply safety.

* Paying and refunding uses same interface, renaming stuff.. I dont like it.
