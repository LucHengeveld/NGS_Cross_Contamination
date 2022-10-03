from Levenshtein import distance


def bar_spike(barcode, bar_type, combinations, spike_seq, unknown_dict,
              correct_bar_list, correct_spike_list):
    """
    Checks if the barcode and spike-in sequences are unknown or if they exist
    in the entered barcode file.
    :param barcode: The sequence of the i5, i7 or i5+i7 barcode.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :param spike_seq: Spike-in sequence.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param correct_bar_list: List with all barcodes from the entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :return unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    """
    # Checks if barcode is in the entered barcode file
    if barcode in correct_bar_list:
        # Checks if the spike-in sequence is in the entered barcode file
        if spike_seq in correct_spike_list:
            # Barcode and spike sequence known
            combinations[barcode][spike_seq] += 1
        else:
            # Spike-in sequence unknown
            if spike_seq not in unknown_dict["spike"]:
                unknown_dict["spike"].update({spike_seq: 1})
            else:
                unknown_dict["spike"][spike_seq] += 1

    # Checks if spike-in sequence is in the entered barcode file
    elif spike_seq in correct_spike_list:
        # Barcode unknown
        if barcode not in unknown_dict[bar_type]:
            unknown_dict[bar_type].update({barcode: 1})
        else:
            unknown_dict[bar_type][barcode] += 1
    else:
        # Barcode and spike-in sequence are unknown
        unknown_dict = unknown_bar_spike(barcode, unknown_dict, bar_type,
                                         spike_seq)

    # Returns the dictionary with the known barcodes, unknown barcodes,
    # spike-in sequences and their amount of occurrences
    return unknown_dict, combinations


def bar_spike_bar_diff(barcode, bar_type, combinations, spike_seq,
                       unknown_dict, correct_bar_list, correct_spike_list,
                       diff_bar_nucl):
    """
    Checks if the barcode and spike-in sequences are unknown or if they exist
    in the entered barcode file. Using diff_bar_nucl parameter.
    :param barcode: The sequence of the i5, i7 or i5+i7 barcode.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :param spike_seq: Spike-in sequence.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param correct_bar_list: List with all barcodes from the entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param diff_bar_nucl: Parameter from parameters.txt.
    :return unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    """
    # Creates a boolean
    found_barc = False

    # Loops through the correct barcodes and checks if barcodes differ
    # max diff_seq_nucl from each other
    for correct_bar in correct_bar_list:
        if distance(barcode, correct_bar) <= diff_bar_nucl:
            found_barc = True
            # Checks if the spike-in sequence is in the entered barcode file
            if spike_seq in correct_spike_list:
                # Barcode and spike sequence known
                combinations[correct_bar][spike_seq] += 1
            else:
                # Spike-in sequence unknown
                if spike_seq not in unknown_dict["spike"]:
                    unknown_dict["spike"].update({spike_seq: 1})
                else:
                    unknown_dict["spike"][spike_seq] += 1
            break
    if not found_barc:
        # Checks if spike-in sequence is in the entered barcode file
        if spike_seq in correct_spike_list:
            # Barcode unknown
            if barcode not in unknown_dict[bar_type]:
                unknown_dict[bar_type].update({barcode: 1})
            else:
                unknown_dict[bar_type][barcode] += 1
        else:
            # Barcode and spike-in sequence are unknown
            unknown_dict = unknown_bar_spike(barcode, unknown_dict, bar_type,
                                             spike_seq)

    # Returns the dictionary with the known barcodes, unknown barcodes,
    # spike-in sequences and their amount of occurrences
    return unknown_dict, combinations


def bar_spike_seq_diff(barcode, bar_type, combinations, spike_seq,
                       unknown_dict, correct_bar_list, correct_spike_list,
                       diff_seq_nucl):
    """
    Checks if the barcode and spike-in sequences are unknown or if they exist
    in the entered barcode file. Using diff_seq_nucl parameter.
    :param barcode: The sequence of the i5, i7 or i5+i7 barcode.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :param spike_seq: Spike-in sequence.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param correct_bar_list: List with all barcodes from the entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param diff_seq_nucl: Parameter from parameters.txt.
    :return unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    """
    # Creates a boolean
    found_spike = False

    # Checks if barcode is in the entered barcode file
    if barcode in correct_bar_list:
        unknown_dict, combinations, found_spike = check_spike_in(
            correct_spike_list, spike_seq, diff_seq_nucl, combinations,
            barcode, unknown_dict, found_spike, True, bar_type)
    else:
        # Checks if spike-in sequence is in the entered barcode file
        unknown_dict, combinations, found_spike = check_spike_in(
            correct_spike_list, spike_seq, diff_seq_nucl, combinations,
            barcode, unknown_dict, found_spike, False, bar_type)
        if not found_spike:
            # Barcode and spike-in sequence are unknown
            unknown_dict = unknown_bar_spike(barcode, unknown_dict, bar_type,
                                             spike_seq)

    # Returns the dictionary with the known barcodes, unknown barcodes,
    # spike-in sequences and their amount of occurrences
    return unknown_dict, combinations


