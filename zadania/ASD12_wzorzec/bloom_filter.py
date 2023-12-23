import numpy as np
from typing import List, Tuple
import time

q1 = 101
d = 256
d_shift = int(np.sqrt(d))


def get_next_prime_number(n: int) -> int:
    while True:
        n += 1
        is_prime = True
        for i in range(2, n // 2):
            if n % i == 0:
                is_prime = False
                break

        if is_prime:
            return n


def my_hash(text: str, pattern_length: int, q: int):
    hw = 0
    for i in range(pattern_length):
        hw = ((hw << d_shift) + ord(text[i])) % q

    return hw


def bloom_hash(text: str, prime_numbers: List[int]) -> List[int]:
    hash_values = []
    for q in prime_numbers:
        hash_values.append(my_hash(text, len(text), q))

    return hash_values


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

    prime_numbers = [q1]
    for _ in range(k - 1):
        prime_numbers.append(get_next_prime_number(prime_numbers[-1]))

    bloom_filter_pattern = np.empty((b,), dtype=bool)
    for pattern in patterns:
        pattern_hash_values = bloom_hash(pattern, prime_numbers)
        pattern_hash_indexes = [el % b for el in pattern_hash_values]
        for idx in pattern_hash_indexes:
            bloom_filter_pattern[idx] = True

    m = 0
    s_hash_values = bloom_hash(s[m: m + pattern_length], prime_numbers)
    h = [1 for _ in range(k)]
    for idx, q in enumerate(prime_numbers):
        for i in range(pattern_length - 1):
            h[idx] = (h[idx] << d_shift) % q

    while m < s_length - pattern_length:
        s_hash_indexes = [el % b for el in s_hash_values]
        no_comp += patterns_quantity
        if all([True if bloom_filter_pattern[idx] else False for idx in s_hash_indexes]):
            same_hash += 1
            no_comp += pattern_length * patterns_quantity
            if any(s[m: m + pattern_length] == pattern for pattern in patterns):
                positions.append(m)

        for i, hash_value in enumerate(s_hash_values):
            new_hash_value = (((hash_value - ord(s[m]) * h[i]) << d_shift) + ord(s[m + pattern_length])) % \
                             prime_numbers[i]
            new_hash_value = new_hash_value + prime_numbers[i] if new_hash_value < 0 else new_hash_value
            s_hash_values[i] = new_hash_value

        m += 1

    s_hash_indexes = [el % b for el in s_hash_values]
    no_comp += patterns_quantity
    if all([True if bloom_filter_pattern[idx] else False for idx in s_hash_indexes]):
        same_hash += 1
        no_comp += pattern_length * patterns_quantity
        if any(s[m: m + pattern_length] == pattern for pattern in patterns):
            positions.append(m)

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
