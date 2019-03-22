#!/bin/bash

python $1.py

pdflatex $1.tex
pdftoppm -png -r 70 $1.pdf > $1.png

rm -rf *.aux *.log *.vscodeLog
# rm -rf *.tex

xdg-open $1.pdf
