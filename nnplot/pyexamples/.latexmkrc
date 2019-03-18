$pdf_mode="1";
$pdflatex="pdflatex --shell-escape %O %S";

$default_files=("all_blocks.tex");


add_cus_dep("py", "pdf", 0, "run_script");
sub run_script {
   system("python $_[0].py"); 
}
