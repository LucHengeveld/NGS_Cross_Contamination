def bcl_to_fastq(parameters):
    # TODO: Code voor bcl te converten naar fastq met bijbehorende
    #  parameters van het converten (bv min quality)
    fastq_file = "C:\\Users\\luche\\Desktop\\example.fastq"
    return fastq_file


def fastq_reader(fastq_path):
    fastq_dict = {}
    with open(fastq_path, "r") as fastq_file:
        for line in fastq_file:
            if line.startswith("@"):
                barcode = line.split(":")[-1].replace("\n", "")
            elif line.replace("\n", "").isalpha():
                if barcode in fastq_dict.keys():
                    fastq_dict[barcode].append(line.replace("\n", ""))
                else:
                    fastq_dict[barcode] = [line.replace("\n", "")]

    return fastq_dict