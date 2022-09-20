import xlsxwriter


def no_spike_output(i5_i7_combinations, unknown_barcodes, unknown_i5,
                    unknown_i7, output_file, i5_i7_loc, indexing):
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
    :param output_file: Output file path.
    :param i5_i7_loc: Dictionary containing the i5 and i7 barcodes with their
            corresponding well locations. Dictionary has the structure:
            {i5: ["A" {i7: 1, i7: 2}]}.
    :param indexing: Parameter of the used indexing method.
    :return: Excel output file at entered location.
    """
    # TODO: Possible improvement: Add heatmap.
    # Heatmap: https://xlsxwriter.readthedocs.io/working_with_pandas.html
    # TODO: Split this function into multiple ones.

    # Create base layout in 2d list for Excel output file
    excel_2d_list = [["", "i7 barcodes"], ["", ""]]

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
    excel_2d_list[1][0] = "i5 barcodes"

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

        # Saves the amount of columns to a variable
        cols = len(excel_2d_list[1])

        # Set column width
        contamination_table.set_column(0, 1, 10.3)
        contamination_table.set_column(2, cols, 9.3)

        # Loops through the data and writes it to an Excel sheet with
        # the correct cell format (bold / green background)
        for i in range(len(excel_2d_list)):
            for j in range(len(excel_2d_list[i])):
                if i in [0, 1] or j in [0, 1]:
                    contamination_table.write(i, j, excel_2d_list[i][j], bold)
                elif i == j and 1 < i < len(excel_2d_list) - 1:
                    contamination_table.write(i, j, excel_2d_list[i][j],
                                              green_bg)
                elif i != len(excel_2d_list) - 1 and j != \
                        len(excel_2d_list[i]) - 1:
                    if indexing == "1":
                        contamination_table.write(i, j, excel_2d_list[i][j])
                    else:
                        contamination_table.write(i, j, excel_2d_list[i][j],
                                                  heatmap(excel_2d_list, i, j,
                                                          workbook))
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


def heatmap(excel_2d_list, i, j, workbook):
    """
    Returns the cell background color format.
    :param excel_2d_list: 2D list of the Excel output data.
    :param i: y-coordinate of current cell in excel_2d_list.
    :param j: x-coordinate of current cell in excel_2d_list.
    :param workbook: Excel workbook object to save the background color.
    :return bg_format: Background color format for a specific cell.
    """
    # Checks if cell values should be compared to the correct barcode
    # value in its row or column
    if i < j:
        max_val = round(excel_2d_list[i][i] / 10000)
    else:
        max_val = round(excel_2d_list[j][j] / 10000)

    # If the correct barcode has value 0 and current cell has value 0,
    # return white background color
    if max_val == 0 and excel_2d_list[i][j] == 0:
        hex_color = '#%02x%02x%02x' % (255, 255, 255)

    # If the correct barcode has value 0 and current cell has a higher
    # value or current cell value is higher than correct barcode value,
    # return red background color
    elif max_val == 0 or excel_2d_list[i][j] > max_val:
        hex_color = '#%02x%02x%02x' % (255, 0, 0)

    # If the correct barcode has a value higher than 0 and current cell
    # has value 0, return white background color
    elif excel_2d_list[i][j] == 0:
        hex_color = '#%02x%02x%02x' % (255, 255, 255)

    # Calculates the shade of red for the cell if it does not get
    # through the if statements above
    else:
        current_cell = excel_2d_list[i][j]
        color = round(255 - (255 * current_cell / max_val))
        hex_color = '#%02x%02x%02x' % (255, color, color)

    # Saves the color to the workbook background color format and
    # returns it
    bg_format = workbook.add_format({'bg_color': hex_color})
    return bg_format
