
Idea inspired on [gittip](http://gittip.com/) due to Chad Whitacre.

## GitBitTip script on sender side
`gitbitip_from_sender_1.cll`is a perspective from the sender. Before anything
is changed with the script, the pledged time&times;payout is *always* sent.
There is no way around it.
(But receivers may want to poke so they dont have to wait)

Anyone can put coin in, no point in restricting. Receivers can be any address,
including other scripts.

The owner of the script can extract coin and change the list, but only after the
pledged is sent.

The other one, `gitbitip_from_sender.cll` uses `3+recipient_cnt` data entries, is
more complicated, requires all receivers to get the same ammounts.

## (non)Issues:
**Overzealous pokers raking up transaction fees?** Nope, they should just have
to pay whatever transaction fees. (**TODO** how to ensure fees sufficient?)

**Small ammounts**: maybe could be dealt with better. But again, transaction
fees have to be paid by anyone poking it before anything is sent. 

**Only remove/add one at a time?** This is probably not efficient enough?
**TODO** Think it is better to be able to add a list of addresses, remove a 
list of indexes.

(I do not claim to have all the issues!)

## Other ways?
Afaict all of these are more complex.

**GitBitTip script on receiver side**: Basically have the receiver set up the
script, and the script keeps track of the balances donors can still extract.

**GitBitTip as DAO**: like a monolithic scripts many people can use. Not sure if
useful, but something to look at.

**Judged-donation slow release**: Basically a way to donate with assurance that
a set of judges judge the donation to go to the right cause. I think its a 
different concept. It is interesting in that single donors cant back off, only
the judges can return the ether.

## TODO: 
* Use `contract.storage` elements to 
* Test the darned thing.
* Need proper fee value.
