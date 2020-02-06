TEX = $(wildcard *.tex)

.PHONY: paper
paper: $(TEX)
	echo -n "Words in abstract (200 max): " > wordcount.tex
	-texcount -total -brief -sum=1 summary.tex >> wordcount.tex
	echo -n "Words in main text (3300 max): " >> wordcount.tex
	-texcount -total -brief -sum=1 body.tex >> wordcount.tex
	echo -n "Words in methods (3000 max): " >> wordcount.tex
	-texcount -total -brief -sum=1 methods.tex >> wordcount.tex
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA
	-rm wordcount.tex
