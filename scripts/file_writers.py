import xlsxwriter


def comb_no_spike_output(correct_barcodes, unknown_barcodes, output_file):
    """
    Creates the output Excel file for combinatorial indexing with no spike-in
    sequence.
    :param correct_barcodes: Dictionary with all barcodes from the original
            barcode Excel file and the amount of times they have been found in
            the fastq file. Structure: {barcode: occurrences}.
    :param unknown_barcodes: Dictionary with all fastq barcodes that have not
            been found in the original barcode Excel file.
            Structure: {barcode: occurrences}.
    :param output_file: Output file path.
    :return: Excel output file at entered location.
    """
    # Creates a new Excel workbook
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    # Makes the header bold
    bold = workbook.add_format({'bold': True})
    worksheet.write_row("A1", ["Correct barcodes:", "Occurrences:", "", "Unknown barcodes:", "Occurrences:"], bold)

    # Writes the correct barcodes and number of occurrences to the Excel
    # file
    row = 0
    for key in correct_barcodes.keys():
        row += 1
        worksheet.write(row, 0, key)
        worksheet.write(row, 1, correct_barcodes[key])

    # Writes the unknown barcodes and number of occurrences to the Excel
    # file
    row = 0
    for key in unknown_barcodes.keys():
        row += 1
        worksheet.write(row, 3, key)
        worksheet.write(row, 4, unknown_barcodes[key])

    # Closes and saves the workbook
    workbook.close()


def uniq_no_spike_output(i5_i7_combinations, unknown_barcodes, output_file):
    """
    Creates the output Excel file for unique dual (non redundant) indexing with
    no spike-in sequence.
    :param i5_i7_combinations: Dictionary containing all possible i5 + i7
            combinations and its amount of occurrences in the fastq file.
            Structure: {i5: {i7: counter}, {i7, counter}}.
    :param unknown_barcodes: List with all unknown barcode combinations from
            the fastq file.
    :param output_file: Output file path.
    :return: Excel output file at entered location.
    """
    # TODO: Add column for unknown barcodes.
    # TODO: Possible improvement: Add heatmap and make col A/B and row 1/2 bold.
    # Heatmap: https://xlsxwriter.readthedocs.io/working_with_pandas.html

    # Create base layout in 2d list for Excel output file
    excel_2d_list = [["", "", "i7 barcodes"], ["", ""]]

    # Variable to add i7 barcodes to the array if they haven't been
    # added yet
    add_i7 = True

    # Loops through all possible i5 + i7 combinations and adds the
    # occurrences to the Excel 2d array
    for i5 in i5_i7_combinations.keys():
        row = ["", i5]
        for i7 in i5_i7_combinations[i5]:
            row.append(i5_i7_combinations[i5][i7])
            if add_i7:
                excel_2d_list[1].append(i7)
        # Calculates the row totals
        row.append(sum(row[2:]))
        excel_2d_list.append(row)
        add_i7 = False

    # Adds description to the i5 barcodes column
    excel_2d_list[2][0] = "i5 barcodes"

    # Adds Total description to the end of the row / column
    excel_2d_list[1].append("Total")
    excel_2d_list.append(["", "Total"])

    # Calculates the column totals
    column_tot = excel_2d_list[2][2:-1]
    for row in range(3, len(excel_2d_list)):
        for col in range(2, len(excel_2d_list[row])-1):
            column_tot[col-2] += excel_2d_list[row][col]

    # Adds the column total values to the Excel 2d list
    excel_2d_list[-1] += column_tot

    # Writes the output to the Excel file
    with xlsxwriter.Workbook(output_file) as workbook:
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(excel_2d_list):
            worksheet.write_row(row_num, 0, data)
