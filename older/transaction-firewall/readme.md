# Transaction firewall and parameter selection
Does two things.

## Classifying input
Classifying input using simple logic. Potentially usable as 'transaction firewall'.
Where construct a classifier in this so you stake a clear claim about what
transactions a program produces, allowing that to be checked. It may also serve
as a 'look at this transaction before sending' warning.

Note: i am not sure how applicable it is, it probably makes more sense to have
successive ethereum bytecode statement classify/firewall transactions.

## Creating input
Turns out the other side of the coin is selecting parameters. There is a
simple stdin, and gtk gui under development.
