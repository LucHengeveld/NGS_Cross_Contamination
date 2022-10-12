# Imports the required modules
import os
from python_settings import settings


def check_parameters():
    """
    Retrieves the parameters from the settings.py file and checks if they have
    been entered correctly.
    :return settings: Class containing the values of all parameters.
    """
    # TODO: Fix error code numbers

    # Retrieves the parameters from the setting file
    os.environ["SETTINGS_MODULE"] = 'settings'

    try:
        # Checks if the entered fastq/bcl file has the correct extension
        if not settings.FASTQ_FILE.endswith(".fastq"):
            print("Error 1: Entered fastq file has incorrect file extension.")
            exit(1)

        # Checks if the entered xlsx file has the correct extension
        if not settings.BARCODE_FILE.endswith(".xlsx"):
            print("Error 2: Entered barcode (+ spike) file has incorrect file extension.")
            exit(2)

        # Checks if the entered indexing value is correct
        if settings.INDEXING not in [1, 2]:
            print("Error 3: Entered indexing value is incorrect.")
            exit(3)

        # Checks if entered analysis value is correct
        if settings.ANALYSE_COMBINATION not in [1, 2, 3, 4]:
            print("Error 4: Entered analysis combination value is incorrect.")
            exit(4)

        # Checks if max different nucleotides of barcodes is numeric
        if not isinstance(settings.BARC_DIFF, int) or not settings.BARC_DIFF >= 0:
            print("Error 1: Barcode nucleotide difference parameter has not been entered correctly in settings.py.")
            exit(1)

        # Checks if max different nucleotides of sequences is numeric
        if not isinstance(settings.SPIKE_DIFF, int) or not settings.SPIKE_DIFF >= 0:
            print("Error 1: Spike-in nucleotide difference parameter has not been entered correctly in settings.py.")
            exit(1)

        # Checks if entered sequencer value is correct
        if settings.SEQUENCER not in [1, 2]:
            print("Error 7: Entered sequencer value is incorrect.")
            exit(7)

        # Checks if entered output directory exists
        if not os.path.isdir(settings.OUTPUT_DIR):
            print("Error 8: Entered output directory path does not exist.")
            exit(8)

        # Checks if entered heatmap contamination percentage is a number
        if not isinstance(settings.MAX_CONTAMINATION, (int, float)):
            print("Error 16: Entered heatmap contamination percentage is not a number.")
            exit(16)

        # Checks if trimming ends value is numeric
        if settings.SPIKE_BAR_ORDER not in [0, 1, 2]:
            print("Error 17: Entered spike-ins i5 and i7 ends order value is incorrect.")
            exit(17)

        # Checks if trimming i5 end value is numeric
        if not isinstance(settings.I5_TRIM, int):
            print("Error 18: Entered spike-ins i5 trimming value is not numeric.")
            exit(18)

        # Checks if trimming i7 end value is numeric
        if not isinstance(settings.I7_TRIM, int):
            print("Error 19: Entered spike-ins i7 trimming value is not numeric.")
            exit(19)

    except:
        print("Not all parameters have been entered in settings.py.")
        exit(1)

    # If all parameters are entered correctly, return the parameters and
    # continue with the main script
    return settings
