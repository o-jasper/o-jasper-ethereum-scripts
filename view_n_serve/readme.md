**Note** The 'rich server' attack is a problem.. For instance if content is
considered 'wrong' someone rich might simply pretend to serve it and then use
the punishment scheme. The cost on his side may just be part of the course.

# Viewing and serving
Servers store data but need to be reimbursed for network use and storage. 
This (on average)pays them for serving data. Note that Vitalics 'dropbox' 
reward system could be complentary for paying for storage data not often
accessed.(afaict the dropbox doesnt actually reward serving it to anyone.

**Viewers:**

* set up the script.
* Put ether in it. (anyone can put ether in it)

That is *all* they do on the blockchain! Rest is talking to the servers.

* ask for serving something with a signed request message.
* give *potential* with the reward message afterwards.

Viewers can only drain it by faking redeem messages. It is not intended to be
emptied afterwards.

**Servers:**
Within the block number range, `from_block` to `from_block + attempt_cnt`:

* can punish using the request message for not getting a signed reward message.
  `(PUNISH request_signature view_checksum from_block)`
* have a *chance* of getting a reward using the signed reward message.
  `(REDEEM request_signature view_checksum from_block)`

Servers would have to look at the script used and if there is enough ether in 
it. They may also keep a blacklist.

Currently it is pretended that viewers give ready-to-go transactions during
requesting and accepting. This might not be possible, we'd need to have a 
viewer-signed statement that the script then has to check.

## Attacks:
* Rich attacker playing server, aiming at particular viewers? 
* Not give out reward message &rightarrow; solved with punishment.
* Draining the script before other servers can get to it by 
  'playing both viewer and server' &rightarrow; **TODO:** minimum ether store.
  
  Note: different servers would have to communicate about contracts being used
  so any particular contract cant be overused to make the minimum ether store
  a small portion.

## TODO
* Most importantly, probably ethereum has some sort of 
  anti-[replay](https://en.wikipedia.org/wiki/Replay_attack) mechanism. So
  the current setup would not work in that case.

* Figure out the effects of miner collusion in the use of `block.prevhash`
  as psuedorandom.

* Minimum ether balance, that *never* extracts. This punishes viewers
  because they'd need ether to make a new contract if servers blacklist it.

* Suppose it would need some suggestions for parameters. For instance 
  `punish_max == 2*redeem_reward` or something.

* Application to other things?

* Prefer if the servers only got one shot, based on a single `.parenthash`, but
  were still able to use a whole range of blocks to actually collect it.

* What does it look like if it were implemented on the server side instead?
  (dont expect it is better)

* If it lives, you'd need software to actually do the server-ing and requesting.
  That includes the signatured messages and the servers checking that the
  scripts are alive and contain coin.

## Additional (potential)features
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

* Trying to avoid users faking signatures to drain it: Dont see how to do it,
  could try having whitelists in the contract i suppose.
