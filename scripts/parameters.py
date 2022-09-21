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
                 "output_dir", "output_filename"]

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
        print("Error 1: Entered file has incorrect extension. Please enter a "
              ".bcl or .fastq file path in parameters.txt.")
        exit(1)
    else:
        # If file has correct extension, it saves it to a variable
        file_extension = parameters_dict["fastq_file_path"].split(".")[1]

    # Checks if the entered xlsx file has the correct extension
    if parameters_dict["barcode_file_path"].split(".")[1] != "xlsx":
        print("Error 2: Entered file has incorrect extension. Please enter a "
              ".xlsx file path in parameters.txt")
        exit(2)

    # Checks if the entered indexing value is correct
    if parameters_dict["indexing"] not in ["1", "2"]:
        print("Error 3: Entered indexing value is incorrect. Please enter a "
              "'1' if combinatorial indexing has been used or a '2' if unique"
              "dual indexing / non redundant indexing has been used.")
        exit(3)

    # Checks if entered analysis value is correct
    if parameters_dict["spike_ins"] not in ["1", "2"]:
        print("Error 4: Entered analysis value is incorrect. Please enter a "
              "'1' to analyse I5 + I7 or a '2' to analyse spike-ins + I5 and "
              "I7.")
        exit(4)

    # Checks if max different nucleotides of barcodes is numeric
    if not parameters_dict["diff_barc"].isdecimal():
        print("Error 5: Entered maximum nucleotide difference between barcodes"
              " is not numeric. Please enter a number.")
        exit(5)

    # Checks if max different nucleotides of sequences is numeric
    if not parameters_dict["diff_seq"].isdecimal():
        print("Error 6: Entered maximum nucleotide difference between"
              "sequences is not numeric. Please enter a number.")
        exit(6)

    # Checks if entered sequencer value is correct
    if parameters_dict["sequencer"] not in ["1", "2"]:
        print("Error 7: Entered sequencer value is incorrect. Please enter a"
              "'1' if iSeq, MiniSeq, NextSeq, HiSeq3000 or HiSeq4000 has been "
              "used. Enter a '2' if a MiSeq, HiSeq2000-2500 or Novaseq has "
              "been used.")
        exit(7)

    # Checks if entered output directory exists
    if not os.path.isdir(parameters_dict["output_dir"]):
        print("Error 8: Entered output directory path does not exist. Please "
              "enter a correct output directory path.")
        exit(8)

    # Checks if all parameters have been entered
    # TODO: Update 9 if more params are added
    if len(parameters_dict.keys()) < 9:
        print("Error 9: Missing one of the parameters. Make sure you have "
              "entered all parameters in parameters.txt")
        exit(9)

    # TODO: Param heatmap % (bv 0,01% / 0,1% / 0,5% / etc)
    
    # If all parameters are entered correctly, return the file extension
    # and continue with the script
    return file_extension
