from Levenshtein import distance
import re


def barc_no_spike(barcode_file_data, fastq_data, diff_bar_nucl,
                  correct_i5_list, correct_i7_list, i5_i7_combinations):
    # TODO: Add last 3 params to docstring
    """
    Checks and counts the different possible i5 + i7 combinations.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :param fastq_data: List with the structure [barcode 1, barcode2, etc].
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :return unknown_barcodes: Dictionary with all unknown barcode combinations
            from the fastq file.
    :return unknown_i5: Dictionary with all unknown i5 barcodes from the fastq
            file.
    :return unknown_i7: Dictionary with all unknown i7 barcodes from the fastq
            file.
    """
    # TODO: Split function into smaller ones
    # TODO: Filter out unknown barcodes that contain homopolymers (AAAA etc)
    # Creates an empty list
    unknown_barcodes = {}
    unknown_i5 = {}
    unknown_i7 = {}

    try:
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
                elif i5 not in correct_i5_list and i7 in correct_i7_list:
                    if i5 in unknown_i5.keys():
                        unknown_i5[i5] += 1
                    else:
                        unknown_i5[i5] = 1

                # If i7 is unknown, adds it to a list
                elif i5 in correct_i5_list and i7 not in correct_i7_list:
                    if i7 in unknown_i7.keys():
                        unknown_i7[i7] += 1
                    else:
                        unknown_i7[i7] = 1

                # If i5 + i7 both are unknown, it adds the barcode to a list
                else:
                    if barcode in unknown_barcodes.keys():
                        unknown_barcodes[barcode] += 1
                    else:
                        unknown_barcodes[barcode] = 1

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
                    if i5 in unknown_i5.keys():
                        unknown_i5[i5] += 1
                    else:
                        unknown_i5[i5] = 1

                # If only i5 matches, adds the i7 barcode to a list
                elif bool_i5 and not bool_i7:
                    if i7 in unknown_i7.keys():
                        unknown_i7[i7] += 1
                    else:
                        unknown_i7[i7] = 1

                # If both i5 and i7 do not match, add both to a list
                else:
                    if barcode in unknown_barcodes.keys():
                        unknown_barcodes[barcode] += 1
                    else:
                        unknown_barcodes[barcode] = 1
    except ValueError:
        print("Error 12: Barcodes have not been found at the end of the "
              "headers in the fastq file.")
        exit(12)

    # Returns i5_i7_combinations and unknown_barcodes to main function
    return i5_i7_combinations, unknown_barcodes, unknown_i5, unknown_i7


def barc_with_spike(barcode_file_data, fastq_data, diff_bar_nucl,
                    diff_spike_nucl):
    # TODO: Docstrings and comments
    # output: list with dictionaries [i5+i7+spike, i5+spike, i7+spike, unknown barcodes/spike ins etc]
    output_dicts = ["i5_i7_spike", "i5_spike", "i7_spike", "unknown_i5",
                    "unknown_i7", "unknown_spike", "Unknown_i5_i7",
                    "unknown_i5_spike", "unknown_i7_spike",
                    "unknown_i5_i7_spike"]
    output_data = {}
    for dict_name in output_dicts:
        output_data[dict_name] = None
    print(output_data)

    # eerste 3 opslaan als dicts want barcodes en sequenties bekend,
    # rest als lijsten want barcodes en sequenties onbekend
    pass


def retrieve_correct_barcodes_combinations(barcode_file_data):
    # TODO: Docstrings
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

    return correct_i5_list, correct_i7_list, i5_i7_combinations


def retrieve_barcode_location(barcode_file_data):
    """
    Retrieves the well locations of the barcodes from the combinatorial
    indexing plate.
    :param barcode_file_data: List with all barcodes from the Excel file.
    :return i5_i7_loc: Dictionary containing the i5 and i7 barcodes with their
            corresponding well locations. Dictionary has the structure:
            {i5: ["A" {i7: 1, i7: 2}]}
    """
    # Creates an empty dictionary
    i5_i7_loc = {}

    # Loops through the barcodes from the entered barcode Excel file
    for barcode in barcode_file_data:
        i5_loc = re.split('(\d+)', barcode[0])[0]
        i7_loc = re.split('(\d+)', barcode[0])[1]
        i5_bar, i7_bar = barcode[1].split("+")

        # Adds the barcodes and their well locations to the dictionary
        if i5_bar not in i5_i7_loc:
            i5_i7_loc[i5_bar] = [i5_loc, {i7_bar: i7_loc}]
        else:
            i5_i7_loc[i5_bar][1].update({i7_bar: i7_loc})

    # Returns the i5_i7_loc dictionary
    return i5_i7_loc
