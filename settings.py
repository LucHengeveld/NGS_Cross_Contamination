# What is the .fastq or .bcl file path? Example: 'C:\\Users\\Biolegio\\example.fastq'
# fastq_testfiles\uniq_fastq_no_spike.fastq
FASTQ_FILE = 'fastq_testfiles\\comb_fastq_spike.fastq'

# What is the barcode (and spike-in sequence) file? Example: C:\\Users\\Biolegio\\example.txt
BARCODE_FILE = 'barcode_testfiles\\comb_barcode_spike.xlsx'

# Is the plate created by using combinatorial indexing (1) or unique dual indexing (2)?
INDEXING = 1

# What would you like to analyse?
# TODO: Add option for both spike i5 and spike i7 together
# (1) i5 + i7
# (2) Spike ins + i5
# (3) Spike ins + i7
# (4) Spike ins + i5+i7
ANALYSE_COMBINATION = 2

# Which sequencer has been used?
# (1) iSeq / MiniSeq / NextSeq / HiSeq3000 / HiSeq4000
# (2) MiSeq / HiSeq2000-2500 / Novaseq
SEQUENCER = 1

# How many nucleotides are the found barcodes allowed to differ from the original barcodes?
BARC_DIFF = 0

# What is the maximum percentage of contamination compared to the amount of correct reads? Please use the following format:
# Write 1 for 1% max contamination
# Write 0.1 (seperated by a dot) for 0.1% max contamination
MAX_CONTAMINATION = 0.1

# In which directory would you like to save the output file?
OUTPUT_DIR = 'output\\'

# What name would you like to use for the output file?
OUTPUT_FILENAME = 'comb_i5_spike'
# OUTPUT_FILENAME = 'comb_i7_spike'
# OUTPUT_FILENAME = 'comb_i5_i7_spike'
# OUTPUT_FILENAME = 'uniq_i5_spike'
# OUTPUT_FILENAME = 'uniq_i7_spike'
# OUTPUT_FILENAME = 'uniq_i5_i7_spike'

# --- Spike-ins ---
# Enter a 0 as value for the parameters below if you are not using spike-in sequences

# If using spike-ins: how many nucleotides are the found spike-in sequences allowed to differ from
# the original sequences?
SPIKE_DIFF = 0

# If using spike-ins: what are the i5 and i7 ends of the spike-in sequences?
# (1) i5 - spike-in sequence - i7
# (2) i7 - spike-in sequence - i5
SPIKE_BAR_ORDER = 0

# If using spike-ins: how many nucleotides should be trimmed from the i5 end?
I5_TRIM = 0

# If using spike-ins: how many nucleotides should be trimmed from the i7 end?
I7_TRIM = 0

# If using spike ins: In which order would you like for the program to count the sequences?
# (1) Per column: A1=1, B1=2, C1=3, ..., A2=9, B2=10, C2=11, ...
# (2) Per row: A1=1, A2=2, A3=3, ..., B1=13, B2=14, B2=15, ...
SPIKE_COUNT_ORDER = 0
