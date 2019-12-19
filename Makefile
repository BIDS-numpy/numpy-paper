TEX = $(wildcard *.tex)

.PHONY: paper
paper: $(TEX)
	touch wordcount.tex
	-texcount -total -sum=1 paper.tex | tail -n 8 > wordcount.tex
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA
