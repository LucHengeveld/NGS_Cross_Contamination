# Imports the other python scripts
from scripts import file_readers as fr, parameters as pm, \
    calculate_contamination as cc, check_barcodes as cb, file_writers as fw

# TODO: Docstrings / comments.
# Main function of the script, calls the different functions
if __name__ == "__main__":
    # Saves the user entered parameters in a list
    parameters_dict = pm.retrieve_parameters("parameters.txt")

    # Checks if the parameters have been entered correctly by the user
    file_extension = pm.check_parameters(parameters_dict)

    # If the file has a bcl file extension, it will convert it to a
    # .fastq file and calls the fastq_reader function
    if file_extension == "bcl":
        fastq_file = fr.bcl_to_fastq(parameters_dict)
        fastq_dict = fr.fastq_reader(fastq_file)
    else:
        fastq_dict = fr.fastq_reader(parameters_dict["fastq_file_path"])

    # Retrieves the data from the barcode Excel file
    barcode_file_data = fr.barcode_file_reader(
        parameters_dict["barcode_file_path"],
        parameters_dict["sequencer"],
        parameters_dict["spike-ins"])

    output_file = parameters_dict["output_dir"] + parameters_dict[
        "output_filename"] + ".xlsx"

    if parameters_dict["spike-ins"] == "1":
        if parameters_dict["indexing"] == "1":
            # Combinatorial i5+i7:
            # Retrieve the unknown barcodes
            unknown_barcodes, correct_barcodes = cb.comb_barc_no_spike(
                fastq_dict, barcode_file_data, parameters_dict["diff_barc"])
            # Write data to output file
            fw.comb_no_spike_output(correct_barcodes, unknown_barcodes,
                                    output_file)
        else:
            # Unique i5 + i7
            i5_i7_combinations, unknown_barcodes = cb.uniq_barc_no_spike(
                barcode_file_data, fastq_dict, parameters_dict["diff_barc"])

            # Write data to output file
            fw.uniq_no_spike_output(i5_i7_combinations, unknown_barcodes,
                                    output_file)

    elif parameters_dict["indexing"] == "1":
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
