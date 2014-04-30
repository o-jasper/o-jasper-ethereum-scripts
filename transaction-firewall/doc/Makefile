
default: classifier.png post.html

%.png: %.svg
	convert -trim $< $@

%.html: %.md
	markdown $< >  $@
