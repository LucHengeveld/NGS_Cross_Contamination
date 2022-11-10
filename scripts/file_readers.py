# Imports the required modules
import openpyxl


def fastq_reader_no_spike(fastq_path, umi_length):
    """
    Reads and saves the info from the .fastq file to a list.
    :param fastq_path: Path to the .fastq file.
    :param umi_length: Length of the unique molecular identifier. Entered by
        user in settings.py.
    :return fastq_data: List with the structure [barcode 1, barcode2, etc].
    """
    # Creates an empty list and set
    fastq_data = []
    umi_set = set()

    # TODO: Save homopolymers to seperate list
    homopolymers = ["AAA", "TTT", "GGG", "CCC"]
    try:
        # Opens the .fastq and reads it line by line
        with open(fastq_path, "r") as fastq_file:
            # Checks if the user used UMIs
            if umi_length == 0:
                for line in fastq_file:
                    # If line starts with a @ it retrieves the barcode
                    if line.startswith("@") and "N" not in line.split(":")[-1]:
                        if not any(homopolymer in line.split(":")[-1] for
                                   homopolymer in homopolymers):
                            fastq_data.append(line.replace("\n", "").split(":")[-1])
            else:
                for line in fastq_file:
                    # If line starts with a @ it retrieves the barcode
                    if line.startswith("@") and "N" not in line.split(":")[-1]:
                        # Retrieves the UMI sequence from the header
                        umi = line.replace("\n", "").split(":")[-1].\
                            split("+")[0][-umi_length:]
                        # Adds the barcodes to a list if UMI has not
                        # been found in previous reads
                        if umi not in umi_set:
                            umi_set.add(umi)
                            fastq_data.append(line.replace("\n", "").
                                              split(":")[-1].
                                              replace(umi+"+", "+"))

        if len(fastq_data) == 0:
            print("Error 15: Fasta file format is incorrect. No headers "
                  "found.")
            exit(15)

        # Returns the fastq list
        return fastq_data

    except FileNotFoundError:
        print("Error 16: Entered fastq file has not been found.")
        exit(16)


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
        print("Error 17: Entered barcode file has not been found.")
        exit(17)

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
                barcode_file_list.append([row[0], row[4] + "+" + row[i5]])
            # Returns the barcode_file_list
            return barcode_file_list

        else:
            # Retrieve barcodes and spike-in sequences from the Excel file
            for row in sheet.iter_rows(min_row=4, values_only=True):
                barcode = row[4] + "+" + row[i5]
                barcode_file_dict[barcode] = [row[0], row[-1], 0]
            # Returns the barcode_file_dict
            return barcode_file_dict

    # Returns an error if file format is incorrect
    except IndexError or TypeError:
        print("Error 18: Barcode file format incorrect.")
        exit(18)


def fastq_reader_with_spike(fastq_path, trim_left, trim_right, umi_length):
    """
    Reads and saves the info from the .fastq file to a dictionary.
    :param fastq_path: Path to the .fastq file.
    :param trim_left: Parameter to trim the left side of the spike sequence.
    :param trim_right: Parameter to trim the right side of the spike sequence.
    :param umi_length: Length of the unique molecular identifier. Entered by
        user in settings.py.
    :return fastq_data: List with the structure [[i5, i7, sequence], [i5, i7,
            sequence], etc].
    """
    # Creates an empty list amd set
    fastq_data = []
    umi_set = set()

    try:
        # Opens the .fastq and reads it line by line
        with open(fastq_path, "r") as fastq_file:
            # Checks if the user used UMIs
            if umi_length == 0:
                for line in fastq_file:
                    # If line starts with a @ it retrieves the barcode
                    if line.startswith("@") and "N" not in line.split(":")[-1]:
                        templist = line.replace("\n", "").split(":")[-1].\
                            split("+")

                    # Checks if line contains only letters and saves it to a
                    # variable
                    elif line[:-1].isalpha() and len(templist) > 0:

                        # Saves the sequence to list
                        templist.append(line[trim_left:-trim_right-1])
                        fastq_data.append(templist)
            else:
                umi_bool = False
                for line in fastq_file:
                    # If line starts with a @ it retrieves the barcode
                    if line.startswith("@") and "N" not in line.split(":")[-1]:
                        templist = line.replace("\n", "").split(":")[-1].\
                            split("+")
                        # Checks if UMI has been found in previous reads
                        if templist[0][-umi_length:] in umi_set:
                            umi_bool = True
                        else:
                            umi_bool = False
                            # Adds the UMI sequence to a set
                            umi_set.add(templist[0][-umi_length:])
                            templist[0] = templist[0][:-umi_length]
                    elif not umi_bool:
                        # Checks if line contains only letters and saves it to
                        # a variable
                        if line[:-1].isalpha() and len(templist) > 0:

                            # Saves the sequence to list
                            templist.append(line[trim_left:-trim_right - 1])
                            fastq_data.append(templist)
        # Checks if fastq data is empty and returns an error if empty
        if len(fastq_data) == 0:
            print("Error 19: Fasta file format is incorrect. No headers or "
                  "sequences found.")
            exit(19)

        # Returns the fastq list
        return fastq_data

    except FileNotFoundError:
        # Returns an error if fastq file has not been found
        print("Error 20: Entered fastq file has not been found.")
        exit(20)
