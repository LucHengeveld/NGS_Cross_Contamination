# Imports the other python scripts
from scripts import file_readers as fr, parameters as pm, \
    calculate_contamination as cc, check_barcodes as cb, file_writers as fw

# TODO: Docstrings / comments
# Main function of the script, calls the different functions
if __name__ == "__main__":
    # Saves the user entered parameters in a list
    parameters_list = pm.retrieve_parameters("parameters.txt")

    # Checks if the parameters have been entered correctly by the user
    file_extension = pm.check_parameters(parameters_list)

    # If the file has a bcl file extension, it will convert it to a
    # .fastq file and calls the fastq_reader function
    # TODO: Build in max difference barcode sequence param
    if file_extension == "bcl":
        fastq_file = fr.bcl_to_fastq(parameters_list)
        fastq_dict = fr.fastq_reader(fastq_file)
    else:
        fastq_dict = fr.fastq_reader(parameters_list[0])

    # Retrieves the data from the barcode excel file
    barcode_file_data = fr.barcode_file_reader(parameters_list[1],
                                               parameters_list[6],
                                               parameters_list[3])
    if parameters_list[3] == "1":
        # Retrieve the unknown barcodes
        # Finished list for combinatorial i5+i7:
        unknown_barcodes, correct_barcodes = cb.barc_no_spike(fastq_dict,
                                                              barcode_file_data,
                                                              parameters_list[
                                                                  4])
        # Extra step if unique i5+i7:
        if parameters_list[2] == "2":
            # Unique i5 + i7
            incorrect_combinations, unknown_barcodes, unknown_i5, unknown_i7, \
            correct_i5, correct_i7 = cb.uni_barc_no_spike(fastq_dict,
                                                          barcode_file_data,
                                                          parameters_list[4],
                                                          unknown_barcodes)
            fw.uni_no_spike_output(incorrect_combinations, unknown_barcodes,
                                   unknown_i5, unknown_i7, correct_i5,
                                   correct_i7, correct_barcodes)
        else:
            fw.com_no_spike_output(unknown_barcodes)
    elif parameters_list[2] == "1":
        # combinatorial spike-ins i5+i7
        pass
    else:
        # unique i5+i7 spike-ins
        pass

    # Spike in sequences:
    # # Checks which sequences are contaminated
    # contaminated_sequences = cc.check_seq_combinatorial(fastq_dict,
    #                                                     bar_seq_dict,
    #                                                     parameters_list[5])
    #
    # if contaminated_sequences:
    #     # print(len(contaminated_sequences), "contaminated sequences found.")
    #     cc.contaminated_origin(bar_seq_dict, contaminated_sequences)
    # else:
    #     # print("No contaminated sequences found.")
    #     pass
