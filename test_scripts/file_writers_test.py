# Imports the required modules
import xlsxwriter


def no_spike_output(i5_i7_combinations, unknown_barcodes, output_file,
                    i5_i7_loc, indexing, max_contamination,
                    analyse_combination):
    """
    Creates the output Excel file for unique dual (non-redundant) indexing with
    no spike-in sequence.
    :param i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :param unknown_barcodes: Dictionary with all unknown barcode combinations
            from the fastq file.
    :param output_file: File path to the output file.
    :param i5_i7_loc: Dictionary containing the i5 and i7 barcodes with their
            corresponding well locations. Dictionary has the structure:
            {i5: ["A" {i7: 1, i7: 2}]}.
    :param indexing: Parameter of the used indexing method.
    :param max_contamination: Parameter of the maximum allowed contamination.
    :param analyse_combination: Parameter from settings.py.
    :return: Excel output file at entered location.
    """
    # Create base layout in 2d list for Excel output file
    excel_2d_list = [["", "i7 barcodes →"], ["", ""]]

    # Variable to add i7 barcodes to the array if they haven't been
    # added yet
    add_i7 = True

    # Loops through all possible i5 + i7 combinations and adds the
    # occurrences to the Excel 2d array
    for i5 in i5_i7_combinations.keys():
        if indexing == 1:
            row = [i5_i7_loc[i5][0], i5]
        else:
            row = ["", i5]

        for i7 in i5_i7_combinations[i5]:
            row.append(i5_i7_combinations[i5][i7])
            if add_i7:
                excel_2d_list[1].append(i7)
                if indexing == 1:
                    excel_2d_list[0].append(i5_i7_loc[i5][1][i7])

        # Calculates the row totals
        row.append(sum(row[2:]))
        excel_2d_list.append(row)
        add_i7 = False

    # Adds description to the i5 barcodes column
    excel_2d_list[1][0] = "i5 barcodes ↓"

    # Adds Total description to the end of the row / column
    excel_2d_list[1].append("Total")
    excel_2d_list.append(["", "Total"])

    # Calculates the column totals
    column_tot = excel_2d_list[2][2:-1]
    for row in range(3, len(excel_2d_list)):
        for col in range(2, len(excel_2d_list[row]) - 1):
            column_tot[col - 2] += excel_2d_list[row][col]

    # Adds the column total values to the Excel 2d list
    excel_2d_list[-1] += column_tot

    # Writes the output to the Excel file
    with xlsxwriter.Workbook(output_file) as workbook:
        contamination_table = workbook.add_worksheet("Contamination Table")

        # Calls a function to write the contamination table
        bold = con_table_writer(workbook, excel_2d_list, contamination_table,
                                indexing, max_contamination, analyse_combination)

        # Writes all unknown i5 + i7 combinations to an Excel sheet
        unknown_sheet = workbook.add_worksheet("Unknown barcodes")
        unknown_sheet.write_row(0, 0, ["i5 barcodes:", "i7 barcodes:",
                                       "i5 known:", "i7 known:",
                                       "Occurrences:"], bold)

        # Sets the excel column width
        unknown_sheet.set_column("A:E", 12)

        row = 1
        for i5 in unknown_barcodes:
            for i7 in unknown_barcodes[i5]:
                unknown_sheet.write_row(row, 0, [i5, i7,
                                                 unknown_barcodes[i5][i7][0],
                                                 unknown_barcodes[i5][i7][1],
                                                 unknown_barcodes[i5][i7][2]])
                row += 1


def con_table_writer(workbook, excel_2d_list, contamination_table, indexing,
                     max_contamination, analyse_combination):
    """
    Creates the contamination table of the Excel output file.
    :param workbook:
    :param excel_2d_list: 2D list of the Excel output data.
    :param contamination_table: Excel sheet for the contamination table.
    :param indexing: Parameter of the used indexing method.
    :param max_contamination: Parameter of the maximum allowed contamination.
    :param analyse_combination: Parameter from settings.py.
    :return bold: Bold Excel workbook format
    """
    # Creates bold and green background color format
    bold = workbook.add_format({'bold': True})
    green_bg = workbook.add_format({'bg_color': '#adebad'})

    # Saves the amount of columns and rows to a variable
    cols = len(excel_2d_list[1])
    rows = len(excel_2d_list)

    # Set column width
    contamination_table.set_column(0, cols, 13)

    # Adds borders around the data
    border_format = workbook.add_format({'border': 1})
    contamination_table.conditional_format(0, 0, rows, cols,
                                           {'type': 'no_blanks',
                                            'format': border_format})

    if indexing == 1 and analyse_combination == 1:
        # comb no spike
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)
                else:
                    contamination_table.write(i, j, excel_2d_list[i][j])

    # All combinations of unique and combinatorial i5+i7+spike
    elif indexing == 2 or (indexing == 1 and analyse_combination == 5):

        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)
                elif i == j:
                    contamination_table.write(i, j, excel_2d_list[i][j],
                                              green_bg)
                elif excel_2d_list[i][1] == "Total" or excel_2d_list[1][j] == \
                        "Total":
                    contamination_table.write(i, j, excel_2d_list[i][j])
                else:
                    contamination_table.write(i, j, excel_2d_list[i][j],
                                              heatmap(excel_2d_list, i, j,
                                                      workbook,
                                                      max_contamination))
    # combinatorial i5+spike / i7+spike or both
    else:
        # TODO: output contamination table writer
        pass
    return bold


