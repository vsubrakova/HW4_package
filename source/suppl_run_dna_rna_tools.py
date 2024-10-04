
translation_table = str.maketrans('atgcuATGCU', 'tacgaTACGA')
valid_dna_nucleotides = set("atgcATGC")
valid_rna_nucleotides = set("augcAUGC")
valid_nucleotides = valid_dna_nucleotides | valid_rna_nucleotides


def transcribe(sequence: str) -> str:
    """Заменяет все T на U"""
    return sequence.replace("t", "u").replace("T", "U")


def reverse(sequence: str) -> str:
    """Возвращает развёрнутую последовательность"""
    return sequence[::-1]


def complement(sequence: str) -> str:
    """Возвращает комплементарную последовательность"""
    return sequence.translate(translation_table)


def reverse_complement(sequence: str) -> str:
    """Возвращает обратную комплементарную последовательность"""
    return reverse(complement(sequence))


def validate_composition(sequence: str) -> str:
    invalid_characters = set(sequence) - valid_nucleotides
    if invalid_characters:
        raise ValueError(
            f"Ошибка: последовательность {sequence} содержит недопустимые "
            f"символы:{', '.join(invalid_characters)}"
        )

    if "T" in sequence.upper() and "U" in sequence.upper():
        raise ValueError(
            f"Ошибка: обнаружены одновременно T и U:{sequence}"
        )

    return sequence
