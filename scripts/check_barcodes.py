# Imports the other python scripts

# Imports the required modules
from Levenshtein import distance
import re


def comp_barcodes(fastq_data, barc_diff, correct_i5_list, correct_i7_list,
                  i5_i7_combinations):
    """
    Compares the i5 and i7 barcodes from the fastq file to the ones from the
    entered barcode file.
    :param fastq_data: List with the structure [barcode 1, barcode2, etc].
    :param barc_diff: Parameter from settings.py.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations with as value a 0. Structure: {i5: {i7: 0, i7: 0}}.
    :return i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :return unknown_barcodes: Dictionary with all unknown barcode combinations
            from the fastq file.
    """
    # Creates a empty dictionary
    unknown_barcodes = {}

    # Loops through the barcodes from the fastq file
    for barcode in fastq_data:
        i5, i7 = barcode.split("+")

        # Checks if the barcode from the fastq file exists in the
        # entered barcode file
        i5_bool, i5 = seq_checker(correct_i5_list, i5, barc_diff)
        i7_bool, i7 = seq_checker(correct_i7_list, i7, barc_diff)

        # If both barcodes exist, counts up the value by 1
        if i5_bool and i7_bool:
            i5_i7_combinations[i5][i7] += 1
        else:
            # Adds the unknown barcode combinations to a dictionary
            if i5 in unknown_barcodes:
                if i7 in unknown_barcodes[i5]:
                    unknown_barcodes[i5][i7][2] += 1
                else:
                    unknown_barcodes[i5].update({i7: [i5_bool, i7_bool, 1]})
            else:
                unknown_barcodes[i5] = {i7: [i5_bool, i7_bool, 1]}

    # Returns dictionaries with the known and unknown barcode
    # combinations
    return i5_i7_combinations, unknown_barcodes


def comp_bar_spike(combinations, correct_spike_list, correct_i5_list,
                   correct_i7_list, fastq_data, barc_diff, spike_diff,
                   analyse_combination):
    """
    Compares the i5, i7 and spike-in sequences from the fastq file to the ones
    from the entered barcode + spike-in file.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination. Structure depends on spike-ins
            parameter.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param fastq_data: List with the structure [[i5, i7, sequence], [i5, i7,
            sequence], etc].
    :param barc_diff: Parameter from settings.py.
    :param spike_diff: Parameter from settings.py.
    :param analyse_combination: Parameter from settings.py.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """

    # Creates an empty dictionary
    unknown_dict = {}

    # Loops through the fastq data
    for read in fastq_data:
        # Checks if found spike-in sequence exist in barcode + spike-in
        # file
        spike_bool, spike = seq_checker(correct_spike_list, read[2],
                                        spike_diff)

        # If analyse combination is i5 + spike-in
        if analyse_combination == 2:
            # Checks if found i5 barcode exist in barcode + spike-in
            # file
            i5_bool, i5 = seq_checker(correct_i5_list, read[0], barc_diff)

            # Adds the i5 and spike-in to the combinations or unknown
            # dictionary
            combinations, unknown_dict = add_barc_spike(
                i5_bool, i5, spike_bool, spike, combinations, unknown_dict)

        # If analyse combination is i7 + spike-in
        elif analyse_combination == 3:
            # Checks if found i7 barcode exist in barcode + spike-in
            # file
            i7_bool, i7 = seq_checker(correct_i7_list, read[1], barc_diff)

            # Adds the i7 and spike-in to the combinations or unknown
            # dictionary
            combinations, unknown_dict = add_barc_spike(
                i7_bool, i7, spike_bool, spike, combinations, unknown_dict)

        # If analyse combination is i5 + spike-in and i7 + spike-in
        else:
            # Checks if found i5 and i7 barcodes exist in barcode + spike-in
            # file
            i5_bool, i5 = seq_checker(correct_i5_list, read[0], barc_diff)
            i7_bool, i7 = seq_checker(correct_i7_list, read[1], barc_diff)

            # Adds the barcodes and spike-in sequence to the
            # combinations or unknown dictionary
            combinations, unknown_dict = add_both_barc_spike(
                i5_bool, i5, i7_bool, i7, spike_bool, spike, combinations,
                unknown_dict)

    # Returns dictionaries with the known and unknown barcode
    # combinations
    return combinations, unknown_dict


