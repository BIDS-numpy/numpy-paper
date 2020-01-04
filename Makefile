TEX = $(wildcard *.tex)

.PHONY: paper
paper: $(TEX)
	echo -n "Words in abstract: " > summarycount.tex
	-texcount -total -brief -sum=1 summary.tex >> summarycount.tex
	touch wordcount.tex
	-texcount -total -sum=1 body.tex | tail -n 8 > wordcount.tex
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA
	-rm summarycount.tex wordcount.tex
