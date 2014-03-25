
# Tipping that may pay for itself

Idea for system where tipping first will pay you back if enough is tipped.
Inspired from maciejolpinski at [forum.ethereum](https://forum.ethereum.org/discussion/comment/3240).

The idea is to have a function g(a), for instance g(a)=1/a&sup2;, if you tip, you
get G(a,d)=&int;<sub>a</sub><sup>a+d</sup>f&sdot;g(a')da', where a is the amount already
tipped, and d the amount you tipped. f is determined by G(0,A)=&beta;A meaning:
a fraction is used as tip.

g(a) must also fall. Also in principle G(0,A) could also be any function of A,
as long as it always increases and never exceeds A.

For g(a)=1/a&sup2; we have G(a,d)= f&sdot;(1/(a+d)&sup3; - 1/a&sup3;) 
 is tipped in total, some fraction &beta; goes back to the tippers;
 &beta;A=G(0,A) then so then f= &beta;A/(1/(a+d)&sup3; - 1/a&sup3;)
