# --- These parameters can be edited by the user ---

# What is the .fastq file path? Example: 'C:\\Users\\Biolegio\\example.fastq'.
# fastq_testfiles\uniq_fastq_no_spike.fastq
FASTQ_FILE = 'fastq_testfiles\\test.fastq'

# What is the barcode (and spike-in sequence) file? Example: C:\\Users\\Biolegio\\example.txt.
# Use the same format as the barcode_example.xlsx file.
BARCODE_FILE = 'barcode_testfiles\\uniq_barcode_spike.xlsx'

# Is the plate created by using combinatorial indexing (1) or unique dual indexing (2)?
INDEXING = 2

# What would you like to analyse?
# (1) i5 + i7
# (2) Spike ins + i5
# (3) Spike ins + i7
# (4) Spike ins + i7 and spike ins + i5
# (5) Spike ins + i5 + i7
ANALYSE_COMBINATION = 1

# What would you like to analyse?
# (1) Known and unknown barcodes / spike-in sequences
# (2) Only known barcodes / spike-in sequences
# (3) Only unknown barcodes / spike-in sequences
ANALYSE_TYPE = 1

# Which sequencer has been used?
# (1) iSeq / MiniSeq / NextSeq / HiSeq3000 / HiSeq4000
# (2) MiSeq / HiSeq2000-2500 / Novaseq
SEQUENCER = 1

# How many nucleotides are the found barcodes allowed to differ from the original barcodes?
BARC_DIFF = 0

# What is the maximum percentage of contamination compared to the amount of correct reads? Please use the following format:
# Write 1 for 1% max contamination
# Write 0.1 (seperated by a dot) for 0.1% max contamination
MAX_CONTAMINATION = 0.0001

# In which directory would you like to save the output file?
OUTPUT_DIR = 'output\\no-spike\\'
# OUTPUT_DIR = 'output\\with-spike\\'

# What name would you like to use for the output file?
OUTPUT_FILENAME = 'comb_test'


# --- UMI: Unique Molecular Identifier ---
# Enter a 0 as value below if you are not using unique molecular identifiers

# What is the i7 barcode length? (all nucleotides after this specific length
# are seen as UMIs)
I7_LENGTH = 0


# --- Spike-ins ---
# Enter a 0 as value for the parameters below if you are not using spike-in sequences

# If using spike-ins: how many nucleotides are the found spike-in sequences allowed to differ from
# the original sequences?
SPIKE_DIFF = 0

# If using spike-ins: how many nucleotides should be trimmed from the left end?
LEFT_TRIM = 0

# If using spike-ins: how many nucleotides should be trimmed from the right end?
RIGHT_TRIM = 0
