from Levenshtein import distance


def barc_no_spike(fastq_dict, barcode_file_data, diff_bar_nucl):
    """
    Checks if found barcode exists in the original barcodes file.
    :param fastq_dict: Dictionary with the structure {barcode, [sequence1,
            sequence2, etc]}.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return unknown_barcodes: List with all fastq barcodes that have not been
    found in the original barcode Excel file.
    """
    # Creates an empty list
    unknown_barcodes = []
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
            # Adds barcode to list if is has not been found
            unknown_barcodes.append(fastq_barcode)

    # Returns the unknown barcodes
    return unknown_barcodes, correct_barcodes


def uni_barc_no_spike(fastq_dict, barcode_file_data, diff_bar_nucl,
                      unknown_barcodes):
    # TODO: Docstrings / comments
    # structure {found barcode: [original i5 barcode combination,
    # original i7 barcode combination]}
    correct_i5 = []
    correct_i7 = []
    incorrect_combinations = []
    unknown_i5 = []
    unknown_i7 = []

    # Split the barcodes into separate i5 and i7
    unknown_i5_i7 = [barcode.split("+") for barcode in unknown_barcodes]

    for barcode in barcode_file_data:
        correct_i5.append(barcode.split("+")[0])
        correct_i7.append(barcode.split("+")[1])

    unknown_barcodes.clear()

    for unknown_combination in unknown_i5_i7:
        i5 = unknown_combination[0]
        i7 = unknown_combination[1]
        if i5 in correct_i5:
            if i7 in correct_i7:
                # print("Both i5 and i7 have been found. Barcodes do not match.", i5, i7)
                incorrect_combinations.append([i5, i7])
            else:
                # print("i7 is unknown:", i7, i5+"+"+i7)
                unknown_i7.append([i5, i7])
        elif i7 in correct_i7:
            # print("i5 is unknown:", i5, i5+"+"+i7)
            unknown_i5.append([i5, i7])
        else:
            # print("i5", i5, "and i7", i7, "are unknown.")
            unknown_barcodes.append([i5, i7])

    return incorrect_combinations, unknown_barcodes, unknown_i5, unknown_i7, correct_i5, correct_i7
