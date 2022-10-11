from scripts import spike_in_contamination as sic

from Levenshtein import distance
import re


def barc_no_spike(fastq_data, diff_bar_nucl, correct_i5_list,
                  correct_i7_list, i5_i7_combinations):
    """
    Checks and counts the different possible i5 + i7 combinations.
    :param fastq_data: List with the structure [barcode 1, barcode2, etc].
    :param diff_bar_nucl: Parameter from settings.py.
    :param correct_i5_list: List with all i5 barcodes from entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from entered barcode
            file.
    :param i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations with as value a 0. Structure: {i5: {i7: 0, i7: 0}}.
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
                    if unknown_i5.get(i5):
                        unknown_i5[i5] += 1
                    else:
                        unknown_i5[i5] = 1

                # If i7 is unknown, adds it to a list
                elif i5 in correct_i5_list and i7 not in correct_i7_list:
                    if unknown_i7.get(i7):
                        unknown_i7[i7] += 1
                    else:
                        unknown_i7[i7] = 1

                # If i5 + i7 both are unknown, it adds the barcode to a list
                else:
                    if barcode in unknown_barcodes:
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
                    if i5 in unknown_i5:
                        unknown_i5[i5] += 1
                    else:
                        unknown_i5[i5] = 1

                # If only i5 matches, adds the i7 barcode to a list
                elif bool_i5 and not bool_i7:
                    if i7 in unknown_i7:
                        unknown_i7[i7] += 1
                    else:
                        unknown_i7[i7] = 1

                # If both i5 and i7 do not match, add both to a list
                else:
                    if barcode in unknown_barcodes:
                        unknown_barcodes[barcode] += 1
                    else:
                        unknown_barcodes[barcode] = 1

    except ValueError:
        print("Error 12: Barcodes have not been found at the end of the "
              "headers in the fastq file.")
        exit(12)

    # Returns i5_i7_combinations and unknown_barcodes to main function
    return i5_i7_combinations, unknown_barcodes, unknown_i5, unknown_i7


def barc_with_spike(combinations, correct_spike_list, correct_i5_list,
                    correct_i7_list, fastq_data, diff_bar_nucl, diff_seq_nucl,
                    analyse_combination):
    """
    Compares all fastq barcodes and spike-ins sequences to the barcode and
    spike-ins sequence file.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination. Structure depends on spike-ins
            parameter.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param fastq_data: List with the structure [[i5, i7, sequence],[i5, i7,
            sequence], etc].
    :param diff_bar_nucl: Parameter from settings.py.
    :param diff_seq_nucl: Parameter from settings.py.
    :param analyse_combination: Parameter from settings.py.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    """
    # List of all possible unknown barcode / spike-in sequence
    # combinations
    unknown_keys = ["i5", "i7", "spike", "i5_i7", "i5_spike", "i7_spike",
                    "i5_i7_spike"]

    # Loops through the possible unknown combinations and adds these to
    # a dictionary
    unknown_dict = {}
    for key in unknown_keys:
        unknown_dict[key] = {}

    # Loops through the fastq data list
    for read in fastq_data:

        # Saves the spike-in sequence as variable
        spike_seq = read[2]

        # Checks if spike-ins parameter has value 2 (i5+spike) or 3
        # (i7+spike)
        if analyse_combination in [2, 3]:
            if analyse_combination == 2:
                # Saves the i5 barcode and correct barcode list to a
                # variable
                barcode = read[0]
                bar_type = "i5"
                correct_bar_list = correct_i5_list

            else:
                # Saves the i7 barcode and correct barcode list to a
                # variable
                barcode = read[1]
                bar_type = "i7"
                correct_bar_list = correct_i7_list

            # Checks if barcode nucleotides are allowed to differ
            if diff_bar_nucl == 0:

                # Calls correct functions depending on diff_bar_nucl and
                # diff_seq_nucl parameters
                if diff_seq_nucl == 0:
                    # Bar diff = 0 and seq diff = 0
                    unknown_dict, combinations = sic.bar_spike(
                        barcode, bar_type, combinations, spike_seq,
                        unknown_dict, correct_bar_list, correct_spike_list)
                else:
                    # Bar diff = 0 and seq diff != 0
                    unknown_dict, combinations = sic.bar_spike_seq_diff(
                        barcode, bar_type, combinations, spike_seq,
                        unknown_dict, correct_bar_list, correct_spike_list,
                        diff_seq_nucl)

            # Calls correct functions depending on diff_bar_nucl and
            # diff_seq_nucl parameters
            elif diff_seq_nucl == 0:

                # Bar diff != 0 and seq diff = 0
                unknown_dict, combinations = sic.bar_spike_bar_diff(
                    barcode, bar_type, combinations, spike_seq, unknown_dict,
                    correct_bar_list, correct_spike_list, diff_bar_nucl)

            else:
                # Bar diff != 0 and seq diff != 0
                unknown_dict, combinations = sic.bar_spike_bar_seq_diff(
                    barcode, bar_type, combinations, spike_seq, unknown_dict,
                    correct_bar_list, correct_spike_list, diff_bar_nucl,
                    diff_seq_nucl)

        # Calls the i5+i7+spike-ins functions
        else:

            # Saves the i5+i7 barcode to a variable
            barcode = [read[0], read[1]]

            # Calls correct functions depending on diff_bar_nucl and
            # diff_seq_nucl parameters
            if diff_bar_nucl == 0:
                if diff_seq_nucl == 0:

                    # Bar diff = 0 and seq diff = 0
                    unknown_dict, combinations = sic.i5_i7_spike(
                        barcode, combinations, spike_seq, unknown_dict,
                        correct_i5_list, correct_i7_list, correct_spike_list)

                else:
                    # Bar diff = 0 and seq diff != 0
                    unknown_dict, combinations = sic.i5_i7_spike_seq_diff(
                        barcode, combinations, spike_seq, unknown_dict,
                        correct_i5_list, correct_spike_list, diff_seq_nucl)

            # Calls correct functions depending on diff_bar_nucl and
            # diff_seq_nucl parameters
            elif diff_seq_nucl == 0:

                # Bar diff != 0 and seq diff = 0
                unknown_dict, combinations = sic.i5_i7_spike_bar_seq_diff(
                    barcode, combinations, spike_seq, unknown_dict,
                    correct_i5_list, correct_spike_list, diff_bar_nucl,
                    diff_seq_nucl)

            else:
                # Bar diff != 0 and seq diff != 0
                unknown_dict, combinations = sic.i5_i7_spike_bar_diff(
                    barcode, combinations, spike_seq, unknown_dict,
                    correct_i5_list, correct_spike_list, diff_bar_nucl)

    # Returns a dictionary containing all unknown i5/i7/spike-in
    # combinations and a dictionary containing all known combinations
    # and their occurrence
    return unknown_dict, combinations


def retrieve_combinations_no_spike(barcode_file_list):
    """
    Creates a dictionary with all possible barcode combinations.
    :param barcode_file_list: List with all barcodes from the Excel file.
    :return correct_i5_list: List with all i5 barcodes from entered barcode
            file.
    :return correct_i7_list: List with all i7 barcodes from entered barcode
            file.
    :return i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations with as value a 0. Structure: {i5: {i7: 0, i7: 0}}.
    """
    # Creates empty lists
    correct_i5_list = []
    correct_i7_list = []

    # Splits the barcodes from the Excel file into i5 and i7
    for line in barcode_file_list:
        i5, i7 = line[1].split("+")
        correct_i5_list.append(i5)
        correct_i7_list.append(i7)

    # Creates an empty dictionary
    i5_i7_combinations = {}

    # Creates a dictionary with every possible i5 + i7 combination and
    # set the amount of occurrences to 0
    for i5 in correct_i5_list:
        for i7 in correct_i7_list:
            if i5 not in i5_i7_combinations:
                i5_i7_combinations[i5] = {i7: 0}
            else:
                i5_i7_combinations[i5][i7] = 0

    # Returns the correct barcode lists and i5_i7_combinations dict
    return correct_i5_list, correct_i7_list, i5_i7_combinations


def retrieve_combinations_with_spike(barcode_file_dict, analyse_combination):
    """
    Creates a dictionary with all possible barcode combinations.
    :param barcode_file_dict: List with all barcodes from the Excel file.
    :param analyse_combination: Parameter from settings.py.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination. Structure depends on spike-ins
            parameter.
    :return correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :return correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :return correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    """
    # Creates empty lists
    correct_i5_list = []
    correct_i7_list = []
    correct_spike_list = []
    well_locations = []

    # Splits the barcodes from the Excel file into i5 and i7
    for barcode in barcode_file_dict:
        i5, i7 = barcode.split("+")
        correct_i5_list.append(i5)
        correct_i7_list.append(i7)
        correct_spike_list.append(barcode_file_dict[barcode][1])
        well_locations.append(barcode_file_dict[barcode][0])

    # Creates empty dictionary
    combinations = {}

    # Creates a dictionary with every possible combination and set the
    # amount of occurrences to 0
    if analyse_combination in [2, 3]:

        # Use correct list depending on spike_ins parameter
        if analyse_combination == 2:
            correct_barcode_list = correct_i5_list
        else:
            correct_barcode_list = correct_i7_list

        # Saves the i5 + spike-in or i7 + spike-in combinations to a
        # dictionary
        for barcode in correct_barcode_list:
            for spike_seq in correct_spike_list:
                if barcode not in combinations:
                    combinations[barcode] = {spike_seq: 0}
                else:
                    combinations[barcode][spike_seq] = 0

    else:
        # Saves the i5 / i7 / spike-in sequence combinations to a
        # dictionary
        for bar_index in range(len(correct_i5_list)):
            for spike_seq in correct_spike_list:
                barcode = correct_i5_list[bar_index] + "+" + correct_i7_list[
                    bar_index]
                if barcode not in combinations:
                    combinations[barcode] = {spike_seq: 0}
                else:
                    combinations[barcode][spike_seq] = 0

    # Returns the combinations dict and correct i5, i7 and spike
    # sequence lists
    return combinations, correct_spike_list, correct_i5_list, correct_i7_list, well_locations


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
        i5_loc = re.split("(\d+)", barcode[0])[0]
        i7_loc = re.split("(\d+)", barcode[0])[1]
        i5_bar, i7_bar = barcode[1].split("+")

        # Adds the barcodes and their well locations to the dictionary
        if i5_bar not in i5_i7_loc:
            i5_i7_loc[i5_bar] = [i5_loc, {i7_bar: i7_loc}]
        else:
            i5_i7_loc[i5_bar][1].update({i7_bar: i7_loc})

    # Returns the i5_i7_loc dictionary
    return i5_i7_loc
