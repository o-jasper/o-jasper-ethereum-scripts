https://forum.ethereum.org/discussion/comment/2948/

For *any* computation for which checking is cheaper than computing, you can

* Offer rewards for correct computation.
* Force one of the parties to provide computation.

The openness of the script is not negatively affected, if only one solution is
really accepted.

Caveit: In the case of reward, there is a race condition! A reservation for
providing the solution `S` by providing `H(S)` is needed, otherwise, anyone
can see the posed solution and pretend to come up with one independently.
