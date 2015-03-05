
default: build/grudge_creator.js build/grudge-escrow.lll

build/grudge_creator.js: build/grudge-escrow.evm grudge_creator_js.sh
	sh grudge_creator_js.sh > build/grudge_creator.js

test: test_cases

test_cases:
	python2 cases.py

build/%.lll: %.se
	serpent compile_to_lll $< > $@

build/%.lll.evm: %.lll
	lllc -x $< > $@

build/%.evm: %.se
	serpent compile $< > $@
