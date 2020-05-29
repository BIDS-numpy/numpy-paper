TEX = $(wildcard *.tex)
REFERENCES = '/bibliography{references}/ {'
PATTERN1 = "s/\{references\}/\{supplementary\}/"
PATTERN2 = '/bibliography{supplementary}/ {'

.PHONY: paper
paper: $(TEX)
	echo -n "Words in abstract (200 max): " > wordcount.tex
	-texcount -total -brief -sum=1 summary.tex >> wordcount.tex
	echo -n "Words in main text (3000 max): " >> wordcount.tex
	-texcount -total -brief -sum=1 body.tex >> wordcount.tex
	echo -n "Words in methods (3000 max): " >> wordcount.tex
	-texcount -total -brief -sum=1 methods.tex >> wordcount.tex
	TEXINPUTS=.//: latexmk -pdf -use-make paper.tex

.PHONY: submit
submit: paper
	# Main
	latexpand _main.tex > main.tex
	latexmk -pdf -use-make main.tex
	sed -e $(REFERENCES) -e 'r main.bbl' -e 'd' -e '}' -i main.tex
	# Supplement
	latexpand _supplementary.tex > supplementary.tex
	latexmk -pdf -use-make supplementary.tex
	bibexport -o supplementary.bib supplementary.aux
	sed -ie '/textbf/,+2d' supplementary.bib
	perl -pi -e $(PATTERN1) supplementary.tex
	latexmk -pdf -use-make supplementary.tex
	sed -e $(PATTERN2) -e 'r supplementary.bbl' -e 'd' -e '}' -i supplementary.tex
	@echo 
	@echo "******************************************"
	@echo "Final steps"
	@echo "******************************************"
	@echo "Deal with figures."

.PHONY: summary
summary:
	pandoc --strip-comments -t plain  summary.tex

.PHONY: clean
clean:
	@rm -f *~
	latexmk -CA
	-rm wordcount.tex
