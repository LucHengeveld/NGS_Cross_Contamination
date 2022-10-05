# Imports the other python scripts
from scripts import file_readers as fr, parameters as pm, check_barcodes as cb, file_writers as fw

import time

start_time = time.time()

if __name__ == "__main__":
    # TODO: Docstrings / comments.
    # Main function of the script, calls the different functions

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
    if settings.ANALYSE_COMBINATION == "1":

        # Retrieve barcodes from fastq file
        print("Retrieve barcodes from fastq file", time.strftime("%H:%M"))
        fastq_data = fr.fastq_reader_no_spike(settings.FASTQ_FILE)

        # Retrieve all possible barcode combinations
        print("Retrieve barcodes from barcode file", time.strftime("%H:%M"))
        correct_i5_list, correct_i7_list, i5_i7_combinations = \
            cb.retrieve_combinations_no_spike(barcode_file_data)

        # Compare all fastq barcode sequences to the ones from the
        # input Excel file
        print("Compare barcodes", time.strftime("%H:%M"))
        i5_i7_combinations, unknown_barcodes, unknown_i5, unknown_i7 = \
            cb.barc_no_spike(fastq_data, settings.BARC_DIFF,
                             correct_i5_list, correct_i7_list,
                             i5_i7_combinations)

        if settings.INDEXING == "1":
            # Retrieve barcode well locations
            print("Retrieve well locations", time.strftime("%H:%M"))
            i5_i7_loc = cb.retrieve_barcode_location(barcode_file_data)

            # Write data to Excel output file
            print("Write comb data to excel output file",
                  time.strftime("%H:%M"))
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               unknown_i5, unknown_i7, output_file, i5_i7_loc,
                               settings.INDEXING, settings.MAX_CONTAMINATION)
        else:
            # Write data to Excel output file
            print("Write uniq data to excel output file",
                  time.strftime("%H:%M"))
            fw.no_spike_output(i5_i7_combinations, unknown_barcodes,
                               unknown_i5, unknown_i7, output_file, [],
                               settings.INDEXING, settings.MAX_CONTAMINATION)

    else:
        # Retrieve the fastq data
        print("Retrieve barcodes and sequences from fastq file",
              time.strftime("%H:%M"))
        fastq_data = fr.fastq_reader_with_spike(settings.FASTQ_FILE,
                                                settings.SPIKE_BAR_ORDER,
                                                settings.I5_TRIM,
                                                settings.I7_TRIM)

        # Retrieve all possible barcode and spike-in combinations
        print("Create dict of all possible combinations",
              time.strftime("%H:%M"))
        combinations, correct_spike_list, correct_i5_list, correct_i7_list, \
            well_locations = cb.retrieve_combinations_with_spike(
                barcode_file_data,
                settings.ANALYSE_COMBINATION)

        # Compare all fastq barcodes to the ones found in the barcode +
        # spike-in file
        print("Compare barcodes and sequences from fastq file",
              time.strftime("%H:%M"))
        # TODO: i5+i7+spike
        unknown_dict, combinations = cb.barc_with_spike(
            combinations, correct_spike_list, correct_i5_list, correct_i7_list,
            fastq_data, settings.BARC_DIFF, settings.SPIKE_DIFF,
            settings.ANALYSE_COMBINATION)

        print("Write data to output Excel file", time.strftime("%H:%M"))
        fw.excel_writer(correct_i5_list, correct_i7_list, correct_spike_list, well_locations, unknown_dict, combinations, output_file, settings.MAX_CONTAMINATION, settings.ANALYSE_COMBINATION)

        # 4. Write data to excel file in multiple tabs (10 total)
        #   - i5+i7+spike, i5+spike, i7+spike
        #   - Unknown spike, i5, i7, i5+i7, i5+spike, i7+spike, unknown i5+i7+spike
        if settings.INDEXING == "1":
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
