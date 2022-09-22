# Imports the other python scripts
from scripts import file_readers as fr, parameters as pm, \
    calculate_contamination as cc, check_barcodes as cb, file_writers as fw

import time
start_time = time.time()


if __name__ == "__main__":
    # TODO: Docstrings / comments.
    # Main function of the script, calls the different functions
    # Saves the user entered parameters in a list
    print("Retrieve parameters", time.strftime("%H:%M"))
    parameters_dict = pm.retrieve_parameters("parameters.txt")

    # Checks if the parameters have been entered correctly by the user
    file_extension = pm.check_parameters(parameters_dict)

    # If the file has a bcl file extension, it will convert it to a
    # .fastq file and calls the fastq_reader function
    # if file_extension == "bcl":
    #     fastq_file = fr.bcl_to_fastq(parameters_dict)
    #     fastq_dict = fr.fastq_reader(fastq_file)
    # else:
    #     fastq_dict = fr.fastq_reader(parameters_dict["fastq_file_path"])

    print("Retrieve barcodes from barcode file", time.strftime("%H:%M"))
    # Retrieves the data from the barcode Excel file
    barcode_file_data = fr.barcode_file_reader(
        parameters_dict["barcode_file_path"],
        parameters_dict["sequencer"],
        parameters_dict["spike_ins"])

    # Combinatorial and unique dual indexing without spike-in sequence
    if parameters_dict["spike_ins"] == "1":

        print("Retrieve barcodes from fastq file", time.strftime("%H:%M"))
        # Retrieve barcodes from fastq file
        fastq_data = fr.fastq_reader_no_spike(
            parameters_dict["fastq_file_path"])

        print("Compare barcodes", time.strftime("%H:%M"))
        # Compare all fastq barcode sequences to the ones from the
        # input Excel file
        i5_i7_combinations, unknown_barcodes, unknown_i5, unknown_i7 = \
            cb.barc_no_spike(barcode_file_data, fastq_data,
                             parameters_dict["diff_barc"])

        print("Retrieve output filename and location", time.strftime("%H:%M"))
        # Saves the output file location and name to a variable
        output_file = parameters_dict["output_dir"] + parameters_dict[
            "output_filename"] + ".xlsx"

        if parameters_dict["indexing"] == "1":
            # Retrieve barcode well locations
            print("Retrieve well locations", time.strftime("%H:%M"))
            i5_i7_loc = cb.retrieve_barcode_location(barcode_file_data)

            print("Write comb data to excel output file", time.strftime("%H:%M"))
            # Write data to Excel output file
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               unknown_i5, unknown_i7, output_file, i5_i7_loc,
                               parameters_dict["indexing"],
                               parameters_dict["heatmap_percentage"])
        else:

            print("Write uniq data to excel output file", time.strftime("%H:%M"))
            # Write data to Excel output file
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               unknown_i5, unknown_i7, output_file, [],
                               parameters_dict["indexing"],
                               parameters_dict["heatmap_percentage"])

    elif parameters_dict["indexing"] == "1":
        # combinatorial spike-ins i5+i7
        pass
    else:
        # unique i5+i7 spike-ins
        pass

        # Unfinished spike-ins code:
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

print("Code took:", round(time.time() - start_time), "seconds")