def spike_outputs(correct_i5_list, correct_i7_list, correct_spike_list,
                  well_locations, combinations, output_file,
                  analyse_combination, unknown_dict, indexing,
                  max_contamination):
    """
    Calls the different file writers depending on the entered parameters.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param well_locations: List with all well locations of the different
            barcode + spike-in sequence combinations.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination.
    :param output_file: File path to the output file.
    :param analyse_combination: Parameter from settings.py.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param indexing: Parameter of the used indexing method.
    :param max_contamination: Parameter of the maximum allowed contamination.
    """
    # i5+spike
    if analyse_combination == 2:
        file_writer_bar_spike(correct_i5_list, correct_spike_list,
                              well_locations, combinations, output_file,
                              analyse_combination, unknown_dict, indexing,
                              max_contamination)

    # i7+spike
    elif analyse_combination == 3:
        file_writer_bar_spike(correct_i7_list, correct_spike_list,
                              well_locations, combinations, output_file,
                              analyse_combination, unknown_dict, indexing,
                              max_contamination)

    # i5+spike and i7+spike
    elif analyse_combination == 4:
        # TODO: filewriter function
        pass

    # i5+i7+spike
    else:
        # TODO: filewriter function
        pass


def file_writer_bar_spike(correct_bar_list, correct_spike_list,
                          well_locations, combinations, output_file,
                          analyse_combination, unknown_dict, indexing,
                          max_contamination):
    """
    Writes the output of i5+spike or i7+spike to an Excel file.
    :param correct_bar_list: List with all i5 or i7 barcodes from the entered
            barcode file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param well_locations: List with all well locations of the different
            barcode + spike-in sequence combinations.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination. Structure depends on spike-ins
            parameter.
    :param output_file: File path to the output file.
    :param analyse_combination: Parameter from settings.py.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param indexing: Parameter of the used indexing method.
    :param max_contamination: Parameter of the maximum allowed contamination.
    :return: Excel output file at entered location.
    """
    # Checks if i5+spike or i7+spike has been selected
    if analyse_combination == 2:
        excel_2d_list = [["", "", "i5 barcodes →"], ["Well", "Spike-in"]]
        excel_tabname = "i5 + spike-in"
    else:
        excel_2d_list = [["", "", "i7 barcodes →"], ["Well", "Spike-in"]]
        excel_tabname = "i7 + spike-in"

    # Adds all well locations to the Excel 2d list
    for i in range(len(well_locations)):
        excel_2d_list.append([well_locations[i], i + 1])

    # Creates an empty list
    added_barc = []

    # Loops through the barcodes from the entered barcode file
    for i in range(len(correct_bar_list)):

        # Adds every barcode and spike-in sequence to the Excel 2d list
        bar = correct_bar_list[i]
        if bar not in added_barc:
            added_barc.append(bar)
            excel_2d_list[1].append(bar)
            for j in range(len(correct_spike_list)):
                spike = correct_spike_list[j]
                excel_2d_list[j + 2].append(combinations[bar][spike])

    # Adds a total column and row
    excel_2d_list[1].append("Total")
    excel_2d_list.append(["", "Total"])

    # Creates an empty list
    col_tot = []

    # Adds the total values to the total column / row
    for row in range(2, len(excel_2d_list) - 1):
        excel_2d_list[row].append(sum(excel_2d_list[row][2:]))
        for value in range(2, len(excel_2d_list[row]) - 1):
            if len(col_tot) != len(excel_2d_list[row]) - 3:
                col_tot.append(excel_2d_list[row][value])
            else:
                col_tot[value - 2] += excel_2d_list[row][value]
    excel_2d_list[-1].extend(col_tot)

    # Creates the output file
    with xlsxwriter.Workbook(output_file) as workbook:

        # Adds a new Excel tab
        contamination_table = workbook.add_worksheet(excel_tabname)

        # Loops through the Excel 2d list and writes it to an Excel
        # sheet with the correct cell format (bold / green background)
        bold = con_table_writer(workbook, excel_2d_list, contamination_table,
                                indexing, max_contamination,
                                analyse_combination)

        # Checks if i5+spike has been selected
        if analyse_combination == 2:

            # Creates unknown barcode and spike-in sequence Excel tabs
            unknown_bar = workbook.add_worksheet("unknown_i5")
            unknown_bar.write_row(0, 0, ["i5 barcode", "Occurrences"], bold)

            unknown_bar_spike = workbook.add_worksheet("unknown_i5_spike")
            unknown_bar_spike.write_row(0, 0, ["i5 barcode",
                                               "Spike-in sequence",
                                               "Occurrences"], bold)
            # Saves the barcode type to a variable
            barcode = "i5"

        # i7+spike has been selected
        else:

            # Creates unknown barcode and spike-in sequence Excel tabs
            unknown_bar = workbook.add_worksheet("unknown_i7")
            unknown_bar.write_row(0, 0, ["i7 barcode", "Occurrences"])

            unknown_bar_spike = workbook.add_worksheet("unknown_i7_spike")
            unknown_bar_spike.write_row(0, 0, ["i7 barcode",
                                               "Spike-in sequence",
                                               "Occurrences"], bold)
            # Saves the barcode type to a variable
            barcode = "i7"

        # Creates unknown spike-in sequence Excel tab
        unknown_spike = workbook.add_worksheet("unknown_spike")
        unknown_spike.write_row(0, 0, ["Spike-in sequence", "Occurrences"],
                                bold)

        # Writes the unknown barcodes and their occurrences to an Excel
        # tab
        row = 1
        for bar in unknown_dict[barcode]:
            unknown_bar.write_row(row, 0, [bar,
                                           unknown_dict[barcode][bar]])
            row += 1

        # Writes the unknown spike-ins and their occurrences to an Excel
        # tab
        row = 1
        for spike in unknown_dict["spike"]:
            unknown_spike.write_row(row, 0, [spike,
                                             unknown_dict["spike"][spike]])
            row += 1

        # Writes the unknown barcodes+spike-ins and their occurrences to
        # an Excel tab
        row = 1
        for bar in unknown_dict[barcode + "_spike"]:
            for spike in unknown_dict[barcode + "_spike"][bar]:
                unknown_bar_spike.write_row(row, 0, [
                    bar, spike, unknown_dict[barcode + "_spike"][bar][spike]])
            row += 1


