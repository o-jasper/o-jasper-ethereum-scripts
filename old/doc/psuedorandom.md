From me [here](https://forum.ethereum.org/discussion/comment/2758/#Comment_2758),
kept here for reference and warning about miner collusion.

# Text

Future block hashes can be combined with some predetermined value to
provide psuedorandom data.

Afaik that should be fairly good psuedorandom data. *However* block miners
could collude; hold back blocks that dont have the winner they want. It 
lowers their chance of winning a block, so it is costly, but then bets could
have a lot at stake too.

This can be prevented by both parties having a secret S1,S2, initially they
reveal H(S1), H(S2), then they wait a block, which has a checksum H(B). After
that the 'game' or program can use the number R=H(S1 ... S2 ... H(B)) as random.
Since neither knew S1,S2 of the other side, neither can collude with miners to
affect R.

Still have a problem though, one of the two has to release the secret first,
and the second one can then figure out what the result of the game is before 
he gives his secret. This can be fixed by giving forfeitures at this point the
'maximum loss' in the game, and having a time frame for the players to respond.
(presumably they can get their transactions in a block by that time)

# TODO
* See if i can update this.
* Consider a contract particularly for serving up random data.
* At what point does miner collusion *actually* become a problem. I.e. if the
  damage is at an acceptable level, the simple method might be acceptable.
* Keep a lookout for other ways of getting psuedorandom value.
