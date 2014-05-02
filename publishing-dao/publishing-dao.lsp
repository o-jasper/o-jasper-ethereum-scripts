{
  [0] DAO_NAME  ;Register name
  (call NAMECOIN_ADDR 0 0 0 DAO_NAMELEN 0 0)
  
;Number of articles/advertisements. Note that the DHT page scripts do the work
; of figuring out which are advertisements and which 
  [[0x00]] 0
;Duration of advertising period.
  [[0x10]] 0 
}
{
;Plain donation. Return time at which current advertising series ends.
(if (= (calldatasize) 0) (return @0x10))

(if (= (calldatasize) 1)  ;Asking what articles/advertisements there are.
    (if (< (+ (calldataload 0) 0x20) @@0)
        {
        (if (> (callvalue) 0) ;Also indicating particular interest.
            ;TODO..
            )
        (return @@(+ (calldataload 0) 0x20))
        }
        (return)
        ))

;;Everything is owned by that address/contract from past this point.
;; Note that the owner probably needs mechanism to ensure 
(if (not (= (caller) OWNER))
    (return))

(if (> (calldatasize) 1)
    [cmd] (calldataload 0)
    (if (= [cmd] 0)  ;Adding addresses.
        {
        (for [i] 1 (< @i (calldatasize)) [i] (+ @i 1)
             {
             [[ @@0x00 ]] (calldataload @i)
             [[0x00]] (+ @0x00 1)
             })
        (return @0x00)
        })
    (if (= [cmd] 1)  ;Overwriting adresses; index-address pairs.
        {
        (for [i] 1 (< @i (calldatasize)) [i] (+ @i 2)
             {
             [[ @@(calldataload ) ]] (calldataload @i)
             [[0x00]] (+ @0x00 1)
             })
        (return)
        })
    (if (= [cmd] 2) ;Removing everthing past this number of adresses.
        )
}
