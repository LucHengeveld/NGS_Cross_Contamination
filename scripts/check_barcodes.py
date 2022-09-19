from Levenshtein import distance


def barc_no_spike(barcode_file_data, fastq_data, diff_bar_nucl):
    """
    Checks and counts the different possible i5 + i7 combinations.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :param fastq_data: List with the structure [barcode 1, barcode2, etc].
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :return unknown_barcodes: List with all unknown barcode combinations from
            the fastq file.
    """
    # Creates empty lists
    correct_i5_list = []
    correct_i7_list = []

    # Splits the barcodes from the Excel file into i5 and i7
    for line in barcode_file_data:
        i5, i7 = line[1].split("+")
        correct_i5_list.append(i5)
        correct_i7_list.append(i7)

    # Creates an empty dictionary
    i5_i7_combinations = {}

    # Creates a dictionary with every possible i5 + i7 combination and
    # set the amount of occurrences to 0
    for i5 in correct_i5_list:
        for i7 in correct_i7_list:
            if i5 not in i5_i7_combinations.keys():
                i5_i7_combinations[i5] = {i7: 0}
            else:
                i5_i7_combinations[i5][i7] = 0

    # Creates an empty list
    unknown_barcodes = []
    unknown_i5 = []
    unknown_i7 = []

    # Checks if the barcode sequence is allowed to differ from the ones
    # in the barcode Excel file. If it is not allowed to differ:
    if diff_bar_nucl == "0":

        # Loops through the barcodes from the fastq file
        for barcode in fastq_data:
            i5, i7 = barcode.split("+")
            # If the i5 and i7 barcode exist in Excel file, increases the
            # occurrences counter of that specific barcode with 1
            if i5 in correct_i5_list and i7 in correct_i7_list:
                i5_i7_combinations[i5][i7] += 1

            # If i5 is unknown, adds it to a list
            elif i5 not in correct_i5_list:
                unknown_i5.append(i5)

            # If i7 is unknown, adds it to a list
            elif i7 not in correct_i7_list:
                unknown_i7.append(i7)

            # If i5 + i7 both are unknown, it adds the barcode to a list
            else:
                unknown_barcodes.append(barcode)

    # If barcode sequence is allowed to differ:
    else:
        # Loops through the barcodes from the fastq file
        for barcode in fastq_data:
            i5, i7 = barcode.split("+")
            bool_i5 = False
            bool_i7 = False

            # Loops through the correct i5 barcodes and checks if it
            # matches the one from the fastq file
            for correct_i5 in correct_i5_list:
                if distance(i5, correct_i5) <= int(diff_bar_nucl):
                    i5 = correct_i5
                    bool_i5 = True

            # Loops through the correct i7 barcodes and checks if it
            # matches the one from the fastq file
            for correct_i7 in correct_i7_list:
                if distance(i7, correct_i7) <= int(diff_bar_nucl):
                    i7 = correct_i7
                    bool_i7 = True

            # If both i5 and i7 match, it increases the barcode counter
            if bool_i5 and bool_i7:
                i5_i7_combinations[i5][i7] += 1

            # If only i7 matches, adds the i5 barcode to a list
            elif not bool_i5 and bool_i7:
                unknown_i5.append(i5)

            # If only i5 matches, adds the i7 barcode to a list
            elif bool_i5 and not bool_i7:
                unknown_i7.append(i7)

            # If both i5 and i7 do not match, add both to a list
            else:
                unknown_barcodes.append(barcode)

    # Returns i5_i7_combinations and unknown_barcodes to main function
    return i5_i7_combinations, unknown_i5, unknown_i7, unknown_barcodes


def retrieve_barcode_location(barcode_file_data):
    # TODO: Docstrings and comments
    i5_i7_loc = {}
    for barcode in barcode_file_data:
        i5_loc = barcode[0][0]
        i7_loc = barcode[0][1]
        i5_bar, i7_bar = barcode[1].split("+")
        if i5_bar not in i5_i7_loc:
            i5_i7_loc[i5_bar] = [i5_loc, {i7_bar: i7_loc}]
        else:
            i5_i7_loc[i5_bar][1].update({i7_bar: i7_loc})
    return i5_i7_loc
