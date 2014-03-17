**TODO** remove this once the simple modifications are in cll-sim.
They are adding `block.number` and `block.parenthash`.

# Viewing and serving
Servers store data but need to be reimbursed for network use and storage. 
This (on average)pays them for serving data. Note that Vitalics 'dropbox' 
reward system could be complentary for paying for storage data not often
accessed.(afaict the dropbox doesnt actually reward serving it to anyone.

**Viewers:**
* set up the script with some coin in it.

That is *all* they do on the blockchain! Rest is talking to the servers.

* ask for serving something with a signed request message.
* give *potential* with the reward message afterwards.
Finally, they can top up the ammount of coin.(just send coin)

Viewers can only drain it by faking a redeem messages. It is not intended to be
emptied afterwards.

**Servers:**
Within the block number range, `from_block` to `from_block + attempt_cnt`:

* can punish using the request message for not getting a signed reward message.
  `(PUNISH request_signature view_checksum from_block)`
* have a *chance* of getting a reward using the signed reward message.
  `(REDEEM request_signature view_checksum from_block)`

# Attacks:
* Not give out reward message &rightarrow; solved with punishment.
* Draining the script before other servers can get to it by 
  'playing both viewer and server' &rightarrow; **TODO:** minimum ether store.

# TODO
* Most importantly, probably ethereum has some sort of anti-replay mechanism. So
  the current setup would not work in that case.
* If it lives, you'd need software to actually do the server-ing and requesting.
  That includes the signatured messages and the servers checking that the
  scripts are alive and contain coin.
* Do math? Are viewers draining the scripts right before a problem?
  (do not think so)
* Suppose it would need some suggestions for parameters. For instance 
  `punish_max == 2*redeem_reward` or something.
* Application to other things?
* Minimum ether storage, that doesnt extract. Basically it is a stake so that
  the contract owner loses something if servers were to blacklist the particular
  viewer.
* Think about 'stock' aspect, can you make a subcurrency somehow and give the
  creators a premine?

# Additional (potential)features
Maybe just allow a single block for potential payout. 

Could simply specify a single block, but that assumes you can always get into
blocks. (multiple blocks is not a foolproof solution..) Again: do math.

Seem bad:

* Trying to insure against a lot of payouts at once; the `redeem_reward` simply
  should not be too high. The idea here is that the payments are really-really
  tiny such that we need use probability. Besides, servers simply wouldnt get
  paid, and can see the balance and the chance of not being paid ahead of time.

* User getting the money out; people should already know that sending money is
  by default final, and they can use other mechanisms to make it more secure.

* Trying to avoid users faking signatures to drain it: No known Sigil-proof way
  of doing it. Probably cant be done.
