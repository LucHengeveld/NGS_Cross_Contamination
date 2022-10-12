# Imports the required modules
import openpyxl


def fastq_reader_no_spike(fastq_path):
    """
    Reads and saves the info from the .fastq file to a list.
    :param fastq_path: Path to the .fastq file.
    :return fastq_data: List with the structure [barcode 1, barcode2, etc].
    """
    # Creates an empty list
    fastq_data = []

    try:
        # Opens the .fastq and reads it line by line
        with open(fastq_path, "r") as fastq_file:
            for line in fastq_file:
                # If line starts with a @ it retrieves the barcode
                if line.startswith("@"):
                    fastq_data.append(line[:-2].split(":")[-1])
        if len(fastq_data) == 0:
            print("Error 10: Fasta file format is incorrect. No headers"
                  "found.")
            exit(10)
        # Returns the fastq list
        return fastq_data

    except FileNotFoundError:
        print("Error 11: Entered fastq file has not been found.")
        exit(11)


def barcode_file_reader(barcode_file, sequencing_method, analyse_combination):
    """
    Retrieves the barcodes (and spike in sequences if spike_in parameter is
    '2') from the entered Excel file.
    :param barcode_file: Path to the Excel file.
    :param sequencing_method: Parameter from settings.py.
    :param analyse_combination: Parameter from settings.py.
    :return barcode_file_list: List with all barcodes from the Excel file.
    :return barcode_file_dict: Dictionary with structure {barcode: [well, spike
            seq, 0]}.
    """
    try:
        # Loads in the Excel barcode file
        excel_reader = openpyxl.load_workbook(barcode_file)
        sheet = excel_reader.active

    except FileNotFoundError:
        # Returns an error if file has not been found
        print("Error 13: Entered barcode file has not been found.")
        exit(13)

    # Creates an empty list and dictionary
    barcode_file_list = []
    barcode_file_dict = {}

    # Checks sequencing method to retrieve correct i5 column
    if sequencing_method == 1:
        i5 = 8
    else:
        i5 = 9
    try:
        # Checks spike in parameter
        if analyse_combination == 1:
            # Retrieve barcodes from the Excel file
            for row in sheet.iter_rows(min_row=4, values_only=True):
                barcode_file_list.append([row[0], row[i5] + "+" + row[4]])
            # Returns the barcode_file_list
            return barcode_file_list

        else:
            # Retrieve barcodes and spike-in sequences from the Excel file
            for row in sheet.iter_rows(min_row=4, values_only=True):
                barcode = row[i5] + "+" + row[4]
                barcode_file_dict[barcode] = [row[0], row[-1], 0]
            # Returns the barcode_file_dict
            return barcode_file_dict

    # Returns an error if file format is incorrect
    except IndexError:
        print("Error 14: Barcode file format incorrect.")
        exit(14)
    except TypeError:
        print("Error 15: Barcode file format incorrect.")
        exit(15)


def fastq_reader_with_spike(fastq_path, trimming_ends, trim_i5, trim_i7):
    """
    Reads and saves the info from the .fastq file to a dictionary.
    :param fastq_path: Path to the .fastq file.
    :param trimming_ends: Parameter for the i5 and i7 side of the spike
            sequences.
    :param trim_i5: Parameter to trim the i5 side of the spike sequence.
    :param trim_i7: Parameter to trim the i7 side of the spike sequence.
    :return fastq_data: List with the structure [[i5, i7, sequence],[i5, i7,
            sequence], etc].
    """
    # Creates an empty list
    fastq_data = []

    try:
        # Opens the .fastq and reads it line by line
        with open(fastq_path, "r") as fastq_file:
            for line in fastq_file:

                # If line starts with a @ it retrieves the barcode
                if line.startswith("@"):
                    templist = line.replace("\n", "").split(":")[-1].split("+")

                # Checks if line contains only letters and saves it to a
                # variable
                elif line[:-1].isalpha() and len(templist) > 0:

                    # Checks which sides of the sequence are the i5 and
                    # i7 ends and saves sequence to list
                    if trimming_ends == "2":
                        # Makes sequence reverse and removes the \n
                        line = line.replace("\n", "")[::-1]
                        # Adds sequences to list
                        if trim_i7 == 0:
                            templist.append(line[trim_i5:])
                        else:
                            templist.append(line[trim_i5:-trim_i7])
                    else:
                        templist.append(line[trim_i5:-trim_i7-1])
                    fastq_data.append(templist)

        # Checks if fastq data is empty and returns an error if empty
        if len(fastq_data) == 0:
            print("Error 21: Fasta file format is incorrect. No headers or "
                  "sequences found.")
            exit(21)

        # Returns the fastq list
        return fastq_data

    except FileNotFoundError:
        # Returns an error if fastq file has not been found
        print("Error 22: Entered fastq file has not been found.")
        exit(22)
