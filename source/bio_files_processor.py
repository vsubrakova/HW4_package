import re


def write_to_file(out_path, name, sequence, cigar):
    with open(out_path, "a") as file:
        file.write(f"'{name}': ('{sequence}', '{cigar}'),\n")


def read_fastq_to_dict(input_fasta: str) -> dict:

    fasta_dict = {}

    print("Running 'convert_fastq_to_dict'\n")
    print(f"Processing input file: {input_fasta}")

    with open(input_fasta, "r") as infile:
        lines = []

        for line in infile:
            line = line.strip()
            lines.append(line)

            if len(lines) == 4:
                name_line = lines[0]
                sequence_line = lines[1]
                cigar_line = lines[3]
                fasta_dict[name_line] = (sequence_line, cigar_line)

                lines = []

    print("FASTQ file has been transformed into a dictionary.")

    return fasta_dict


def convert_multiline_fasta_to_oneline(input_fasta: str, output_fasta: str = None):

    if output_fasta is None:
        output_fasta = f"{input_fasta.split(".")[0]}_oneline.fasta"

    print("Running 'convert_multiline_fasta_to_oneline'\n")
    print(f"Processing input file: {input_fasta}")

    with open(input_fasta, "r") as infile, open(output_fasta, "w") as outfile:
        current_sequence = ""

        for line in infile:
            line = line.strip()

            if line.startswith(">"):
                if current_sequence:
                    outfile.write(current_sequence + "\n")
                outfile.write(line + "\n")
                current_sequence = ""
            else:
                current_sequence += line

        if current_sequence:
            outfile.write(current_sequence + "\n")

    print(f"Converted FASTA file has been saved to {output_fasta}")


def parse_blast_output(input_file: str, output_file: str = None):

    if output_file is None:
        output_file = f"{input_file.split(".")[0]}_parsed.txt"

    print("Running 'parse_blast_output'\n")
    print(f"Processing input file: {input_file}")

    with open(input_file, "r") as infile, open("temp_file.txt", "w") as tempfile:
        parsing = False

        for line in infile:

            if "Sequences producing significant alignments:" in line:
                parsing = True
                continue

            if parsing:
                next_line = infile.readline()
                next_line = infile.readline()
                description = next_line.split("...")[0].strip()
                description = re.split(r"\s{2,}", description)[0]
                tempfile.write(description + "\n")
                parsing = False

    sort_and_remove_duplicates(temp_file="temp_file.txt", output_file=output_file)

    print(f"Parsed protein names have been saved to {output_file}")


def sort_and_remove_duplicates(temp_file: str, output_file: str):

    lines = set()

    with open(temp_file, "r") as tempfile:
        for line in tempfile:
            lines.add(line.strip())

    sorted_lines = sorted(lines)

    with open(output_file, "w") as outfile:
        for line in sorted_lines:
            outfile.write(line + "\n")

    print("Protein names sorted and deduplicated.")
