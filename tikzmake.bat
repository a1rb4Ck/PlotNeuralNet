python %~1.py

pdflatex %~1.tex
pdftoppm -png -r 70 %~1.pdf > %~1.png

del /F /Q *.log *.aux
REM del /F /Q *.tex

REM start %~1.pdf
PAUSE;
