# Imports the required modules
import xlsxwriter


def no_spike_output(i5_i7_combinations, unknown_barcodes, output_file,
                    i5_i7_loc, indexing, max_contamination,
                    analyse_combination, homopolymers, homopolymer_length):
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
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param homopolymer_length: Maximum length of homopolymers within barcodes.
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
                                indexing, max_contamination,
                                analyse_combination)

        # Writes all unknown i5 + i7 combinations to an Excel sheet
        unknown_sheet = workbook.add_worksheet("Unknown barcodes")
        unknown_sheet.write_row(0, 0, ["i5 barcodes:", "i7 barcodes:",
                                       "i5 known:", "i7 known:",
                                       "Occurrences:"], bold)

        # Sets the Excel column width
        unknown_sheet.set_column("A:E", 20)

        row = 1
        for i5 in unknown_barcodes:
            for i7 in unknown_barcodes[i5]:
                unknown_sheet.write_row(row, 0, [i5, i7,
                                                 unknown_barcodes[i5][i7][0],
                                                 unknown_barcodes[i5][i7][1],
                                                 unknown_barcodes[i5][i7][2]])
                row += 1

        if homopolymer_length > 0:
            homopolymer_sheets(homopolymers, workbook, bold)


def con_table_writer(workbook, excel_2d_list, contamination_table, indexing,
                     max_contamination, analyse_combination):
    """
    Creates the contamination table of the Excel output file.
    :param workbook: Excel workbook object to save the background color.
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

    # Checks if user wants to analyse combinatorial indexing i5 + i7
    if indexing == 1 and analyse_combination == 1:
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                # Gives the bold format to first two rows / columns
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)
                # Write data to Excel contamination table
                else:
                    contamination_table.write(i, j, excel_2d_list[i][j])

    # Checks if user wants to analyse unique indexing or combinatorial
    # i5 + i7 + spike-ins
    elif indexing == 2 or (indexing == 1 and analyse_combination == 5):
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):

                # Gives the bold format to first two rows / columns
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)

                # Adds a green background to the correct combinations
                elif i == j:
                    contamination_table.write(i, j, excel_2d_list[i][j],
                                              green_bg)

                # Writes data to the total row / column
                elif excel_2d_list[i][1] == "Total" or excel_2d_list[1][j] == \
                        "Total":
                    contamination_table.write(i, j, excel_2d_list[i][j])

                else:
                    # Calculates the max allowed contaminated reads of a
                    # row or column
                    if i < j:
                        max_con = round(excel_2d_list[i][i] *
                                        (max_contamination / 100))
                    else:
                        max_con = round(excel_2d_list[j][j] *
                                        (max_contamination / 100))

                    # Writes all other values to the Excel sheet with
                    # the correct background color depending on
                    # contamination
                    contamination_table.write(i, j, excel_2d_list[i][j],
                                              heatmap(excel_2d_list, i, j,
                                                      workbook, max_con))

    # Checks if user wants to analyse combinatorial i5 + spike or i7 +
    # spike
    else:
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):

                # Gives the bold format to first two rows / columns
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)

                # Writes data to the total row / column
                elif excel_2d_list[i][1] == "Total" or excel_2d_list[1][j] == \
                        "Total":
                    contamination_table.write(i, j, excel_2d_list[i][j])

                else:
                    # Writes the correct i5 + spike and i7 + spike
                    # combinations to Excel with a green background
                    if excel_2d_list[i][j] == max(excel_2d_list[i][2:-1]):
                        contamination_table.write(i, j, excel_2d_list[i][j],
                                                  green_bg)

                    else:
                        # Calculates the max allowed contaminated reads of a
                        # row or column
                        max_con = round(max(excel_2d_list[i][2:-1]) *
                                        (max_contamination / 100))

                        # Writes all other values to the Excel sheet with
                        # the correct background color depending on
                        # contamination
                        contamination_table.write(i, j, excel_2d_list[i][j],
                                                  heatmap(excel_2d_list, i, j,
                                                          workbook, max_con))
    return bold


def spike_outputs(correct_i5_list, correct_i7_list, correct_spike_list,
                  well_locations, combinations, output_file,
                  analyse_combination, unknown_dict, indexing,
                  max_contamination, homopolymers, homopolymer_length):
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
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param homopolymer_length: Maximum length of homopolymers within barcodes.
    """
    # i5+spike
    if analyse_combination == 2:
        fw_bar_spike(correct_i5_list, correct_spike_list, well_locations,
                     combinations, output_file, analyse_combination,
                     unknown_dict, indexing, max_contamination, homopolymers,
                     homopolymer_length)

    # i7+spike
    elif analyse_combination == 3:
        fw_bar_spike(correct_i7_list, correct_spike_list, well_locations,
                     combinations, output_file, analyse_combination,
                     unknown_dict, indexing, max_contamination, homopolymers,
                     homopolymer_length)

    # i5+spike and i7+spike
    elif analyse_combination == 4:
        fw_both_bar_spike(correct_i5_list, correct_i7_list, correct_spike_list,
                          well_locations, combinations, output_file,
                          analyse_combination, unknown_dict, indexing,
                          max_contamination, homopolymers, homopolymer_length)

    # i5+i7+spike
    else:
        fw_i5_i7_spike(correct_i5_list, correct_i7_list,
                       correct_spike_list, well_locations,
                       combinations, output_file, analyse_combination,
                       unknown_dict, indexing, max_contamination, homopolymers,
                       homopolymer_length)


