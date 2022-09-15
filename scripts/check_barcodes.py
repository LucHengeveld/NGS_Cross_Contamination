from Levenshtein import distance


def comb_barc_no_spike(fastq_dict, barcode_file_data, diff_bar_nucl):
    """
    Checks if found barcode exists in the original barcodes file.
    :param fastq_dict: Dictionary with the structure {barcode, [sequence1,
            sequence2, etc]}.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return unknown_barcodes: Dictionary with all fastq barcodes that have not
            been found in the original barcode Excel file.
            Structure: {barcode: occurrences}.
    :return correct_barcodes: Dictionary with all barcodes from the original
            barcode Excel file and the amount of times they have been found in the
            fastq file. Structure: {barcode: occurrences}.
    """
    # TODO: Check if barcode i5+i7 are mismatched or if one of them contains
    #  unknown barcode (like in def uniq_barc_no_spike)
    # TODO: Add parameter to enable or disable the diff_bar_nucl param, speed
    #  increases if distance function is not used
    # Creates an empty list
    unknown_barcodes = {}
    correct_barcodes = {}
    for barcode in barcode_file_data:
        correct_barcodes[barcode] = 0

    # Loops through the found fastq barcodes
    for fastq_barcode in fastq_dict.keys():
        counter = 0
        # Loops through the list with original barcodes
        for original_barcode in barcode_file_data:
            # Checks if barcodes are similar to each other
            if distance(fastq_barcode, original_barcode) <= int(diff_bar_nucl):
                counter += 1
                correct_barcodes[original_barcode] += 1
        if counter == 0:
            # Adds barcode and counter to dictionary if is has not been
            # found
            if fastq_barcode in unknown_barcodes.keys():
                unknown_barcodes[fastq_barcode] += 1
            else:
                unknown_barcodes[fastq_barcode] = 1

    # Returns the unknown_barcodes and correct_barcodes
    return unknown_barcodes, correct_barcodes


def uniq_barc_no_spike(barcode_file_data, fastq_dict, diff_bar_nucl):
    """
    Checks and counts the different possible i5 + i7 combinations.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :param fastq_dict: Dictionary with the structure {barcode, [sequence1,
            sequence2, etc]}.
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :return unknown_barcodes: List with all unknown barcode combinations from
            the fastq file.
    """
    # TODO: Possible improvement: split unknown barcodes into unknown i5,
    #  unknown i7 and both unknown. Add difference nucleotide barcode param.
    # Creates empty lists
    correct_i5 = []
    correct_i7 = []

    # Splits the barcodes from the excel file into i5 and i7
    for barcode in barcode_file_data:
        i5, i7 = barcode.split("+")
        correct_i5.append(i5)
        correct_i7.append(i7)

    # Creates an empty dictionary
    i5_i7_combinations = {}

    # Creates a dictionary with every possible i5 + i7 combination and
    # set the amount of occurrences to 0
    for i5 in correct_i5:
        for i7 in correct_i7:
            if i5 not in i5_i7_combinations.keys():
                i5_i7_combinations[i5] = {i7: 0}
            else:
                i5_i7_combinations[i5][i7] = 0

    # Creates an empty list
    unknown_barcodes = []

    # Checks if found i5 and i7 barcodes exist in Excel file
    for barcode in fastq_dict.keys():
        i5, i7 = barcode.split("+")
        # If the i5 and i7 barcode exist in Excel file, increases the
        # occurrences counter of that specific barcode with 1
        if i5 in correct_i5 and i7 in correct_i7:
            i5_i7_combinations[i5][i7] += 1
        else:
            # If i5 + i7 combination is unknown, it adds the barcode to
            # a list
            unknown_barcodes.append(barcode)

    # Returns i5_i7_combinations and unknown_barcodes to main function
    return i5_i7_combinations, unknown_barcodes
