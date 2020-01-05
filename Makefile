TEX = $(wildcard *.tex)

.PHONY: paper
paper: $(TEX)
	echo -n "Words in abstract: " > wordcount.tex
	-texcount -total -brief -sum=1 summary.tex >> wordcount.tex
	echo -n "Words in text: " >> wordcount.tex
	-texcount -total -brief -sum=1 body.tex >> wordcount.tex
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA
	-rm summarycount.tex wordcount.tex
