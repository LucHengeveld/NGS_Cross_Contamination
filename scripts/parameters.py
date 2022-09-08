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
    # TODO: Add new parameters to this function.
    # Checks if the entered file has the correct extension
    if not parameters_list[0].split(".")[1] in ["bcl", "fastq"]:
        print("Error 1: Entered file has incorrect extension. Please enter a "
              ".bcl or .fastq file path in parameters.txt")
        exit(1)
    else:
        # If file has correct extension, it saves it to a variable
        file_extension = parameters_list[0].split(".")[1]

    # Checks if the entered indexing value is correct
    if int(parameters_list[1]) not in [1, 2]:
        print("Error 2: Entered indexing value is incorrect. Please enter a "
              "1 if combinatorial indexing has been used or a 2 if unique dual "
              "indexing / non redundant indexing has been used.")
        exit(2)

    # If all parameters are entered correctly, return the file extension
    # and continue with the script
    return file_extension