def fw_bar_spike(correct_bar_list, correct_spike_list,
                 well_locations, combinations, output_file,
                 analyse_combination, unknown_dict, indexing,
                 max_contamination, homopolymers, homopolymer_length):
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
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param homopolymer_length: Maximum length of homopolymers within barcodes.
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
    excel_2d_list = excel_list_bar_spike(
        well_locations, excel_2d_list, correct_bar_list, correct_spike_list,
        combinations)

    # Creates the output file
    with xlsxwriter.Workbook(output_file) as workbook:

        # Adds a new Excel tab
        contamination_table = workbook.add_worksheet(excel_tabname)

        # Loops through the Excel 2d list and writes it to an Excel
        # sheet with the correct cell format (bold / green background)
        bold = con_table_writer(workbook, excel_2d_list, contamination_table,
                                indexing, max_contamination,
                                analyse_combination)

        # Creates a new Excel tab named Unknown combinations
        unknown_sheet = workbook.add_worksheet("Unknown combinations")

        # Checks if i5+spike has been selected
        if analyse_combination == 2:

            # Adds unknown i5 and spike-in row names
            unknown_sheet.write_row(0, 0, ["i5 barcodes:", "Spike-ins:",
                                           "i5 known:", "Spike-in known:",
                                           "Occurrences:"], bold)

        # i7+spike has been selected
        else:

            # Adds unknown i7 and spike-in row names
            unknown_sheet.write_row(0, 0, ["i7 barcodes:", "Spike-ins:",
                                           "i7 known:", "Spike-in known:",
                                           "Occurrences:"], bold)

        # Writes the unknown barcodes and their occurrences to an Excel
        # tab
        row = 1
        for bar in unknown_dict:
            for spike in unknown_dict[bar]:
                unknown_sheet.write_row(row, 0, [bar, spike,
                                                 unknown_dict[bar][spike][0],
                                                 unknown_dict[bar][spike][1],
                                                 unknown_dict[bar][spike][2]])
                row += 1

        # Checks if user would like to analyse homopolymers
        if homopolymer_length > 0:
            # Calls function to write homopolymers to a Excel sheet
            homopolymer_sheets(homopolymers, workbook, bold)


