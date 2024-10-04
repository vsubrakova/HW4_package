# HW4_package

# Description: This program filters a set of FASTQ sequences
# based on their GC content, length, and quality scores,
# and applies DNA/RNA sequence processing tools to the filtered sequences.

# Input: The program takes a dictionary of FASTQ sequences
# where each entry contains a sequence and its corresponding quality scores.
# The filtering is based on GC content, length, and quality thresholds.
# After filtering, the program accepts variable arguments representing
# DNA or RNA sequences (as strings) and the name of a procedure to
# perform on these sequences.

# Output: The filter_fastq function modifies the original FASTQ dictionary
# by removing sequences that do not meet the criteria.
# The run_dna_rna_tools function returns the result of the
# specified operation applied to all filtered DNA or RNA sequences.

# Authors: VS

import source.suppl_filter_fastq as sfq
import source.suppl_run_dna_rna_tools as sdnat


def filter_fastq(seqs: dict,
                 gc_bounds: int | tuple = (0, 100),
                 length_bounds: int | tuple = (0, 2**32),
                 quality_threshold: float = 0) -> dict:
    """
    Фильтрует словарь последовательностей на основе критериев содержания GC,
    длины и среднего качества. Удаляет из исходного словаря
    последовательности, не прошедшие фильтры.

    Args:
    seqs (dict): Словарь с последовательностями FASTQ, где ключ - имя
    последовательности, а значение - кортеж(нуклеотидная последовательность,
    строка качества).
    gc_bounds (tuple): Диапазон содержания GC для фильтрации.
    По умолчанию (0, 100).
    length_bounds (tuple): Диапазон длины последовательности для фильтрации.
    По умолчанию (0, 2**32).
    quality_threshold (float): Пороговое значение качества по шкале phred33.
    По умолчанию 0.

    Returns:
    None: Функция изменяет исходный словарь seqs, удаляя неподходящие
    последовательности."""

    if isinstance(gc_bounds, int):
        gc_bounds = (0, gc_bounds)

    if isinstance(length_bounds, int):
        length_bounds = (0, length_bounds)

    filtered_seqs = {}

    for name, (sequence, cigar) in seqs.items():
        if (sfq.has_sufficient_gc(sequence, gc_bounds)
                and sfq.has_sufficient_length(sequence, length_bounds)
                and sfq.has_sufficient_quality(cigar, quality_threshold)):
            filtered_seqs[name] = (sequence, cigar)

    return filtered_seqs


def run_dna_rna_tools(*args: str, results: list = None) -> str | list:
    """
    Выполняет указанную операцию (транскрипция, реверс, комплементарность,
    реверс-комплементарность) для последовательностей ДНК/РНК.

    Args:
    *args (str): Строки, где все, кроме последнего аргумента, являются
    последовательностями, а последний аргумент - имя операции для выполнения.
    results (list): Список для хранения результатов.

    Returns:
    str или list: Результат выполнения операции для каждой последовательности.
    Если одна последовательность, возвращается строка,
    иначе список результатов."""

    procedure = args[-1]
    sequences = args[:-1]

    procedures = {"transcribe": sdnat.transcribe,
                  "reverse": sdnat.reverse,
                  "complement": sdnat.complement,
                  "reverse_complement": sdnat.reverse_complement}

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
