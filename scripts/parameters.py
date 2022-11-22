# Imports the required modules
import os
import python_settings


def check_parameters():
    """
    Retrieves the parameters from the settings.py file and checks if they have
    been entered correctly.
    :return settings: Class containing the values of all parameters.
    """
    # Retrieves the parameters from the setting file
    os.environ["SETTINGS_MODULE"] = 'settings'

    try:
        # Checks if the entered fastq/bcl file has the correct extension
        if not python_settings.settings.FASTQ_FILE.endswith(".fastq"):
            print("Error 1: Entered fastq file has incorrect file extension.")
            exit(1)

        # Checks if the entered xlsx file has the correct extension
        if not python_settings.settings.BARCODE_FILE.endswith(".xlsx"):
            print("Error 2: Entered barcode (+ spike) file has incorrect file extension.")
            exit(2)

        # Checks if the entered indexing value is correct
        if python_settings.settings.INDEXING not in [1, 2]:
            print("Error 3: Entered indexing value is incorrect.")
            exit(3)

        # Checks if entered analysis value is correct
        if python_settings.settings.ANALYSE_COMBINATION not in [1, 2, 3, 4, 5]:
            print("Error 4: Entered analysis combination value is incorrect.")
            exit(4)

        # Checks if max different nucleotides of barcodes is numeric
        if not isinstance(python_settings.settings.BARC_DIFF, int) or not python_settings.settings.BARC_DIFF >= 0:
            print("Error 6: Barcode nucleotide difference parameter is incorrect.")
            exit(5)

        # Checks if max different nucleotides of sequences is numeric
        if not isinstance(python_settings.settings.SPIKE_DIFF, int) or not python_settings.settings.SPIKE_DIFF >= 0:
            print("Error 7: Spike-in nucleotide difference parameter is incorrect.")
            exit(6)

        # Checks if entered sequencer value is correct
        if python_settings.settings.SEQUENCER not in [1, 2]:
            print("Error 8: Entered sequencer value is incorrect.")
            exit(7)

        # Checks if entered output directory exists
        if not os.path.isdir(python_settings.settings.OUTPUT_DIR):
            print("Error 9: Entered output directory path does not exist.")
            exit(8)

        # Checks if entered heatmap contamination percentage is a number
        if not isinstance(python_settings.settings.MAX_CONTAMINATION, (int, float)) or not python_settings.settings.MAX_CONTAMINATION >= 0:
            print("Error 10: Entered heatmap contamination percentage is incorrect.")
            exit(9)

        # Checks if barcode i7 length value is numeric
        if not isinstance(python_settings.settings.UMI_LENGTH, int) or python_settings.settings.UMI_LENGTH < 0:
            print("Error 11: Entered UMI length is incorrect.")
            exit(10)

        # Checks if trimming left end value is numeric
        if not isinstance(python_settings.settings.LEFT_TRIM, int) or python_settings.settings.LEFT_TRIM < 0:
            print("Error 12: Entered spike-ins left trimming value is incorrect.")
            exit(11)

        # Checks if trimming right end value is numeric
        if not isinstance(python_settings.settings.RIGHT_TRIM, int) or python_settings.settings.RIGHT_TRIM < 0:
            print("Error 13: Entered spike-ins right trimming value is incorrect.")
            exit(12)

    except python_settings.ImproperlyConfigured:
        print("Error 14: Not all parameters have been entered in settings.py.")
        exit(13)

    # If all parameters are entered correctly, return the parameters and
    # continue with the main script
    return python_settings.settings
