import xlsxwriter


def no_spike_output(i5_i7_combinations, unknown_barcodes, unknown_i5,
                    unknown_i7, output_file, i5_i7_loc, indexing,
                    max_contamination):
    """
    Creates the output Excel file for unique dual (non-redundant) indexing with
    no spike-in sequence.
    :param i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :param unknown_barcodes: Dictionary with all unknown barcode combinations
            from the fastq file.
    :param unknown_i5: Dictionary with all unknown i5 barcodes from the fastq
            file.
    :param unknown_i7: Dictionary with all unknown i7 barcodes from the fastq
            file.
    :param output_file: File path to the output file.
    :param i5_i7_loc: Dictionary containing the i5 and i7 barcodes with their
            corresponding well locations. Dictionary has the structure:
            {i5: ["A" {i7: 1, i7: 2}]}.
    :param indexing: Parameter of the used indexing method.
    :param max_contamination: Parameter of the maximum allowed contamination.
    :return: Excel output file at entered location.
    """
    # TODO: Split this function into multiple ones.

    # Create base layout in 2d list for Excel output file
    excel_2d_list = [["", "i7 barcodes →"], ["", ""]]

    # Variable to add i7 barcodes to the array if they haven't been
    # added yet
    add_i7 = True

    # Loops through all possible i5 + i7 combinations and adds the
    # occurrences to the Excel 2d array
    for i5 in i5_i7_combinations.keys():
        if indexing == "1":
            row = [i5_i7_loc[i5][0], i5]
        else:
            row = ["", i5]

        for i7 in i5_i7_combinations[i5]:
            row.append(i5_i7_combinations[i5][i7])
            if add_i7:
                excel_2d_list[1].append(i7)
                if indexing == "1":
                    excel_2d_list[0].append(int(i5_i7_loc[i5][1][i7]))

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

        # Creates bold and green background color format
        bold = workbook.add_format({'bold': True})
        green_bg = workbook.add_format({'bg_color': '#adebad'})

        # Saves the amount of columns and rows to a variable
        cols = len(excel_2d_list[1])
        rows = len(excel_2d_list)

        # Set column width
        contamination_table.set_column(0, cols, 11)

        # Adds borders around the data
        border_format = workbook.add_format({'border': 1})
        contamination_table.conditional_format(1, 1, rows, cols,
                                               {'type': 'no_blanks',
                                                'format': border_format})

        # Loops through the data and writes it to an Excel sheet with
        # the correct cell format (bold / green background)
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)
                elif i == j and 1 < i < len(excel_2d_list) - 1:
                    if indexing == "1":
                        contamination_table.write(i, j, excel_2d_list[i][j])
                    else:
                        contamination_table.write(i, j, excel_2d_list[i][j],
                                                  green_bg)
                elif i != len(excel_2d_list) - 1 and j != \
                        len(excel_2d_list[i]) - 1:
                    if indexing == "1":
                        contamination_table.write(i, j, excel_2d_list[i][j])
                    else:
                        contamination_table.write(i, j, excel_2d_list[i][j],
                                                  heatmap(excel_2d_list, i, j,
                                                          workbook,
                                                          max_contamination))
                else:
                    contamination_table.write(i, j, excel_2d_list[i][j])

        # Writes all unknown i5 + i7 combinations to an Excel sheet
        unknown_i5_i7_sheet = workbook.add_worksheet("Unknown i5+i7")
        unknown_i5_i7_sheet.set_column("A:A", 23.5)
        unknown_i5_i7_sheet.set_column("B:B", 11.7)
        unknown_i5_i7_sheet.write_row(0, 0, ["Unknown i5 + i7 barcodes:",
                                             "Occurrences:"], bold)

        for row in range(len(unknown_barcodes.keys())):
            unknown_i5_i7_sheet.write_row(row + 1, 0,
                                          [list(unknown_barcodes.keys())[row],
                                           unknown_barcodes[list(
                                               unknown_barcodes.keys())[row]]])

        # Writes all unknown i5 barcodes to an Excel sheet
        unknown_i5_sheet = workbook.add_worksheet("Unknown i5")
        unknown_i5_sheet.set_column("A:A", 20)
        unknown_i5_sheet.set_column("B:B", 11.7)
        unknown_i5_sheet.write_row(0, 0, ["Unknown i5 barcodes:",
                                          "Occurrences:"], bold)
        for row in range(len(unknown_i5.keys())):
            unknown_i5_sheet.write_row(row + 1, 0,
                                       [list(unknown_i5.keys())[row],
                                        unknown_i5[list(unknown_i5.keys()
                                                        )[row]]])

        # Writes all unknown i7 barcodes to an Excel sheet
        unknown_i7_sheet = workbook.add_worksheet("Unknown i7")
        unknown_i7_sheet.set_column("A:A", 20)
        unknown_i7_sheet.set_column("B:B", 11.7)
        unknown_i7_sheet.write_row(0, 0, ["Unknown i7 barcodes:",
                                          "Occurrences:"], bold)
        for row in range(len(unknown_i7.keys())):
            unknown_i7_sheet.write_row(row + 1, 0,
                                       [list(unknown_i7.keys())[row],
                                        unknown_i7[list(unknown_i7.keys()
                                                        )[row]]])


