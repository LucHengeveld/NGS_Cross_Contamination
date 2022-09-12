# Imports the other python scripts
from scripts import file_scripts as fs, parameters as pm, \
    calculate_contamination as cc

# Main function of the script, calls the different functions
if __name__ == "__main__":
    # Saves the user entered parameters in a list
    parameters_list = pm.retrieve_parameters("parameters.txt")

    # Checks if the parameters have been entered correctly by the user
    file_extension = pm.check_parameters(parameters_list)

    # Retrieve the barcodes and corresponding sequences
    bar_seq_dict = fs.bar_seq_file_reader(parameters_list[1])

    # If the file has a bcl file extension, it will convert it to a
    # .fastq file and calls the fastq_reader function
    # TODO: Build in max difference barcode sequence param
    if file_extension == "bcl":
        fastq_file = fs.bcl_to_fastq(parameters_list)
        fastq_dict = fs.fastq_reader(fastq_file)
    else:
        fastq_dict = fs.fastq_reader(parameters_list[0])

    # Checks which sequences are contaminated
    contaminated_sequences = cc.check_seq_combinatorial(fastq_dict,
                                                        bar_seq_dict,
                                                        parameters_list[4])

    if contaminated_sequences:
        # print(len(contaminated_sequences), "contaminated sequences found.")
        cc.contaminated_origin(bar_seq_dict, contaminated_sequences)
    else:
        # print("No contaminated sequences found.")
        pass
