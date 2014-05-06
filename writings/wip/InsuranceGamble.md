# Insurance is betting

Consider a bet where failure implies you get `F`(`<`) and success `S`(`>0`),
you think the probability of success is `p`.. You think the average is:

       Failure       Success    Average
         F             S          (1-p)F + pS = p(S-F) + F

Now there is someone willing to bet, he believes that the probability is
infact `q`. He offers compensation if it fails `C`, but he wants `&beta;C`
if it success
    
               Failure    Success        Average
         You     F+C        S-&beta;C      (1-p)(F+C) + p(S-&beta;C)  =  p(S-F-C(1+&beta;)) + F + C
       Gambler   -C         &beta;C        -(1-q)C + q&beta;C         =  qC(1+&beta;) - C

Now You will accept if you will do better than earlier;

        p(S-F-C(1+&beta;)) + F + C &ge; p(S-F) + F
     
        -pC(1+&beta;) + C &ge; 0
     
        &beta; &le; 1/p -1

So `S` and `F` dont matter! In general can add whatever you want and it
doesnt matter. It is just a bet? So why do just bet for stuff like insurance?

Three reasons come to mind:

1. Our utility(wellbeing) is not linear with the amount of money we own.
  `U(F)` and `U(S)` are much further apart than `F` and `S`. 
  But `U(F+C)` and `U(S-&beta;C)`.. Infact we can approximate;
    
       U(F+C) - U(S-&beta;C) &asymp; U'(F+C)(F + C - S + &beta;C)
    
  This aswel makes this calculation still work as the approximation is linear
  and the factor doesnt matter for the analysis. So the bet is in a sense a 
  side issue.

2. The mechanisms in which someone else bets that way indicates someone else has
  trust in -for instance- a vendor.

3. You are particularly aware of the risks and deals and their probability.

Of course, in the current world, insurers are often large institutions and their
many bets even out.

It can also be investment, where `C` is given beforehand.
This implies that it can be used as stake. After all, if a contract(like RANDAO)
requires ethers as stake, and a gambler trusts you would not lose that stake,
he can make a deal. If you fail, his belief in you will decrease; that would be
the thing that is at stake for you.

## The gambler side

The gambler, assume he wants some profit; `E`

       qC(1+&beta;) - C &ge; E;

       &beta; &ge; (E/C +1)/q -1

But then we notice that the profit motive shows itself as an apparent probability;
`q' = q/(E/C + 1)` as the gambler can change the two accordingly, there is
not point to the freedom; we choose `E=0` and note that probability is only
apparent.

A deal is possible if `1/p -1 &ge; &beta; &ge; (E/C +1)/q -1`.

## Many gamblers
From many gamblers, the best deal is from one with the highest
(Apparent)probability, he will be able to demand the smallest payment. Perhaps,
however, he doesnt have enough money, or doesnt want to risk at those probabilities
that much money. Here this would be again because of nonlinearity of utility, but
also because the probability of failure may be dependent on the amount.

If we assume we have the comprehensive list of gamblers, after a gambler is
depleted, you can go to the next one with a lower `q`.

We presumably can find these gamblers within a system in Ethereum. Mind that
finding them being possibly client-side massively increases the ability to
search without using gas. You put the key things that actually need to be
done by contracts in the transaction.

The user will often 'bet' by estimating what he wants to pay for what he gets.
For instance if this backs up the quality of a product the effective price
increase of the product is increased. This makes the choice easier, the gamblers
will simply ask their minimum, and gamblers will have to deal with it with their
`q`. Really there is a slight worry here; gamblers might want a piecemeal approach
and seek workarounds. Currently expect this problem to be limited at best.

## Systems to determine `q`
Limiting to services with reputation, in the case of a kind of network where
nodes keep opinions of each other, which transfer.(in some non-exploitable way,
of course) This network may be used to determine `q` assuming the reputation
can be used in some fashion for that purpose.

Lets also assume that nodes list where they got trust from.

For instance in buying a service, say without escrow, client side, the search
starts from your own node, and that of the service. You work outward finding
nodes that have good reputation for both. How good different paths(trees) are
depends on how high `q` is for nodes on them, and how much they are willing to
contribute.

Once the search has exhausted, there are a bunch of paths(trees) of contracts
to follow, to submit this request for bets, you create a transaction that
lists the paths, and contract execution will not have to search and go straight
to computing how the bet will operate.

## Probabilities and trust
When a gambler indicates probability directly, this results from estimates of
the different aspects. It may be possible to figure out probabilities of the
individuals, and imply a level of trust. However, this can be a tangle, 
it seems likelier that the above approach is used to figure out an order of
betters. Still, it is an approach to look at.

There is also the issue to handle when things go wrong. Basically gamblers
would remove reputation, but they could also investigate what happened.
Removing reputation from a node may in many systems also remove reputation
from nodes downstream. This is bad for the subject of the node which thus gets
less reputation. So in principle it may cause investigation from that end aswel.
(and contacting about what the results are)

Point of the latter is that reputation may also be a way to incentivize at
least reputable people/entities helping each other.

## Stabilizing gambler income
The gambler expects on average factor on the input ethers per unit time. However
depending on the number of bets and their dependence, actual results can vary.
He could insure himself against it, or predict some growth use a Contract for
a difference where people may bet it is more.
(this may actually be the same thing twice..)