def bar_spike_bar_seq_diff(barcode, bar_type, combinations, spike_seq,
                           unknown_dict, correct_bar_list, correct_spike_list,
                           diff_bar_nucl, diff_seq_nucl):
    """
    Checks if the barcode and spike-in sequences are unknown or if they exist
    in the entered barcode file. Using diff_bar_nucl and diff_seq_nucl
    parameters.
    :param barcode: The sequence of the i5, i7 or i5+i7 barcode.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :param spike_seq: Spike-in sequence.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param correct_bar_list: List with all barcodes from the entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param diff_bar_nucl: Parameter from parameters.txt.
    :param diff_seq_nucl: Parameter from parameters.txt.
    :return unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    """
    # Creates a boolean
    found_barc = False
    found_spike = False

    # Loops through the correct barcodes and checks if barcodes differ
    # max diff_seq_nucl from each other
    for correct_bar in correct_bar_list:
        if distance(barcode, correct_bar) <= diff_bar_nucl:
            found_barc = True
            unknown_dict, combinations, found_spike = check_spike_in(
                correct_spike_list, spike_seq, diff_seq_nucl, combinations,
                barcode, unknown_dict, found_spike, found_barc, bar_type)
            break
    if not found_barc:
        # Checks if spike-in sequence is in the entered barcode file
        unknown_dict, combinations, found_spike = check_spike_in(
            correct_spike_list, spike_seq, diff_seq_nucl, combinations,
            barcode, unknown_dict, found_spike, found_barc, bar_type)

    # Returns the dictionary with the known barcodes, unknown barcodes,
    # spike-in sequences and their amount of occurrences
    return unknown_dict, combinations


# TODO: Docstrings / comments in every i5_i7_spike function
def i5_i7_spike(barcode, combinations, spike_seq, unknown_dict,
                correct_i5_list, correct_spike_list):
    return unknown_dict, combinations


def i5_i7_spike_bar_diff(barcode, combinations, spike_seq, unknown_dict,
                         correct_i5_list, correct_spike_list, diff_bar_nucl):
    # Both i5 and i7 are allowed to differ x amount of nucleotides, not
    # 2 times x in total!
    return unknown_dict, combinations


def i5_i7_spike_seq_diff(barcode, combinations, spike_seq, unknown_dict,
                         correct_i5_list, correct_spike_list, diff_seq_nucl):
    return unknown_dict, combinations


def i5_i7_spike_bar_seq_diff(barcode, combinations, spike_seq, unknown_dict,
                             correct_i5_list, correct_spike_list,
                             diff_bar_nucl, diff_seq_nucl):
    # Both i5 and i7 are allowed to differ x amount of nucleotides, not
    # 2 times x in total!
    return unknown_dict, combinations


def unknown_bar_spike(barcode, unknown_dict, bar_type, spike_seq):
    """
    Gets called when the barcode and spike-in sequence are unknown. Adds them
    to the unknown dict.
    :param barcode: i5 or i7 barcode sequence.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param spike_seq: Spike-in sequence.
    :return unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    """
    if barcode not in unknown_dict[bar_type + "_spike"]:
        unknown_dict[bar_type + "_spike"].update({barcode: {spike_seq: 1}})
    elif spike_seq not in unknown_dict[bar_type + "_spike"][barcode]:
        unknown_dict[bar_type + "_spike"][barcode].update({spike_seq: 1})
    else:
        unknown_dict[bar_type + "_spike"][barcode][spike_seq] += 1
    return unknown_dict


# TODO: Docstrings and comments:
def check_spike_in(correct_spike_list, spike_seq, diff_seq_nucl, combinations,
                   barcode, unknown_dict, found_spike, bar_type, found_barc):
    """
    Checks if a spike-in sequence from the barcode file has been found.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param spike_seq: Spike-in sequence.
    :param diff_seq_nucl: Parameter from parameters.txt.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :param barcode: The sequence of the i5, i7 or i5+i7 barcode.
    :param unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :param found_spike: If a spike-in sequence similar to the ones from
            the barcode file has been found, this boolean is True.
    :param bar_type: Type of the barcode (i5, i7 or i5+i7).
    :param found_barc: If a barcode sequence similar to the ones from
            the barcode file has been found, this boolean is True.
    :return unknown_dict: Dictionary containing all unknowns barcodes and
            spike-in sequences.
    :return combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on spike-ins parameter.
    :return found_spike: If a spike-in sequence similar to the ones from
            the barcode file has been found, this boolean is True.
    """
    for correct_spike in correct_spike_list:
        # Checks if the spike-in sequence is in the entered barcode
        # file
        if distance(spike_seq, correct_spike) <= diff_seq_nucl:
            found_spike = True
            # Barcode and spike-in sequence known
            combinations[barcode][spike_seq] += 1
            break

    if found_barc and not found_spike:
        # Spike-in sequence unknown
        if spike_seq not in unknown_dict["spike"]:
            unknown_dict["spike"].update({spike_seq: 1})
        else:
            unknown_dict["spike"][spike_seq] += 1
    if not found_barc and not found_spike:
        # Barcode and spike-in sequence are unknown
        unknown_dict = unknown_bar_spike(barcode, unknown_dict, bar_type,
                                         spike_seq)
    return unknown_dict, combinations, found_spike