def excel_writer(correct_i5_list, correct_i7_list, correct_spike_list,
                 well_locations, unknown_dict, combinations, output_file,
                 max_contamination, analyse_combination):
    """
    Calls the function for the Excel output file writer.
    :param correct_i5_list: List with all i5 barcodes from entered barcode
            file.
    :param correct_i7_list: List with all i7 barcodes from entered barcode
            file.
    :param correct_spike_list: List with all spike-in sequences from the
            entered barcode file.
    :param well_locations: List with all well locations of the different
            barcode + spike-in sequence combinations.
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :param combinations: Dictionary containing every possible barcode +
            spike-in sequence combination and the amount of occurrences.
            Structure depends on analyse_combination parameter.
    :param output_file: File path to the output file.
    :param max_contamination: Parameter of the maximum allowed contamination.
    :param analyse_combination: Parameter from settings.py.
    """
    # TODO: Add heatmap to spike-in results
    # Checks which analyse parameter has been used
    if analyse_combination == 2:
        # Calls file_writer function for i5+spike-ins
        file_writer_bar_spike(correct_i5_list, correct_spike_list,
                              well_locations, combinations, output_file,
                              analyse_combination, unknown_dict)

    elif analyse_combination == 3:
        # Calls file_writer function for i7+spike-ins
        file_writer_bar_spike(correct_i7_list, correct_spike_list,
                              well_locations, combinations, output_file,
                              analyse_combination, unknown_dict)

    elif analyse_combination == 4:
        # Calls file_writer function for i5+spike-ins and i7+spike-ins
        i5_spike_i7_spike([correct_i5_list, correct_i7_list],
                          correct_spike_list, well_locations, combinations,
                          output_file, unknown_dict)

    # TODO: i5+i7+spike file writer
    else:
        # Calls file_writer function for i5+i7+spike-ins
        pass


def file_writer_bar_spike(correct_bar_list, correct_spike_list,
                          well_locations, combinations, output_file,
                          analyse_combination, unknown_dict):
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
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                contamination_table.write(i, j, excel_2d_list[i][j])

        # Checks if i5+spike has been selected
        if analyse_combination == 2:

            # Creates unknown barcode and spike-in sequence Excel tabs
            unknown_bar = workbook.add_worksheet("unknown_i5")
            unknown_bar.write_row(0, 0, ["i5 barcode", "Occurrences"])

            unknown_bar_spike = workbook.add_worksheet("unknown_i5_spike")
            unknown_bar_spike.write_row(0, 0, ["i5 barcode",
                                               "Spike-in sequence",
                                               "Occurrences"])
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
                                               "Occurrences"])
            # Saves the barcode type to a variable
            barcode = "i7"

        # Creates unknown spike-in sequence Excel tab
        unknown_spike = workbook.add_worksheet("unknown_spike")
        unknown_spike.write_row(0, 0, ["Spike-in sequence", "Occurrences"])

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


