
# Simpler contract for simpler testing..

It is called grudging escrow because if the deal fails, the rational choice if
grudge has no value to you, is to pretend it succeeded.

Also, it just destroys value if things go wrong. It is a *bad* contract to
actually use! *Dont do it*, just on the testnet with wortless things. 

The testing and such does not go as far as it aught to.
There will be TODOs left behind. Please do not take this thing seriously.

### TODO

* Automatically release after longer time if no intervention to specifically
  deny it. (Avoid accidents)

* When a transaction is already underway, the javascript doesnt send another.
  
* Have images of waiting/smiling guys, and add a 'time of delivery',
  and if funds arent released have them turn grumpy.(TODO have more images)

* Get the javascript contract launcher to actually work.

* Yikes, max-gas-use defaults to max ability of balance right now.. Do better
  on estimating.
  
* Registering the time in the contract might not be needed after all,
  can go through `eth.messages(filter)` to find the relevant messages.
  
### Did
* Add time notice to ensure the merchant cannot change the deal right
  before a customers' transaction arrives.

* Refund non-meaningful-message-donations.

* Add tipping to javascript.

* When setting up, show percentages of stake.
  Red letters if stake is bigger than total.