def fw_both_bar_spike(correct_i5_list, correct_i7_list,
                      correct_spike_list, well_locations,
                      combinations, output_file, analyse_combination,
                      unknown_dict, indexing, max_contamination, homopolymers,
                      homopolymer_length):
    """
    Creates the output Excel file for i5 + spike-ins and i7 + spike-ins.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
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
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param homopolymer_length: Maximum length of homopolymers within barcodes.
    :return: Excel output file at entered location.
    """
    # Creates the base layout for the Excel contamination tab and saves
    # the tab name to a variable
    excel_2d_list_i5 = [["", "", "i5 barcodes →"], ["Well", "Spike-in"]]
    excel_tabname_i5 = "i5 + spike-in"
    excel_2d_list_i7 = [["", "", "i7 barcodes →"], ["Well", "Spike-in"]]
    excel_tabname_i7 = "i7 + spike-in"

    # Creates the Excel 2d list for the i5 barcodes
    excel_2d_list_i5 = excel_list_bar_spike(
        well_locations, excel_2d_list_i5, correct_i5_list, correct_spike_list,
        combinations)

    # Creates the Excel 2d list for the i7 barcodes
    excel_2d_list_i7 = excel_list_bar_spike(
        well_locations, excel_2d_list_i7, correct_i7_list, correct_spike_list,
        combinations)

    # Creates the output file
    with xlsxwriter.Workbook(output_file) as workbook:
        # Adds a new Excel tab
        contamination_table_i5 = workbook.add_worksheet(excel_tabname_i5)
        contamination_table_i7 = workbook.add_worksheet(excel_tabname_i7)

        # Loops through the Excel 2d list and writes it to an Excel
        # sheet with the correct cell format (bold / green background)
        con_table_writer(workbook, excel_2d_list_i5, contamination_table_i5,
                         indexing, max_contamination, analyse_combination)

        bold = con_table_writer(workbook, excel_2d_list_i7,
                                contamination_table_i7,
                                indexing, max_contamination,
                                analyse_combination)

        # Creates a new Excel tab named Unknown combinations
        unknown_sheet = workbook.add_worksheet("Unknown combinations")
        unknown_sheet.set_column("A:G", 20)

        # Adds unknown i5, i7 and spike-in row names
        unknown_sheet.write_row(0, 0, ["i5 barcodes:", "i7 barcodes:",
                                       "Spike-ins:", "i5 known:", "i7 known:",
                                       "Spike-in known:", "Occurrences:"], bold
                                )

        # Writes the unknown data to the unknown Excel tab
        row = 1
        for i5 in unknown_dict:
            for i7 in unknown_dict[i5]:
                for spike in unknown_dict[i5][i7]:
                    unknown_sheet.write_row(row, 0, [
                        i5, i7, spike, unknown_dict[i5][i7][spike][0],
                        unknown_dict[i5][i7][spike][1],
                        unknown_dict[i5][i7][spike][2],
                        unknown_dict[i5][i7][spike][3]])
                    row += 1

        # Checks if user would like to analyse homopolymers
        if homopolymer_length > 0:
            # Calls function to write homopolymers to a Excel sheet
            homopolymer_sheets(homopolymers, workbook, bold)


def excel_list_bar_spike(well_locations, excel_2d_list, correct_bar_list,
                         correct_spike_list, combinations):
    """
    Creates a 2D list of the found contamination.
    :param well_locations: List with all well locations of the different
            barcode + spike-in sequence combinations.
    :param excel_2d_list: 2D list of the Excel output data.
    :param correct_bar_list: List with all i5 or i7 barcodes from the entered
            barcode file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination. Structure depends on spike-ins
            parameter.
    :return excel_2d_list: 2D list of the Excel output data.
    """
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

    return excel_2d_list


