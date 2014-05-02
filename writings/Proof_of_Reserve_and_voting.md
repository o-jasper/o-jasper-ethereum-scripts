# Proof of Reserve and voting

Say you have a DAO, like a 'corporation' with stocks, a co-op, or
full-on democracy. Now you have a vote.. Now suddenly, millions of
people have to do a transaction?!

The voting transactions would essentially be signed statements of which way
people vote. If there is a way to create a single statement that compresses
all those signed statements into a single statement?

A while ago, Kraken used a 
<a href="https://www.kraken.com/security/audit">Proof of reserve</a>,
to increase trust that it held the bitcoins it requires. Essentially,
each person knows his balance, asking for the proof, he gets a Merkle path,
instead of each node of the path having just the checksum of the other branch,
it also has an amount.

For votes you can count yes(1)/no(0), and do the same. Problem is that
cannot prove that people either didnt vote, or did vote, but the counter cheated
by not including it in the total.

A possible solution is to try make the collection method more trustworth. 
Perhaps there is a way of using multiple collectors, yet counting each vote 
only once? Each collector would itself sign statements of no-shows, and they
would also compare their tallies, noting double shows.

## What can contracts do

Essentially the idea is that the vote is tallied, the root hash and amount
put in a contract on the blockchain.

People challenge the vote, getting the Merkle paths. If the counter fails to
deliver, or doesnt deliver correct paths, you present the challenge to the
contract. At the beginning the counter put stake into the contract, that is at
risk if he does not satisfy the challenge.

If such a challenge succeeds, the stake is taken from the challenger somehow.
(could be a reward for it, but careful against corruption..) The decision may
be reverted, or modified, or re-voted depending on the case.

If a vote is written down as a 'double show', this can also be challenged. 

## Truth or Punish

I would categorize this as 'Truth or Punish'. As opposed to the
'Truth or Invalid' approach of regular the blockchain. 
I think you could even based a <a href="https://forum.ethereum.org/discussion/comment/3924/#Comment_3924">merged mining blockchain</a> 
on this idea.

But 'Truth or Invalid' is better; there is a inherent weakness/limitation
in that the profit of cheating must not exceed the price of the punishment.
(that includes 'profit' in terms of a party that benefits from trying to
hurt parties behind the contract)

## Idea incomplete

As said, 'Truth or Invalid' is better. Also the 'no-show' or 'no-incorporate'
isnt solved either, although it doesnt seem unlikely there is a way to use
multiple collectors. 

Besides that, i wouldnt rule out completely different solutions!
