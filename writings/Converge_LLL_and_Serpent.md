As [this issue](https://github.com/ethereum/cpp-ethereum/issues/175).

----

I understand that this is sort-of a loosely coupled project. But i think perhaps there is a way to neatly 'align' Serpent and LLL.

Starting bottom-up; in order

* Firstly, LLL becomes a lisp version very close to the bytecode.  (essentially it is now?)

* Currently in cpp-ethereum `compileLispFragment` goes straight from a string,  it will have to go via a tree.(potentially nested lists) Could write a   `parseLisp` that can do it.

* Then we add lisp-like macros, for developers only; i.e. essentially the macros  are developers a uniform and flexible tool for adding features.^&dagger;
  
  We will also need a way to symbol-macros, or rather, have some logic around  those.
  
* Start adding macros, going for the set that makes Serpent first;

  Tying names and storage in with `set`

  + `(set name value &optional type)`, `name` would be stored at a particular index. Convert to `(mstore <memindex> <value>)` in typeless case, and remember the name and index.
    
    If the type is not 16 bytes, it will need to add a symbol-macro that selects the correct bit of memory every time. If `name` is already defined, the old one is used, and non-specification and identicalness to the old type asserted. Names are forgotten outside the scope.
  
  + `(set (mem index) value &optional type)` rawly sets a location in memory. Probably add a `memindex` to indicate where the memory is currently. This be a symbol-macro, not a variable. Users beware that making new variables afterwards moves the index.
    
    It would convert to simply `(mstore <index> <value>)`.
  
  + `(set (store name) value &optional type)` Here we also add `(rawstore value)` for raw storing, and keep a `storeindex`.(same caveit as `memindex`)
     
  + `(mem ..)` and `(store ..)` go to `mload`, `sload` *if* the first argument is not a symbol(in code) in which case the symbol is used. Not strictly needed for `mem`, but more consisten that way.
    
    (get around it with `(identity ..)`)
     
  We dont need `(mem value)` a lot, really? maybe `[[]]` &rarr; `[]`... Ditch `@` notation too.

* Then make the the Serpent bijection, parsing it into these trees, and writing the trees to be Serpent if possible. The parsing bit would have access to to everything LLL has.

  I [Explored 'beginners and enders + infix'](https://github.com/o-jasper/Treekenize.jl), to make the [Julia](http://julialang.org/) language more lispy by making the syntax perfectly clear. (syntax is simular to Lua)
  
  I just had to mention that a bit, both syntaxes are fine, and python looks better imo. LLL would have the beginners and enders bit, at least. (use it to do the current `{[]}`)

* Add more:

  + Or smooth out dealing with for instance multiple k-v stores.
  
  + Start taking `(address ...)` to be `(call address ...)` without value, this would essentially automatically translate over to Serpent.
  
  + Add a `cond` or `case` as in lisp, (or a `switch`.. but, well havent seen it often that i dont `break;`..)
  
  + Add the variable-type approach for the input.

Hope it doesnt sound wishy-washy, maybe i should speak in code more, but then you wouldnt know what i was doing, and it might be a giant power plant. Probably best to implement in Python, tests easier during development. Can always write versions in other languages afterward.

Already wrote a [s-expression parse in python](https://github.com/ethereum/serpent/pull/4)
with a slightly different motive, but i can put into action for this. I did start to a [to_LLL](https://github.com/o-jasper/serpent/tree/to_cll) conversion thing(i mislabeled it!), but i now kindah think the other way round is a better approach.
