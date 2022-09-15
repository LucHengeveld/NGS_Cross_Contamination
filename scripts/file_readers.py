import openpyxl


def bcl_to_fastq(parameters):
    # TODO: Code for converting .bcl to .fastq and its parameters (like min quality)
    # https://support.illumina.com/content/dam/illumina-support/documents/documentation/software_documentation/bcl2fastq/bcl2fastq2-v2-20-software-guide-15051736-03.pdf
    fastq_file = "C:\\Users\\luche\\Desktop\\example.fastq"
    return fastq_file


def fastq_reader(fastq_path):
    """
    Reads and saves the info from the .fastq file to a dictionary.
    :param fastq_path: Path to the .fastq file.
    :return fastq_dict: Dictionary with the structure {barcode, [sequence1,
            sequence2, etc]}.
    """
    # TODO: Increase fastq_reader speed by creating spike in and no spike-in
    #  split in function. No spike-in requires no sequence.
    # TODO: Build in max difference barcode sequence param if spike-in has been
    #  used.

    # Creates an empty dictionary
    fastq_dict = {}

    # Opens the .fastq and reads it line by line
    with open(fastq_path, "r") as fastq_file:
        for line in fastq_file:
            # If line starts with a @ it retrieves the barcode
            if line.startswith("@"):
                barcode = line.split(":")[-1].replace("\n", "")
            # Checks if line consists of only letters
            elif line.replace("\n", "").isalpha():
                # Checks if barcode already exists in dictionary
                if barcode in fastq_dict.keys():
                    # Adds barcode with its sequence to the dictionary
                    fastq_dict[barcode].append(line.replace("\n", ""))
                else:
                    # Appends the sequence to the dictionary
                    fastq_dict[barcode] = [line.replace("\n", "")]

    # Returns the fastq dictionary
    return fastq_dict


def barcode_file_reader(barcode_file, sequencing_method, spike_ins):
    """
    Retrieves the barcodes (and spike in sequences if spike_in parameter is
    '2') from the entered Excel file.
    :param barcode_file: Path to the Excel file.
    :param sequencing_method: Parameter from parameters.txt.
    :param spike_ins: Parameter from parameters.txt.
    :return barcode_file_list: List with all barcodes from the Excel file.
    :return barcode_file_dict: Dictionary with structure {barcode:well, [spike
            seq1, spike seq2, etc]}.
    """
    # Loads in the Excel barcode file
    excel_reader = openpyxl.load_workbook(barcode_file)
    sheet = excel_reader.active

    # Creates an empty list and dictionary
    barcode_file_list = []
    barcode_file_dict = {}

    # Checks sequencing method to retrieve correct i5 column
    if sequencing_method == "1":
        i5 = 8
    else:
        i5 = 9

    # Checks spike in parameter
    if spike_ins == "1":
        # Retrieves barcodes from the Excel file
        for row in sheet.iter_rows(min_row=4, values_only=True):
            barcode_file_list.append(row[i5] + "+" + row[4])

        # Returns the barcode_file_list
        return barcode_file_list

    else:
        # Retrieves barcodes and spike-in sequences from the Excel file
        for row in sheet.iter_rows(min_row=4, values_only=True):
            barcode = row[i5] + "+" + row[4]
            if barcode in barcode_file_dict.keys():
                barcode_file_dict[barcode][1].append(row[-1])
            else:
                barcode_file_dict[barcode] = [row[0], [row[-1]]]

        # Returns the barcode_file_dict
        return barcode_file_dict