def add_barc_spike(barc_bool, barc, spike_bool, spike, combinations,
                   unknown_dict):
    """
    Adds the barcode and spike-in sequence to the combinations or unknown_dict
    dictionaries.
    :param barc_bool: Boolean, true if barcode exists in barcode file.
    :param barc: i5 or i7 barcode.
    :param spike_bool: Boolean, true if spike-in exists in barcode file.
    :param spike: Spike-in sequence.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """
    # Checks if the barcode and spike booleans are true
    if barc_bool and spike_bool:
        # Counts up combination value
        combinations[barc][spike] += 1

    # If barcode or spike boolean is false, adds them to the unknown
    # dictionary
    elif barc in unknown_dict:
        if spike in unknown_dict[barc]:
            unknown_dict[barc][spike][2] += 1
        else:
            unknown_dict[barc].update({spike: [barc_bool,
                                               spike_bool, 1]})
    else:
        unknown_dict[barc] = {spike: [barc_bool, spike_bool, 1]}

    # Returns dictionaries with the known and unknown barcode
    # combinations
    return combinations, unknown_dict


def add_both_barc_spike(i5_bool, i5, i7_bool, i7, spike_bool, spike,
                        combinations, unknown_dict):
    """
    Adds both the i5+spike and i7+spike sequences to the combinations or
    unknown_dict dictionaries.
    :param i5_bool: Boolean, true if i5 exists in barcode file.
    :param i5: i5 barcode sequence.
    :param i7_bool: Boolean, true if i5 exists in barcode file.
    :param i7: i7 barcode sequence.
    :param spike_bool: Boolean, true if spike-in exists in barcode file.
    :param spike: Spike-in sequence.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """
    # Checks if the i5 and spike booleans are true
    if spike_bool and i5_bool:
        #         # Counts up combination value
        combinations[i5][spike] += 1

    # Checks if the i7 and spike booleans are true
    if spike_bool and i7_bool:
        # Counts up combination value
        combinations[i7][spike] += 1

    # If barcode or spike boolean is false, adds them to the unknown
    # dictionary
    if not i5_bool or not i7_bool:
        if i5 in unknown_dict:
            if i7 in unknown_dict[i5]:
                if spike in unknown_dict[i5][i7]:
                    unknown_dict[i5][i7][spike][-1] += 1
                else:
                    unknown_dict[i5][i7].update(
                        {spike: [i5_bool, i7_bool, spike_bool, 1]})
            else:
                unknown_dict[i5].update(
                    {i7: {spike: [i5_bool, i7_bool, spike_bool, 1]}})

        else:
            unknown_dict[i5] = {i7: {spike: [i5_bool, i7_bool, spike_bool, 1]}}

    return combinations, unknown_dict


def comp_i5_i7_spike(combinations, correct_spike_list, correct_i5_list,
                     correct_i7_list, fastq_data, barc_diff, spike_diff,
                     indexing):
    """

    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param fastq_data: List with the structure [[i5, i7, sequence], [i5, i7,
            sequence], etc].
    :param barc_diff: Parameter from settings.py.
    :param spike_diff: Parameter from settings.py.
    :param indexing: Parameter of the used indexing method.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """
    # Creates an empty dictionary
    unknown_dict = {}

    # Loops through the fastq data
    for read in fastq_data:

        # Checks if found spike-in sequence exist in barcode + spike-in
        # file
        spike_bool, spike = seq_checker(correct_spike_list, read[2],
                                        spike_diff)

        # Checks if indexing parameter is combinatorial
        if indexing == 1:
            # Checks if the i5 and i7 sequences exist in the entered
            # barcode file
            i5_bool, i5 = seq_checker(correct_i5_list, read[0], barc_diff)
            i7_bool, i7 = seq_checker(correct_i7_list, read[1], barc_diff)

            # Checks if the barcodes and spike booleans are true
            if i5_bool and i7_bool and spike_bool:
                barc = i5 + "+" + i7
                # Counts up combination value
                combinations[barc][spike] += 1
            else:
                # Saves unknown barcodes to a dictionary
                unknown_dict = write_unknown_i5_i7_spike(unknown_dict, i5, i7,
                                                         spike, i5_bool,
                                                         i7_bool, spike_bool)

        # If entered indexing parameter is unique indexing
        else:
            # Checks if the i5 and i7 sequences exist in the entered
            # barcode file
            bar_bool, barcode = seq_checker_uniq_i5_i7_spike(
                correct_i5_list, correct_i7_list, read[0], read[1], barc_diff)

            # Saves the i5 and i7 barcodes as variables
            i5, i7 = barcode.split("+")

            # Checks if the barcodes and spike booleans are true
            if bar_bool and spike_bool:
                # Counts up combination value
                combinations[barcode][spike] += 1
            else:
                unknown_dict = write_unknown_i5_i7_spike(unknown_dict, i5, i7,
                                                         spike, bar_bool,
                                                         bar_bool, spike_bool)

    # Returns the updated combinations and unknown dictionaries
    return combinations, unknown_dict


