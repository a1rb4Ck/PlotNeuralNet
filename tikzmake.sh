#!/bin/bash

python3 $1.py

pdflatex $1.tex
pdftoppm -png -r 70 $1.pdf > $1.png

rm -rf *.aux *.log *.vscodeLog
# rm -rf *.tex

if [[ "$OSTYPE" == "darwin"* ]]; then
    open $1.pdf
else
    xdg-open $1.pdf
fi
