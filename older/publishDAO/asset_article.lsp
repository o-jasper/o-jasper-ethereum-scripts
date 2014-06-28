;Content asset with no rights.

;MAXBAL is there incase they introduce billing for storage.(and no countermeasure)
{
[[0]] PUBDAO_ADDR
}
{
    [bal] (balance (address))
    (if (> @bal MAXBAL)  ;Keep the balance in place.
        (call @@0 (- @bal MAXBAL) 0 0 0 0))

    (if (= (calldatasize) 0) ;;Return the DHT value.
        (return DHT_ADDR))
    
    (if (and (= (calldatasize) 1) (= sender @@0))
        {
        (if (= (calldataload 0) "discontinue")
            (suicide @@0))
        (return "accept")
        })
}