def i5_spike_i7_spike(correct_bar_list, correct_spike_list,
                      well_locations, combinations, output_file, unknown_dict):
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
    :param unknown_dict: Dictionary containing all unknown barcodes and
            spike-in sequences.
    :return: Excel output file at entered location.
    """

    excel_2d_lists = [[["", "", "i5 barcodes →"], ["Well", "Spike-in"]],
                      [["", "", "i7 barcodes →"], ["Well", "Spike-in"]]]
    excel_tabnames = ["i5 + spike-in", "i7 + spike-in"]

    # Adds all well locations to the Excel 2d list
    for i in range(len(well_locations)):
        excel_2d_lists[0].append([well_locations[i], i + 1])
        excel_2d_lists[1].append([well_locations[i], i + 1])

    for i in range(len(correct_bar_list)):
        added_barc = []
        for j in range(len(correct_bar_list[i])):
            # Adds every barcode and spike-in sequence to the Excel 2d list
            bar = correct_bar_list[i][j]
            if bar not in added_barc:
                added_barc.append(bar)
                excel_2d_lists[i][1].append(bar)
                for k in range(len(correct_spike_list)):
                    spike = correct_spike_list[k]
                    excel_2d_lists[i][k + 2].append(combinations[bar][spike])

        # Adds a total column and row
        excel_2d_lists[i][1].append("Total")
        excel_2d_lists[i].append(["", "Total"])

        # Creates an empty list
        col_tot = []

        # Adds the total values to the total column / row
        for row in range(2, len(excel_2d_lists[i]) - 1):
            excel_2d_lists[i][row].append(sum(excel_2d_lists[i][row][2:]))
            for value in range(2, len(excel_2d_lists[i][row]) - 1):
                if len(col_tot) != len(excel_2d_lists[i][row]) - 3:
                    col_tot.append(excel_2d_lists[i][row][value])
                else:
                    col_tot[value - 2] += excel_2d_lists[i][row][value]
        excel_2d_lists[i][-1].extend(col_tot)

    # Creates the output file
    with xlsxwriter.Workbook(output_file) as workbook:

        # Adds new Excel tabs
        contamination_tables = [workbook.add_worksheet(excel_tabnames[0]),
                                workbook.add_worksheet(excel_tabnames[1])]

        # Loops through the Excel 2d list and writes it to an Excel
        # sheet with the correct cell format (bold / green background)
        for index in range(len(excel_2d_lists)):
            for i in range(len(excel_2d_lists[index])):
                for j in range(len(excel_2d_lists[index][i])):
                    contamination_tables[index].write(
                        i, j, excel_2d_lists[index][i][j])

        # Creates unknown barcode and barcode+spike-in sequence
        # Excel tabs
        unknown_bar = [workbook.add_worksheet("unknown_i5"),
                       workbook.add_worksheet("unknown_i7")]
        unknown_bar[0].write_row(0, 0, ["i5 barcode", "Occurrences"])
        unknown_bar[1].write_row(0, 0, ["i7 barcode", "Occurrences"])

        unknown_bar_spike = [workbook.add_worksheet("unknown_i5_spike"),
                             workbook.add_worksheet("unknown_i7_spike")]
        unknown_bar_spike[0].write_row(0, 0, ["i5 barcode",
                                              "Spike-in sequence",
                                              "Occurrences"])
        unknown_bar_spike[1].write_row(0, 0, ["i7 barcode",
                                              "Spike-in sequence",
                                              "Occurrences"])

        # Creates unknown spike-in sequence Excel tab
        unknown_spike = workbook.add_worksheet("unknown_spike")
        unknown_spike.write_row(0, 0, ["Spike-in sequence", "Occurrences"])

        # Writes the unknown barcodes and their occurrences to an Excel
        # tab
        barcodes = ["i5", "i7"]
        for tab in range(len(unknown_bar)):
            row = 1
            for bar in unknown_dict[barcodes[tab]]:
                unknown_bar[tab].write_row(
                    row, 0, [bar, unknown_dict[barcodes[tab]][bar]])
                row += 1

            # Writes the unknown barcodes+spike-ins and their occurrences to
            # an Excel tab
            row = 1
            for bar in unknown_dict[barcodes[tab] + "_spike"]:
                for spike in unknown_dict[barcodes[tab] + "_spike"][bar]:
                    unknown_bar_spike[tab].write_row(row, 0, [bar, spike, unknown_dict[barcodes[tab] + "_spike"][bar][spike]])
                row += 1

        # Writes the unknown spike-ins and their occurrences to an Excel
        # tab
        row = 1
        for spike in unknown_dict["spike"]:
            unknown_spike.write_row(row, 0, [spike, unknown_dict["spike"][spike]])
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
