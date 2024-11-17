

def has_sufficient_gc(sequence: str, gc_bounds: tuple) -> bool:

    gc_content = ((sequence.count("G") + sequence.count("C"))
                  / len(sequence)) * 100
    return gc_bounds[0] <= gc_content <= gc_bounds[1]


def has_sufficient_length(sequence: str, length_bounds: tuple) -> bool:

    seq_length = len(sequence)
    return length_bounds[0] <= seq_length <= length_bounds[1]


def has_sufficient_quality(cigar: str, quality_threshold: float) -> bool:

    quality = sum(ord(char) - 33 for char in cigar) / len(cigar)
    return quality >= quality_threshold
