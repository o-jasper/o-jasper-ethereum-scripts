
default: build/creator.js

test: test_cases

test_cases:
	python2 cases.py

build/%.lll.evm: build/%.lll
	lllc -x $< > $@

build/%.se.evm: %.se
	serpent compile $< > $@

build/creator.js: build/assurance_ent.se.evm creator.sh
	sh creator.sh > build/creator.js
