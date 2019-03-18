#!/bin/bash


python3 $1.py 
pdflatex $1.tex

rm *.aux *.log *.vscodeLog
rm *.tex

xdg-open $1.pdf

