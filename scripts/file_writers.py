import xlsxwriter

output_folder = "C:\\Users\\luche\\Desktop\\output\\"
output_filename = "output"


def com_no_spike_output(unknown_barcodes):
    # TODO: Docstrings / comments
    output_file = output_folder + output_filename + ".xlsx"
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()
    worksheet.write_column("A1", unknown_barcodes)
    workbook.close()
    pass


def uni_no_spike_output(incorrect_combinations, unknown_barcodes,
                        unknown_i5, unknown_i7, correct_i5, correct_i7,
                        correct_barcodes):
    # TODO: Docstrings / comments
    output_file = output_folder + output_filename + ".xlsx"

    excel_2d_array = [["", "", "i7 barcodes"],
                      ["", ""],
                      ["i5 barcodes", correct_i5[0]]]

    excel_2d_array[1].extend(correct_i7)
    for i in range(1, len(correct_i5)):
        excel_2d_array.append(["", correct_i5[i]])

    excel_2d_array[1].append("Total")
    excel_2d_array.append(["", "Total"])

    for i in excel_2d_array:
        print(i)

    # TODO: Create dict {key i5 barcode: [counter first i7, second i7, etc]} to make it easier to write to excel file

    # with xlsxwriter.Workbook(output_file) as workbook:
    #     worksheet = workbook.add_worksheet()
    #
    #     for row_num, data in enumerate(excel_2d_array):
    #         worksheet.write_row(row_num, 0, data)
