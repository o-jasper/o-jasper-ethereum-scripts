;'Face end' of publishing DO.
; OWNER could also be a contract. Infact i would not recommend it being a person
;
; Articles and advertisements are 'assets', are arbitrary other contracts.
;
; * If callers ask for entries, they need to return DHT addresses.
;   The contract then also handles a donation.
;
; * Only owner of the DO can change articles/ads, if it is called with "set", it
;   must return "deny" if the contract doesnt allow, otherwise it accepts.
;
; * Only owner chan change the top level DHT address with "set_addr", now every
;   contract has to accept.(by not returning "deny") otherwise, the change is
;   not allowed.

{
  [0] DAO_NAME  ;Register name
  (call NAMECOIN_ADDR 0 0 0 DAO_NAMELEN 0 0)
  
;DHT address
  [[0x00]] INIT_DHT
}
{
  
  (if (= (calldatasize) 0) ;Take non-particular donation.
      (return))
  
  (if (= (calldatasize) 1)
  {
      (if (= (calldataload 0) "addr")  ;Asking for toplevel DHT address.
          (return @@0x00))
      
      (if (= (calldataload 0) "art_cnt") ;Return number or articles.
          [i] 0x10
          (for () (not (= @@@i 0)) [i] (+ @i 0x10))
          (return (- @i 0x10)))
  })
  
  (if (= (calldatasize) 2)
  {
      (if (= (calldataload 0) "spot")  ;Asking for entries.
       {  [i] (+ (calldataload 1) 0x10)
          (if (= @@@i 0) ;Note: donations are taken, contracts will have to poke first.
              (return 0))
      
      ;Note that it may just give back donation, depends on deal.
          (call @@@i (callvalue) (- (gas) 21) 0 0 0x20 0x20)
          (return @0x20)
        })
      (if (= (calldataload 0) "spotcontract") ;Contract at that spot.
          (return @@(calldataload  1)))
  })
  
;Sender may send entire lists of commands for lower weight.
  (if (and (= (sender) OWNER) (> (calldatasize) 0))
  {
  [j] 0x0
  (for () (< (+ @j 2) (calldatasize)) () ()
  
      (if (and (> (- (calldatasize) @j) 2) (= (calldataload @j) "set"))
       {
          [i] (+ (calldataload (+ @j 1)) 0x10)
          [0x10] "set"
          (call @@@i (callvalue) (- (gas) 21) 0x10 0x10 0x30 0x10)
          
          (if (= @0x30 "deny")  ;Deal is not in a place where it may change.
              (return))
          
          [[@i]] (calldataload (+ @j 2))  ;Successfully changed deal.
          [j] (+ @j 3)
        }
    ;Set top level address. All must agree.
          (if (> (- (calldatasize) @j) 1)
              (if (= (calldataload 0) "set_addr")
                {
                  [i] 0x10
                  [0x30] "set_addr"
                  (for () (not (= @@@i 0)) [i] (+ @i 0x10)
                       {(call @@@i (callvalue) (- (gas) 21) 0x30 0x10 0x40 0x10)
                       (if (= @0x40 "deny")
                           (return))
                       })
                  [[0x00]] (calldataload 0)
                  [j] (+ @j 2)
                  } ;"discontinue" to tell that it is no longer required.
                  {
                  [0x30] (calldataload 1)
                  (call (calldataload 0) (- (gas) 21) 0x30 0x10 0 0)
                  [j] (+ @j 2)
                }))))
  })
}
