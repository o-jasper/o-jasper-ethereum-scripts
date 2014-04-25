
default: tx-firewall.png

%.png: %.svg
	convert -trim $< $@

%.md: %.html
	markdown $< > $@
