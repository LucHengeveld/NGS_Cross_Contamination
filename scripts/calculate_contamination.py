# Imports required packages
from Levenshtein import distance


def check_seq_combinatorial(fastq_dict, bar_seq_dict, max_difference):
    """
    Checks if the sequences are similar to the original sequence. If a sequence
    is different, it means that it has been contaminated and adds it to a list.
    :param fastq_dict: Dictionary with the structure {barcode, [sequence1,
           sequence2, etc}.
    :param bar_seq_dict: Dictionary with the structure {barcode: sequence}.
    :param max_difference: Parameter from the parameters.txt file.
    :return contaminated_sequences: List of all the contaminated sequences.
            Structure: [[barcode1, sequence2],[barcode2, sequence2]]
    """
    # Creates an empty list
    contaminated_sequences = []

    # Checks if the found sequences are similar to the original
    # sequences
    for barcode in fastq_dict.keys():
        for sequence in fastq_dict[barcode]:
            if distance(sequence, bar_seq_dict[barcode]) > int(max_difference):
                contaminated_sequences.append([barcode, sequence])

    # Returns the contaminated sequences
    return contaminated_sequences


def contaminated_origin(bar_seq_dict, contaminated_sequences):
    """
    Finds the origin of the contaminated sequences.
    :param bar_seq_dict: Dictionary with the structure {barcode: sequence}.
    :param contaminated_sequences: List of all the contaminated sequences.
    :return origin_seq_bar: Dictionary with the origin, found sequence and
            found barcodes. Structure: {original barcode: [found barcode, found
            sequence]}.
    """
    # Saves all possible barcodes in a list
    barcode_list = list(bar_seq_dict.keys())

    # Creates empty lists
    unknown_bar_seq = []
    wrong_assigned_seq = []

    # Creates an empty dictionary
    origin_seq_bar = {}

    # Loops through the contaminated sequences
    for sequence in contaminated_sequences:
        # Loops through the different barcodes
        for barcode in barcode_list:
            # Checks if the contaminated sequences have been found at a
            # difference barcode and saves them to a list / dictionary
            if distance(sequence[1], bar_seq_dict[barcode]) <= 3:
                # print(sequence[1], "has been found in", sequence[0] + ", but is supposed to be in barcode", barcode + ".")
                wrong_assigned_seq.append(sequence)
                origin_seq_bar[barcode] = sequence
        # Checks if sequence has been found with a different barcode. If
        # it hasn't been found, the origin is unknown
        if sequence not in wrong_assigned_seq:
            # print("Origin of", sequence, "has not been found.")
            unknown_bar_seq.append(sequence)

    # Returns the origin_seq_bar dictionary and the unknown_bar_seq list
    return origin_seq_bar, unknown_bar_seq
