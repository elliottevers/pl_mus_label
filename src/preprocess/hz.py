import math


def remove_redundancies(seq_hertz):
    nonzero = [0 if not h or math.isinf(h) or math.isnan(h) or h < 0 else int(h) for h in seq_hertz]

    last = nonzero[0]

    diff = []

    for samp in nonzero:
        if samp == last:
            last = samp
            continue
        else:
            last = samp
            diff.append(samp)

    return diff
