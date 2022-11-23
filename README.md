# NGS_Cross_Contamination

## Code manual:

### Windows:
1) Download Python and select add to PATH in installer (3.10 has been used to create this project)
   - Check if python is installed correctly with the command 'py --version'

2) Open a terminal:
   - Type cmd in your windows search bar.

3) Check if pip is installed with the following command:
   - py -m pip --version
   - Skip step 4 and 5 if pip is installed.

4) If pip has not been installed, try running the following commands:
   - py -m ensurepip --default-pip 
   - py -m pip --version

5) If that still doesn't work, manually download pip from https://bootstrap.pypa.io/get-pip.py and run the following command:
   - python get-pip.py

6) Ensure pip, setuptools and wheel are up-to-date with the following command:
   - py -m pip install --upgrade pip setuptools wheel

7) Install the required packages from requirements.txt:
   - By double-clicking the windows_packages.bat file;
   - or by using the command 'pip install (packagename==version)'

8) Open the settings.py file with a text editor like notepad:
   - Edit the parameters and save the file.

9) Open a terminal in the project directory by right-clicking:
   - Show more options -> open in terminal

10) Run main.py by using the following command:
    - python main.py


### Linux:
1) Download Python and select add to PATH in installer (3.10 has been used to create this project)
   - Check if python is installed correctly with the command 'python3 --version'

2) Open a terminal:
   - Type terminal in your linux search bar.

3) Check if pip is installed with the following command:
   - python3 -m pip --version
   - Skip step 4 and 5 if pip is installed.

4) If pip has not been installed, try running the following commands:
   - python3 -m ensurepip --default-pip
   - python3 -m pip --version

5) If that still doesn't work, manually download pip from https://bootstrap.pypa.io/get-pip.py and run the following command:
   - python3 get-pip.py

6) Ensure pip, setuptools and wheel are up-to-date with the following command:
   - python3 -m pip install --upgrade pip setuptools wheel

7) Install the required packages from requirements.txt:
   - By using the command bash linux_packages.sh;
   - or by using the command 'pip install (packagename==version)'

8) Open the settings.py file with a text editor:
   - Edit the parameters and save the file.

9) Open a terminal in the project directory by right-clicking:
   - Open in terminal

10) Run main.py by using the following command:
    - python3 main.py

## List of errors that can occur when running the code:
1) parameters.py - Error 1: Entered fastq file has incorrect file extension.
2) parameters.py - Error 2: Entered barcode (+ spike) file has incorrect file extension.
3) parameters.py - Error 3: Entered indexing value is incorrect.
4) parameters.py - Error 4: Entered analysis combination value is incorrect.
5) parameters.py - Error 5: Barcode nucleotide difference parameter is incorrect.
6) parameters.py - Error 6: Spike-in nucleotide difference parameter is incorrect.
7) parameters.py - Error 7: Entered sequencer value is incorrect.
8) parameters.py - Error 8: Entered output directory path does not exist.
9) parameters.py - Error 9: Entered heatmap contamination percentage is incorrect.
10) parameters.py - Error 10: Entered i7 barcode length is incorrect.
11) parameters.py - Error 11: Entered spike-ins left trimming value is incorrect.
12) parameters.py - Error 12: Entered spike-ins right trimming value is incorrect.
13) parameters.py - Error 13: Not all parameters have been entered in settings.py.
14) file_readers.py - Error 14: Fasta file format is incorrect. No headers found.
15) file_readers.py - Error 15: Entered fastq file has not been found.
16) file_readers.py - Error 16: Entered barcode file has not been found.
17) file_readers.py - Error 17: Barcode file format incorrect.
18) file_readers.py - Error 18: Fasta file format is incorrect. No headers or sequences found.
19) file_readers.py - Error 19: Entered fastq file has not been found.