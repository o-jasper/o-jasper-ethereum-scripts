
MCONV = replace '<code>' '<b>' '</code>' '</b>' '&amp;' '&'\
 '<blockquote>' '<blockquote><b>' '</blockquote>' '</b></blockquote>'

default: *.html

Stake.html: Stake.md
	markdown $< | $(MCONV) > $@

Trust_estimate.html: Trust_estimate.md
	markdown $< | $(MCONV) > $@

%.html: %.md
	markdown $< > $@
