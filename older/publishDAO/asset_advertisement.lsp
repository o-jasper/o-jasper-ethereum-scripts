;Advertisement asset. 

{
[[0x00]] PUBDAO_ADDR
[[0x10]] (number)  ;Last payment.
[[0x20]] EXPIRY
[[0x30]] OWNER
}
{
    (if (= (calldatasize) 0) ;Return the bit of data.(it takes the donation)
        (return DHT_ADDR))

;Attempted of the page, accept if not expired/paid enough.
    (if (= (calldatasize) 1)
    {  
       [bal] (balance (address))
       [need] (* RATE (- (number) @@0x10))
       ;Note that this doesnt do anything in the contract, so anyone is allowed. 
       (if (and (or (= (calldataload 0) "set") (= (calldataload 0) "set_addr"))
                (or (> (number) @@0x20) ;Expired.
                    (< @bal @need))) ;Didnt pay enough.
            (return "accept")
            (return "deny"))
       ;Poke for payment.
       (if (and (= (sender) @@0x00) (= (calldataload 0) "poke"))
           {[n] (/ @bal RATE)
            (if (> @n (- (number) @@2x0)) ;Not enough there.(it would accept change)
                { [n] (- (number) @@2x0) })
            [[0x10]] (- @@0x10 @n)  ;These block numbers paid for.
            (call @@0x00 (* RATE @n) (- (gas) 21) 0 0 0 0)
            })

       ;Take out all you can.
       (if (and (= (sender) @0x30) (= (calldataload 0) "extract")
                (> @bal (+ @need STAKE)))
         (call @0x30 (- @bal @need STAKE) (- (gas) 21) 0 0 0 0))

       ;End contract.
       (if 

       ;PubDAO requests an contract address, and that contract address may
       ; do stuff with this contract.
       (if (or (= (sender) @@0x00) (= (sender) @@0x30))
         { ;Non-accepted suggestion already there, by other party.
           (if (and @@0x40 @@0x50 (not (= (sender) @0x50)))
               {(if (= (calldataload 0) @@0x40)
                    { [0x50] 0 } ;Accepted.
                    { [0x40] 0 ;Denied
                      [0x50] 0
                    })
               (stop)
               })
           (if (and @@0x40 (not @@0x50))  ;A deal was already made.
               (stop))
           [0x40] (calldataload 0) ;Propose.
           [0x50] (sender)
           })
       })

    (if (and (= (sender) @@0x40) (not @@0x50))  ;Accepted action talking.
      {  ;Change the expiration data or stop it.
         (if (and (> (calldatasize) 1)  (= (calldataload 0) "expiry"))
           { (if (= (calldatasize) 2)
                  {  [[0x20]] (calldataload 1) }
                  {  [[0x20]] 0 })
             (stop)
            })
      })
    
    ;Suicide it.
    (if (and (= (calldatasize) 1) (= (calldataload 0) "suicide")
             (or (and (= (sender) @@0x40) (not @@0x50)) ;By action contract.
                 (and (= (sender) @@0x30) (> (number) @@0x20)))) ;Expired and owner.
      {  
         (call @0x00 (* RATE (- (number) @@0x10)) (- (gas) 21) 0 0 0 0)
         (suicide @0x30)
      })
}