def write_unknown_i5_i7_spike(unknown_dict, i5, i7, spike, i5_bool, i7_bool,
                              spike_bool):
    """
    Saves the unknown i5, i7 and spike-in sequences in the unknown dictionary.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param i5: i5 barcode sequence.
    :param i7: i7 barcode sequence.
    :param spike: Spike-in sequence
    :param i5_bool: Boolean, true if i5 exists in barcode file.
    :param i7_bool: Boolean, true if i5 exists in barcode file.
    :param spike_bool: Boolean, true if spike-in exists in barcode file.
    :param spike: Spike-in sequence.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """
    # Checks if the i5, i7 or spike-in sequences already exist in the
    # unknown dictionary
    if i5 in unknown_dict:
        if i7 in unknown_dict[i5]:
            if spike in unknown_dict[i5][i7]:

                # Counts up occurrences by 1 if i5, i7 and spike-in
                # exist in dictionary.
                unknown_dict[i5][i7][spike][3] += 1

            else:
                # Updates the unknown dictionary if i5 and i7 exist in
                # dictionary.
                unknown_dict[i5][i7].update({spike: [i5_bool, i7_bool,
                                                     spike_bool, 1]})
        else:
            # Updates the unknown dictionary if only i5 exist in
            # dictionary.
            unknown_dict[i5].update({i7: {spike: [i5_bool, i7_bool,
                                                  spike_bool, 1]}})
    else:
        # Updates the unknown dictionary if i5, i7 and spike-in combination has
        # not been found in the unknown dictionary.
        unknown_dict[i5] = {i7: {spike: [i5_bool, i7_bool, spike_bool, 1]}}

    # Returns the updated unknown dictionary
    return unknown_dict


def seq_checker(correct_list, sequence, sequence_diff):
    """
    Checks if the barcode or spike-in sequence exist in the barcode file.
    :param correct_list: List containing all known barcodes or spike-in
            sequences.
    :param sequence: Barcode or spike-in sequence from one specific read.
    :param sequence_diff: Parameter BARC_DIFF or SPIKE_DIFF from settings.py.
    :return boolean: Boolean that tells if the barcode or spike-in sequence has
            been found in the barcode file.
    :return sequence: Barcode or spike-in sequence from one specific read or
            what it should have been if x nucleotide(s) is/are allowed to
            differ.
    """
    # Checks if sequence nucleotide difference is 0
    if sequence_diff == 0:
        # Checks if barcode or spike-in is in the known barcode /
        # spike-in list
        if sequence in correct_list:
            return True, sequence
        else:
            return False, sequence

    # If sequence nucleotide difference is not 0
    else:
        # Calculates the difference between the sequence and every
        # barcode / spike-in to find a match
        for i in range(len(correct_list)):
            if distance(sequence, correct_list[i]) <= sequence_diff:
                return True, correct_list[i]
        return False, sequence


def seq_checker_uniq_i5_i7_spike(correct_i5_list, correct_i7_list, i5, i7,
                                 barc_diff):
    """
    Checks if the barcode or spike-in sequence exist in the barcode file.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param i5: i5 barcode sequence from one specific read.
    :param i7: i7 barcode sequence from one specific read.
    :param barc_diff: Parameter BARC_DIFF from settings.py.
    :return boolean: Boolean that tells if the barcode has been found in the
            barcode file.
    :return barcode: Barcode from one specific read or what it should have been
            if x nucleotide(s) is/are allowed to differ.
    """
    barcode = i5 + "+" + i7

    if barc_diff == 0:
        try:
            if correct_i5_list.index(i5) == correct_i7_list.index(i7):
                return True, barcode
            else:
                return False, barcode
        except ValueError:
            return False, barcode
    else:
        for i in range(len(correct_i5_list)):
            if distance(i5, correct_i5_list[i]) <= barc_diff and \
                    distance(i7, correct_i7_list[i]) <= barc_diff:
                return True, correct_i5_list[i] + "+" + correct_i7_list[i]
        return False, barcode


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
    :return well_locations: List with all well locations of the different
            barcode + spike-in sequence combinations.
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

    elif analyse_combination == 4:
        i5_i7_barcode_lists = [correct_i5_list, correct_i7_list]
        for correct_barcode_list in i5_i7_barcode_lists:
            # Saves the i5 + spike-in and i7 + spike-in combinations to a
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
        i7_loc = int(re.split("(\d+)", barcode[0])[1])
        i5_bar, i7_bar = barcode[1].split("+")

        # Adds the barcodes and their well locations to the dictionary
        if i5_bar not in i5_i7_loc:
            i5_i7_loc[i5_bar] = [i5_loc, {i7_bar: i7_loc}]
        else:
            i5_i7_loc[i5_bar][1].update({i7_bar: i7_loc})

    # Returns the i5_i7_loc dictionary
    return i5_i7_loc
