import numpy as np
from typing import List, Tuple
import time

q1, q2 = 101, 169
d = 256
d_shift = int(np.sqrt(d))


def my_hash(pattern: str, pattern_length: int, q: int):
    hw = 0
    for i in range(pattern_length):
        hw = ((hw << d_shift) + ord(pattern[i])) % q

    return hw


def bloom_hash(text: str, k: int) -> List[int]:
    pattern_length = len(text)
    hash_values = []
    for i in range(k):
        hash_values.append(my_hash(text, pattern_length, q1) + i * my_hash(text, pattern_length, q2))

    return hash_values


def rolling_hash(text: str, hash_values: List[int]) -> List[int]:
    new_hash_values = []
    for i, hash_value in enumerate(hash_values):
        # TODO: Wystarczy wziąć jej wartość dla pierwszego podciągu i odjąć wartość zależną od pierwszej
        #  litery pierwszego a dodać wartość zależną od ostatniej drugiego
        new_hash_value = hash_value

        new_hash_values.append(new_hash_value)

    return new_hash_values


def rabin_karp_with_bloom(txt_file: str, patterns: List[str], p: float = 0.001, n: int = 20):
    b = int((-n) * np.log(p) / np.log(2) ** 2)
    k = int(b / n * np.log(2))

    with open(txt_file, encoding='utf-8') as f:
        text = f.readlines()  # Lista linii tekstu

    s = ' '.join(text).lower()
    patterns = [pattern.lower() for pattern in patterns]
    pattern_length = len(patterns[0])
    s_length = len(s)
    patterns_quantity = len(patterns)

    positions = []
    same_hash = 0
    no_comp = 0

    bloom_filter_pattern = np.empty((b,), dtype=bool)
    for pattern in patterns:
        pattern_hash_values = bloom_hash(pattern, k)
        pattern_hash_indexes = [el % b for el in pattern_hash_values]
        for idx in pattern_hash_indexes:
            bloom_filter_pattern[idx] = True

    m = 0
    # s_hash_values = bloom_hash(s[m: m + pattern_length], k)
    while m < s_length - pattern_length + 1:
        s_hash_values = bloom_hash(s[m: m + pattern_length], k)
        s_hash_indexes = [el % b for el in s_hash_values]
        no_comp += patterns_quantity
        if all([True if bloom_filter_pattern[idx] else False for idx in s_hash_indexes]):
            same_hash += 1
            no_comp += pattern_length * patterns_quantity
            if any(s[m: m + pattern_length] == pattern for pattern in patterns):
                positions.append(m)

        # s_hash_values = rolling_hash(s, s_hash_values)
        m += 1

    return positions, no_comp, same_hash


def main():
    t1_start = time.perf_counter()
    out1 = rabin_karp_with_bloom("lotr.txt",
                                 ['gandalf', 'looking', 'blocked', 'comment', 'pouring', 'finally', 'hundred',
                                  'hobbits', 'however', 'popular', 'nothing', 'enjoyed', 'stuffed', 'relaxed',
                                  'himself', 'present', 'deliver', 'welcome', 'baggins', 'further'])
    t1_stop = time.perf_counter()

    print("Czas: {:.7f}".format(t1_stop - t1_start))
    print(f"{len(out1[0])}; {out1[1]}")


if __name__ == "__main__":
    main()