def heatmap(excel_2d_list, i, j, workbook, heatmap_percentage):
    """
    Returns the cell background color format.
    :param excel_2d_list: 2D list of the Excel output data.
    :param i: y-coordinate of current cell in excel_2d_list.
    :param j: x-coordinate of current cell in excel_2d_list.
    :param workbook: Excel workbook object to save the background color.
    :param heatmap_percentage: Parameter of the maximum allowed contamination.
    :return bg_format: Background color format for a specific cell.
    """
    # TODO: Add 3 colors to heatmap (green -> yellow -> red)
    # Checks if cell values should be compared to the correct barcode
    # value in its row or column and calculates the max amount of
    # contaminated reads
    if i < j:
        max_con = round(excel_2d_list[i][i] * (heatmap_percentage / 100))
    else:
        max_con = round(excel_2d_list[j][j] * (heatmap_percentage / 100))

    # If the correct barcode has value 0 and current cell has value 0,
    # return white background color
    if max_con == 0 and excel_2d_list[i][j] == 0:
        hex_color = '#%02x%02x%02x' % (255, 255, 255)

    # If the correct barcode has value 0 and current cell has a higher
    # value or current cell value is higher than correct barcode value,
    # return red background color
    elif max_con == 0 or excel_2d_list[i][j] > max_con:
        hex_color = '#%02x%02x%02x' % (255, 0, 0)

    # If the correct barcode has a value higher than 0 and current cell
    # has value 0, return white background color
    elif excel_2d_list[i][j] == 0:
        hex_color = '#%02x%02x%02x' % (255, 255, 255)

    # Calculates the shade of red for the cell if it does not get
    # through the if statements above
    else:
        current_cell = excel_2d_list[i][j]
        color = round(255 - (255 * current_cell / max_con))
        hex_color = '#%02x%02x%02x' % (255, color, color)

    # Saves the color to the workbook background color format and
    # returns it
    bg_format = workbook.add_format({'bg_color': hex_color})
    return bg_format
