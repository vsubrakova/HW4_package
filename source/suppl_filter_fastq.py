

def has_sufficient_gc(sequence: str, gc_bounds: int | tuple) -> bool:
    """
    Проверяет GC состав.

    Args:
    sequence (str): Нуклеотидная последовательность.
    gc_bounds (tuple): Диапазон для содержания GC.

    Returns:
    bool: True, если содержание GC в пределах указанного диапазона,
    иначе False."""

    gc_content = ((sequence.count("G") + sequence.count("C"))
                  / len(sequence)) * 100

    if len(gc_bounds) == 1:
        return gc_content <= gc_bounds[0]

    elif len(gc_bounds) == 2:
        return gc_bounds[0] <= gc_content <= gc_bounds[1]


def has_sufficient_length(sequence: str, length_bounds: tuple) -> bool:
    """
    Проверяет длину последовательности.

    Args:
    sequence (str): Нуклеотидная последовательность.
    length_bounds (tuple): Диапазон длины.

    Returns:
    bool: True, если длина последовательности в пределах указанного диапазона,
    иначе False.
    """
    seq_length = len(sequence)

    if len(length_bounds) == 1:
        return seq_length <= length_bounds[0]

    elif len(length_bounds) == 2:
        return length_bounds[0] <= seq_length <= length_bounds[1]


def has_sufficient_quality(cigar: str, quality_threshold: float) -> bool:
    """
    Проверяет среднее качество по шкале Phred33.

    Args:
    cigar (str): Строка символов качества.
    quality_threshold (float): Пороговое значение качества.

    Returns:
    bool: True, если среднее качество больше или раавно порогу, иначе False."""

    quality = sum(ord(char) - 33 for char in cigar) / len(cigar)
    return quality >= quality_threshold
