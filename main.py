# Imports the other python scripts
from scripts import file_readers as fr, parameters as pm, \
    check_barcodes as cb, file_writers as fw

# Imports the required modules
import time

start_time = time.time()
print("--- Code started at", time.strftime("%H:%M", time.localtime()), "---\n")


def main():
    # Main function of the script, calls the different functions

    # TODO: Improve speed by directly running code when reading every fastq
    #  line instead of saving it to a list first or pass every 100 000 lines
    #  parallel to compare function

    # TODO: Implement parameters ANALYSE_TYPE

    # Checks if the parameters have been entered correctly by the user
    print("Check parameters", time.strftime("%H:%M"))
    settings = pm.check_parameters()

    # Retrieves the data from the barcode Excel file
    print("Retrieve barcodes from barcode file", time.strftime("%H:%M"))
    barcode_file_data = fr.barcode_file_reader(
        settings.BARCODE_FILE,
        settings.SEQUENCER,
        settings.ANALYSE_COMBINATION)

    # Saves the output file location and name to a variable
    print("Retrieve output filename and location", time.strftime("%H:%M"))
    output_file = settings.OUTPUT_DIR + settings.OUTPUT_FILENAME + ".xlsx"

    # Combinatorial and unique dual indexing without spike-in sequence
    if settings.ANALYSE_COMBINATION == 1:

        # Retrieve barcodes from fastq file
        print("Retrieve barcodes from fastq file", time.strftime("%H:%M"))
        fastq_data = fr.fastq_reader_no_spike(settings.FASTQ_FILE,
                                              settings.UMI_LENGTH)

        # Retrieve all possible barcode combinations
        print("Retrieve barcodes from barcode file", time.strftime("%H:%M"))
        correct_i5_list, correct_i7_list, i5_i7_combinations = \
            cb.retrieve_combinations_no_spike(barcode_file_data)

        # Compare all fastq barcode sequences to the ones from the
        # input Excel file
        print("Compare barcodes", time.strftime("%H:%M"))
        i5_i7_combinations, unknown_barcodes = \
            cb.comp_barcodes(fastq_data, settings.BARC_DIFF,
                             correct_i5_list, correct_i7_list,
                             i5_i7_combinations)

        if settings.INDEXING == 1:
            # Retrieve barcode well locations
            print("Retrieve well locations", time.strftime("%H:%M"))
            i5_i7_loc = cb.retrieve_barcode_location(barcode_file_data)

            # Write data to Excel output file
            print("Write comb data to excel output file",
                  time.strftime("%H:%M"))
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               output_file, i5_i7_loc, settings.INDEXING,
                               settings.MAX_CONTAMINATION,
                               settings.ANALYSE_COMBINATION)
        else:
            # Write data to Excel output file
            print("Write uniq data to excel output file",
                  time.strftime("%H:%M"))
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               output_file, [], settings.INDEXING,
                               settings.MAX_CONTAMINATION,
                               settings.ANALYSE_COMBINATION)
    else:
        # Retrieve the fastq data
        print("Retrieve barcodes and sequences from fastq file",
              time.strftime("%H:%M"))
        fastq_data = fr.fastq_reader_with_spike(settings.FASTQ_FILE,
                                                settings.LEFT_TRIM,
                                                settings.RIGHT_TRIM,
                                                settings.UMI_LENGTH)

        # Retrieve all possible barcode and spike-in combinations
        print("Create dict of all possible combinations",
              time.strftime("%H:%M"))
        combinations, correct_spike_list, correct_i5_list, correct_i7_list, \
        well_locations = cb.retrieve_combinations_with_spike(
            barcode_file_data, settings.ANALYSE_COMBINATION)

        # Compare all fastq barcodes to the ones found in the barcode +
        # spike-in file
        print("Compare barcodes and sequences from fastq file",
              time.strftime("%H:%M"))

        if settings.ANALYSE_COMBINATION in [2, 3]:
            # i5+spike or i7+spike
            combinations, unknown_dict = cb.comp_bar_spike(
                combinations, correct_spike_list, correct_i5_list,
                correct_i7_list, fastq_data, settings.BARC_DIFF,
                settings.SPIKE_DIFF, settings.ANALYSE_COMBINATION)

        elif settings.ANALYSE_COMBINATION == 4:
            # Both i5+spike and i7+spike
            combinations, unknown_dict = cb.comp_bar_spike(
                combinations, correct_spike_list, correct_i5_list,
                correct_i7_list, fastq_data, settings.BARC_DIFF,
                settings.SPIKE_DIFF, settings.ANALYSE_COMBINATION)

        elif settings.INDEXING == 1:
            #  Combinatorial i5+i7+spike
            combinations, unknown_dict = cb.comp_i5_i7_spike(
                combinations, correct_spike_list, correct_i5_list,
                correct_i7_list, fastq_data, settings.BARC_DIFF,
                settings.SPIKE_DIFF, settings.INDEXING)

        else:
            #  Unique i5+i7+spike
            combinations, unknown_dict = cb.comp_i5_i7_spike(
                combinations, correct_spike_list, correct_i5_list,
                correct_i7_list, fastq_data, settings.BARC_DIFF,
                settings.SPIKE_DIFF, settings.INDEXING)

        print("Write data to output Excel file", time.strftime("%H:%M"))
        fw.spike_outputs(correct_i5_list, correct_i7_list, correct_spike_list,
                         well_locations, combinations, output_file,
                         settings.ANALYSE_COMBINATION, unknown_dict,
                         settings.INDEXING,
                         settings.MAX_CONTAMINATION)


if __name__ == "__main__":
    main()

print("\n--- Code ended at", time.strftime("%H:%M", time.localtime()),
      "---\nScript duration:", round(time.time() - start_time), "seconds")