def fw_i5_i7_spike(correct_i5_list, correct_i7_list,
                   correct_spike_list, well_locations, combinations,
                   output_file, analyse_combination, unknown_dict,
                   indexing, max_contamination, homopolymers,
                   homopolymer_length):
    """
    Writes the output of i5 + i7 + spike-ins to an Excel file.
    :param correct_i5_list: List with all i5 barcodes from the entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from the entered barcode
            file.
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
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param homopolymer_length: Maximum length of homopolymers within barcodes.
    :return: Excel output file at entered location.
    """
    # Creates the base structure of the Excel 2D list and saves the tab
    # name to a variable
    excel_2d_list = [["", "", "i5+i7 barcodes →"], ["Well", "Spike-in"]]
    excel_tabname = "i5 + i7 + spike-in"

    # Adds all well locations to the Excel 2d list
    for i in range(len(well_locations)):
        excel_2d_list.append([well_locations[i], i + 1])

    # Adds all barcodes and occurrences to the Excel 2d list
    for i in range(len(correct_i5_list)):
        excel_2d_list[1].append(correct_i5_list[i] + "+" + correct_i7_list[i])
        barcode = correct_i7_list[i] + "+" + correct_i5_list[i]
        for j in range(len(correct_spike_list)):
            spike = correct_spike_list[j]
            excel_2d_list[j + 2].append(combinations[barcode][spike])

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

        # Creates a new Excel tab named Unknown combinations
        unknown_sheet = workbook.add_worksheet("Unknown combinations")

        # Adds unknown i5, i7 and spike-in row names
        unknown_sheet.write_row(0, 0, ["i5 barcodes:", "i7 barcodes:",
                                       "Spike-ins:", "i5 known:", "i7 known:",
                                       "Spike-in known:", "Occurrences:"], bold
                                )

        # Writes the unknown data to the unknown Excel tab
        row = 1
        for i5 in unknown_dict:
            for i7 in unknown_dict[i5]:
                for spike in unknown_dict[i5][i7]:
                    unknown_sheet.write_row(row, 0, [
                        i5, i7, spike, unknown_dict[i5][i7][spike][0],
                        unknown_dict[i5][i7][spike][1],
                        unknown_dict[i5][i7][spike][2],
                        unknown_dict[i5][i7][spike][3]])
                    row += 1

        # Checks if user would like to analyse homopolymers
        if homopolymer_length > 0:
            # Calls function to write homopolymers to a Excel sheet
            homopolymer_sheets(homopolymers, workbook, bold)


def heatmap(excel_2d_list, i, j, workbook, max_con):
    """
    Returns the cell background color format.
    :param excel_2d_list: 2D list of the Excel output data.
    :param i: y-coordinate of current cell in excel_2d_list.
    :param j: x-coordinate of current cell in excel_2d_list.
    :param workbook: Excel workbook object to save the background color.
    :param max_con: Maximum allowed contaminated reads.
    :return bg_format: Background color format for a specific cell.
    """
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


def homopolymer_sheets(homopolymers, workbook, bold):
    """
    Writes the homopolymers to an Excel sheet.
    :param homopolymers: Dictionary containing all found homopolymers. Has the
        structure {"A": {barcode 1: count, barcode 2: count}, "T": {barcode 1:
        count, barcode 2: count}, etc}.
    :param workbook: Excel workbook object to create the homopolymer sheets.
    :param bold: Bold format for an Excel cell.
    :return Homopolymer Excel sheets: Excel sheets containing lists of barcodes
        containing homopolymers and their occurrences.
    """
    # Loops through the homopolymer dictionary keys
    for nucleotide in homopolymers:
        # Adds a new Excel sheet for every nucleotide (A, T, C, G)
        homopolymer_sheet = workbook.add_worksheet(nucleotide +
                                                   " homopolymers")
        homopolymer_sheet.write_row(0, 0, ["i5 barcodes:",
                                           "i7 barcodes:",
                                           "Occurrences:"], bold)

        # Sets the Excel column width
        homopolymer_sheet.set_column("A:C", 20)

        # Writes the homopolymers to Excel sheets
        row = 1
        for barcode in homopolymers[nucleotide]:
            i7, i5 = barcode.split("+")
            homopolymer_sheet.write_row(row, 0, [i5, i7, homopolymers[
                nucleotide][barcode]])
            row += 1
