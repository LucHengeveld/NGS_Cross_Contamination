import os


def retrieve_parameters(parameters_file):
    """
    Retrieves the parameters from the parameters textfile.
    :param parameters_file: File that contains the user entered parameters.
    :return parameters: Dictionary with parameters.
    """
    # Creates an empty dictionary
    parameters_dict = {}

    keys_list = ["fastq_file_path", "barcode_file_path", "indexing",
                 "spike_ins", "diff_barc", "diff_seq", "sequencer",
                 "output_dir", "output_filename", "heatmap_percentage",
                 "trimming_ends", "trim_i5", "trim_i7", "spike_order"]

    counter = 0
    # Opens the parameters file and saves the parameters to a list
    with open(parameters_file, "r") as file:
        for line in file:
            if not line.startswith("#") and line != "\n":
                parameters_dict[keys_list[counter]] = line.replace("\n", "")
                counter += 1

    # Returns the parameters list
    return parameters_dict


def check_parameters(parameters_dict):
    # TODO: Add docstrings to this function.

    # Checks if the entered fastq/bcl file has the correct extension
    if not parameters_dict["fastq_file_path"].split(".")[1] in ["bcl",
                                                                "fastq"]:
        print("Error 1: Entered fastq / bcl file has incorrect extension.")
        exit(1)
    else:
        # If file has correct extension, it saves it to a variable
        file_extension = parameters_dict["fastq_file_path"].split(".")[1]

    # Checks if the entered xlsx file has the correct extension
    if parameters_dict["barcode_file_path"].split(".")[1] != "xlsx":
        print("Error 2: Entered barcode file has incorrect extension.")
        exit(2)

    # Checks if the entered indexing value is correct
    if parameters_dict["indexing"] not in ["1", "2"]:
        print("Error 3: Entered indexing value is incorrect.")
        exit(3)

    # Checks if entered analysis value is correct
    if parameters_dict["spike_ins"] not in ["1", "2", "3", "4"]:
        print("Error 4: Entered analysis value is incorrect.")
        exit(4)

    # Checks if max different nucleotides of barcodes is numeric
    if not parameters_dict["diff_barc"].isdecimal():
        print("Error 5: Entered maximum nucleotide difference between barcodes"
              " is not numeric.")
        exit(5)

    # Checks if max different nucleotides of sequences is numeric
    if not parameters_dict["diff_seq"].isdecimal():
        print("Error 6: Entered maximum nucleotide difference between"
              "sequences is not numeric.")
        exit(6)

    # Checks if entered sequencer value is correct
    if parameters_dict["sequencer"] not in ["1", "2"]:
        print("Error 7: Entered sequencer value is incorrect.")
        exit(7)

    # Checks if entered output directory exists
    if not os.path.isdir(parameters_dict["output_dir"]):
        print("Error 8: Entered output directory path does not exist.")
        exit(8)

    # Checks if all parameters have been entered
    # TODO: Update 14 if more params are added
    if len(parameters_dict.keys()) < 14:
        print("Error 9: Missing one of the parameters. Make sure you have "
              "entered all parameters in parameters.txt")
        exit(9)

    # Checks if entered heatmap contamination percentage is a number
    try:
        parameters_dict["heatmap_percentage"] = float(
            parameters_dict["heatmap_percentage"])
    except ValueError:
        print("Error 16: Entered heatmap contamination percentage is not a number.")

    # Checks if max different nucleotides of sequences is numeric
    if not parameters_dict["trimming_ends"].isdecimal():
        print("Error 17: Entered spike-ins trimming value is not numeric.")
        exit(17)

    if not parameters_dict["trim_i5"].isdecimal():
        print("Error 18: Entered spike-ins i5 trimming value is not numeric.")
        exit(18)

    if not parameters_dict["trim_i7"].isdecimal():
        print("Error 19: Entered spike-ins i7 trimming value is not numeric.")
        exit(19)

    if not parameters_dict["spike_order"].isdecimal():
        print("Error 20: Entered spike-ins order value is not numeric.")
        exit(20)

    # If all parameters are entered correctly, return the file extension
    # and continue with the script
    return file_extension
