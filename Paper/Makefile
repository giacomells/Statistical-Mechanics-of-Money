# ============================================================================
# MAKEFILE: Build automation for LaTeX paper
# ============================================================================

TEX = pdflatex
TEX_FLAGS = -interaction=nonstopmode -halt-on-error
MAIN = main
BIB = bibtex

.PHONY: all build clean distclean view help

all: build

build: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex chapters/*.tex appendices/*.tex config/preamble.tex
	$(TEX) $(TEX_FLAGS) $(MAIN).tex
	$(BIB) $(MAIN)
	$(TEX) $(TEX_FLAGS) $(MAIN).tex
	$(TEX) $(TEX_FLAGS) $(MAIN).tex

clean:
	rm -f *.aux *.bbl *.blg *.log *.out *.toc *.lof *.lot

distclean: clean
	rm -f $(MAIN).pdf

view: $(MAIN).pdf
	open $(MAIN).pdf &

help:
	@echo "Makefile targets:"
	@echo "  make       - Compile to PDF"
	@echo "  make clean - Remove auxiliary files"
	@echo "  make distclean - Remove all generated files"
	@echo "  make view  - Open PDF"
