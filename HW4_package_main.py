# HW4_package 110924

# Description: This program filters a set of FASTQ sequences
# based on their GC content, length, and quality scores,
# and applies DNA/RNA sequence processing tools to the filtered sequences.

# Input: The program takes a dictionary of FASTQ sequences
# where each entry contains a sequence and its corresponding quality scores.
# The filtering is based on GC content, length, and quality thresholds.
# After filtering, the program accepts variable arguments representing
# DNA or RNA sequences (as strings) and the name of a procedure to
# perform on these sequences.

# Output: The filter_fastq function returns filtered FASTQ
# dictionary by removing sequences that do not meet the criteria.
# The run_dna_rna_tools function returns the result of the
# specified operation applied to all filtered DNA or RNA sequences.

# Authors: VS

import source.suppl_filter_fastq as sfq
import source.suppl_run_dna_rna_tools as sdnat
import source.bio_files_processor as bfp
import os


def filter_fastq(
    input_fastq: str,
    gc_bounds: int | tuple = (0, 100),
    length_bounds: int | tuple = (0, 2**32),
    quality_threshold: float = 0,
    output_fastq: str = None,
) -> dict | None:
    """
    Filters FASTQ sequences based on GC content, length, and quality score.

    Args:
    input_fastq (str): Path to the FASTQ file.
    gc_bounds (tuple or int, optional): GC content range for filtering.
    length_bounds (tuple or int, optional): Sequence length range for
    filtering.
    quality_threshold (float, optional): Minimum average quality
    score (phred33).
    output_fastq (str, optional): File name to write the filtered sequences.

    Returns:
    dict: A dictionary of filtered sequences if output_fastq is not provided.
    None: Filtered sequences are written in a file if output_fastq is provided.
    """

    if isinstance(gc_bounds, int):
        gc_bounds = (0, gc_bounds)

    if isinstance(length_bounds, int):
        length_bounds = (0, length_bounds)

    filtered_seqs = {}

    # Read fastq file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current working dir: {script_dir}")

    if not os.path.isabs(input_fastq):
        input_fastq = os.path.join(script_dir, "input_data", input_fastq)

    if output_fastq:
        filtered_output_dir = os.path.join(script_dir, "filtered")
        os.makedirs(filtered_output_dir, exist_ok=True)
        filtered_output_path = os.path.join(filtered_output_dir,
                                            output_fastq)

        with open(filtered_output_path, "w") as file:
            file.write("filtered_fastq = {\n")

    with open(input_fastq, "r") as infile:
        lines = []
        for line in infile:
            line = line.strip()
            lines.append(line)

            if (len(lines) == 4):
                name_line = lines[0]
                sequence_line = lines[1]
                cigar_line = lines[3]

                if (
                    sfq.has_sufficient_gc(sequence_line, gc_bounds)
                    and sfq.has_sufficient_length(sequence_line, length_bounds)
                    and sfq.has_sufficient_quality(cigar_line,
                                                   quality_threshold)
                ):
                    if output_fastq:
                        bfp.write_to_file(
                            filtered_output_path, name_line, sequence_line,
                            cigar_line)
                    else:
                        filtered_seqs[name_line] = (sequence_line, cigar_line)

                lines = []

    if output_fastq:
        with open(filtered_output_path, "a") as file:
            file.write("}\n")

    return filtered_seqs


def run_dna_rna_tools(*args: str, results: list = None) -> str | list:
    """
    Performs a specified procedure (transcription, reverse,
    complement, reverse complement) on DNA/RNA sequences.

    Args:
    *args (str): All arguments except the last are sequences, and the last
    argument is the name of the operation to perform.
    results (list, optional): List to store the results of the procedure.
    Default is None.

    Returns:
    str or list: If one sequence is provided, a string with the result
    is returned. If multiple sequences are provided, a list of results
    is returned.
    """

    procedure = args[-1]
    sequences = args[:-1]

    procedures = {
        "transcribe": sdnat.transcribe,
        "reverse": sdnat.reverse,
        "complement": sdnat.complement,
        "reverse_complement": sdnat.reverse_complement,
    }

    if results is None:
        results = []

    for sequence in sequences:
        try:
            sdnat.validate_composition(sequence)
            result = procedures[procedure](sequence)
        except ValueError as e:
            result = str(e)

        results.append(result)

    if len(results) == 1:
        return results[0]
    else:
        return results
