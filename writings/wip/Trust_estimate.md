# Trust estimates, escrow, and stake

## Escrow by different probability estimates

Alice and Bob want to do a deal, Bob provides a service to Carol for a price
`X`, if it succeeds Bob gets a value `V`. They trust the deal will go through
with a probability `q`.

<blockquote>
    alice = X<br>
    av(bob) = qV - X &ge; 0
</blockquote>
Which goes through if `q &ge; X/V`

Now, Carol has `p'` trust in that deal, she has the option to ask `S`
from the transaction, if is succeeds but to pay `F` if it fails.

<blockquote>
    av(carol) = p'S - (1-p')F = p'(S+F) - F &ge; W<br>
    av(bob)   = q(V - X - S) + (1-q)(F-X) = q(V - S - F) + F - X &ge; 0
</blockquote>
So

<blockquote>
    F/p = (W+F)/p' &le; S+F &le; (F-X)/q + V
</blockquote>

Where `p = p'F/(W+F)` is an effective probability that is the probability if
Carol were to hide her profit motive. The following has to be satisfied for it
to go through:
<blockquote>
    p &ge; F/(S+F)<br>
    q &le; (F-X)/(S+F-V)
</blockquote>

## Many Carols
Lets say there are 'many Carols' coming by. The best deal is from the
Carol that has the highest probability, she will be able to demand the
smallest payment. Perhaps however, she doesnt have enough money, or
doesnt want to risk at those probabilities that much money.
(utility is not linear with amount)

So essentially the Carols are ordered by decreasing trust and provide 
until the need for sum of `F` over them all is satisfied.

If we assume we have the comprehensive list of Carols, the 'best' Carol
knows she is and thus can ask either the minimum of the next
Carol in line, or the maximum Alice will accept.

## Probabilities and trust
The reasons Alice and Bob have probability `q`, and the reasons Carol
has `p` another one are their estimates. These estimates include trust.

Both sides have the estimate `p`,`q`, according to their opinion;

    1 - P(False_report &cup; Bob_fails  &cup; Bob_not_trustworthy)
    
    = 1 - P(False_report) - P(Bob_failse) - P(Bob_not_trustworthy) + 

Trust also implies stake. After all the trust can be lowered if the deal
fails. 

