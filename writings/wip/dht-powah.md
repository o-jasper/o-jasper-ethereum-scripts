Note: i have doubts if this speaks to people nearly enough, might be better to
present it with a 'mocked up DHT'.

# DHTs: more than just storage

<a href="https://en.wikipedia.org/wiki/Distributed_hash_table">Distributed Hash Table</a>
(https://en.wikipedia.org/wiki/Distributed_hash_table)
we will assume the with the DHT you get a file by naming it by its checksum,
and files cannot be removed if they already exist, and there is at least one
party interested in them.

This has far reaching implications: 

A contract can control its page via a Name Registry. As it is arbitrary code,
it can also be <i>limited</i> to the extent it can choose/change the reference
in the name registry.

Furthermore, javascript on the page can 1) look at the consensus data in
the blockchain 2) change what it shows it.

This means that contracts choose can force themselves to have particular data on
their URL, from which follows that particular javascript doing its thing.

## Uses

## Publishing DAOs

For a publishing DAO: force itself to a layout, with articles and
advertisements. Potential advertisers check that they like the layout,
and buy spots. As added bonus a way to opt out from the advertising could
be created where users do a little payment.

For writings, but maybe even audio and video(depending on how well that DHT
works!) on the web, this is one end of the 'Earning from Authorship' problem.

The other end is attracting and rewarding authors! This is still an open
problem. One solution is simply to do a co-op and gather people with some 
agreement over who does/controls/earns wha.

But wiki-DAO or functional code may have a particular way where the content,
is estimated to be valuable or authored by particular people, and reward
based on that. Most ambitiously, even a system where how everything derives
from everything else and who authored it may be possible.

## Entities making claims

A company may claim its product is good, and put that up to some kind of judge,
say that of the customers. The layout is forced again, so if the customers
say NAY, it aint true.

In the context of Democracy-DAO, a government can literally be forced to make
certain statements on their own public websites.

Publishing DAO, again, could also force themselves to allow some other party
to add criticism right on the page itself. This might be useful for parties
seeking to be reputable sources.

## Disadvantages

The browser can change, and the page cannot be updated to match those changes.
It would likely require LTS versions, or use of very stable features.
