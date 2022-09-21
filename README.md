# NGS_Cross_Contamination

## Possible Errors:
1) parameters.py: Error 1: Entered file has incorrect extension. Please enter a .bcl or .fastq file path in parameters.txt. 
2) parameters.py: Error 2: Entered file has incorrect extension. Please enter a .xlsx file path in parameters.txt.
3) parameters.py: Error 3: Entered indexing value is incorrect. Please enter a '1' if combinatorial indexing has been used or a '2' if unique dual indexing / non redundant indexing has been used.
4) parameters.py: Error 4: Entered analysis value is incorrect. Please enter a '1' to analyse I5 + I7 or a '2' to analyse spike-ins + I5 and I7.
5) parameters.py: Error 5: Entered maximum nucleotide difference between barcodes is not numeric. Please enter a number.
6) parameters.py: Error 6: Entered maximum nucleotide difference between sequences is not numeric. Please enter a number.
7) parameters.py: Error 7: Entered sequencer value is incorrect. Please enter a '1' if iSeq, MiniSeq, NextSeq, HiSeq3000 or HiSeq4000 has been used. Enter a '2' if a MiSeq, HiSeq2000-2500 or Novaseq has been used.
8) parameters.py: Error 8: Entered output directory path does not exist. Please enter a correct output directory path.
9) parameters.py: Error 9: Missing one of the parameters. Make sure you have entered all parameters in parameters.txt.
10) file_readers.py: Error 10: Fasta file format is incorrect. No headers found.
11) file_readers.py: Error 11: Entered fastq file has not been found. Please make sure the path to the file is correct.
12) check_barcodes.py: Error 12: Barcodes have not been found at the end of the headers in the fastq file.
13) file_readers.py: Error 13: Entered barcode file has not been found. Please make sure the path to the file is correct.
14) file_readers.py: Error 14: Barcode file format incorrect. Please enter a correct barcode file.
15) file_readers.py: Error 15: Barcode file format incorrect. Please enter a correct barcode file.
16) parameters.py: Error 16: Entered heatmap contamination percentage is not a number.