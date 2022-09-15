def retrieve_parameters(parameters_file):
    """
    Retrieves the parameters from the parameters textfile.
    :param parameters_file: File that contains the user entered parameters.
    :return parameters: List with parameters.
    """
    # Creates an empty list
    parameters_list = []

    # Opens the parameters file and saves the parameters to a list
    with open(parameters_file, "r") as file:
        for line in file:
            if not line.startswith("#") and line != "\n":
                parameters_list.append(line.replace("\n", ""))

    # Returns the parameters list
    return parameters_list


def check_parameters(parameters_list):
    # TODO: Add docstrings to this function.
    # TODO: Add new parameters from txt file to this function.
    # TODO: Error to check if all parameters have been entered.
    # TODO: Maybe change parameters list to a dictionary

    # Checks if the entered fastq/bcl file has the correct extension
    if not parameters_list[0].split(".")[1] in ["bcl", "fastq"]:
        print("Error 1: Entered file has incorrect extension. Please enter a "
              ".bcl or .fastq file path in parameters.txt")
        exit(1)
    else:
        # If file has correct extension, it saves it to a variable
        file_extension = parameters_list[0].split(".")[1]

    # Checks if the entered xlsx file has the correct extension
    if parameters_list[1].split(".")[1] != "xlsx":
        print("Error 2: Entered file has incorrect extension. Please enter a "
              ".xlsx file path in parameters.txt")
        exit(2)
    else:
        # If file has correct extension, it saves it to a variable
        file_extension = parameters_list[0].split(".")[1]

    # Checks if the entered indexing value is correct
    if parameters_list[2] not in ["1", "2"]:
        print("Error 3: Entered indexing value is incorrect. Please enter a "
              "'1' if combinatorial indexing has been used or a '2' if unique"
              "dual indexing / non redundant indexing has been used.")
        exit(3)

    # Checks if entered analysis value is correct
    if parameters_list[3] not in ["1", "2"]:
        print("Error 4: Entered analysis value is incorrect. Please enter a "
              "'1' to analyse I5 + I7 or a '2' to analyse spike-ins + I5 and "
              "I7.")
        exit(4)

    # Checks if max different nucleotides of barcodes is numeric
    if not parameters_list[4].isdecimal():
        print("Error 5: Entered maximum nucleotide difference between barcodes"
              " is not numeric. Please enter a number.")
        exit(5)

    # Checks if max different nucleotides of sequences is numeric
    if not parameters_list[5].isdecimal():
        print(
            "Error 6: Entered maximum nucleotide difference between sequences"
            " is not numeric. Please enter a number.")
        exit(6)

    # Checks if entered sequencer value is correct
    if parameters_list[6] not in ["1", "2"]:
        print("Error 6: Entered sequencer value is incorrect. Please enter a"
              "'1' if iSeq, MiniSeq, NextSeq, HiSeq3000 or HiSeq4000 has been "
              "used. Enter a '2' if a MiSeq, HiSeq2000-2500 or Novaseq has "
              "been used.")
        exit(6)

    # TODO: Parameter output folder check + connect to file_writers.py functions.
    # TODO: Parameter output file name + connect to file_writers.py functions.

    # If all parameters are entered correctly, return the file extension
    # and continue with the script
    return file_extension
