# Imports the other python scripts
from scripts import file_scripts as fs, parameters as pm

# Main function of the script, calls all other functions
if __name__ == "__main__":
    # Saves the user entered parameters in a list
    parameters_list = pm.retrieve_parameters("parameters.txt")

    # Checks if the parameters have been entered correctly by the user
    file_extension = pm.check_parameters(parameters_list)

    # If the file has a bcl file extension, it will convert it to a
    # .fastq file and calls the fastq_reader function
    if file_extension == "bcl":
        fastq_file = fs.bcl_to_fastq(parameters_list)
        fastq_dict = fs.fastq_reader(fastq_file)
    else:
        fastq_dict = fs.fastq_reader(parameters_list[0])
