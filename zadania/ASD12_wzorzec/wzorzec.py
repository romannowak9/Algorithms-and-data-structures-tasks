import math
from typing import Tuple, List
import time

d = 256
d_shift = int(math.sqrt(d))
q = 101  # liczba pierwsza


def hash(word, pattern_length):
    hw = 0
    for i in range(pattern_length):  # długość wzorca
        hw = ((hw << d_shift) + ord(word[i])) % q  # dla d będącego potęgą 2 można mnożenie zastąpić shiftem

    return hw


def naive_method(txt_file: str, pattern: str) -> Tuple[List[int], int]:
    with open(txt_file, encoding='utf-8') as f:
        text = f.readlines()  # Lista linii tekstu

    s = ' '.join(text).lower()
    pattern = pattern.lower()
    pattern_length = len(pattern)
    positions = []
    m = 0
    no_comp = 0
    while m < len(s) - pattern_length + 1:
        no_comp += pattern_length
        if s[m: m + pattern_length] == pattern:
            positions.append(m)

        m += 1

    return positions, no_comp


def rabin_karp(txt_file: str, pattern: str) -> Tuple[List[int], int, int]:
    with open(txt_file, encoding='utf-8') as f:
        text = f.readlines()  # Lista linii tekstu

    s = ' '.join(text).lower()
    pattern = pattern.lower()
    positions = []
    s_length = len(s)
    pattern_length = len(pattern)
    no_comp = 0
    m = 0
    same_hash = 0
    hash_pattern = hash(pattern, pattern_length)
    hash_s = hash(s[m: m + pattern_length], pattern_length)
    h = 1
    for i in range(pattern_length - 1):
        h = (h << d_shift) % q

    while m < s_length - pattern_length:
        no_comp += 1
        if hash_s == hash_pattern:
            same_hash += 1
            if s[m: m + pattern_length] == pattern:
                no_comp += pattern_length
                positions.append(m)

        hash_s = (((hash_s - ord(s[m]) * h) << d_shift) + ord(s[m + pattern_length])) % q
        hash_s = hash_s + q if hash_s < 0 else hash_s
        m += 1

    no_comp += 1
    if hash_s == hash_pattern:
        same_hash += 1
        if s[m: m + pattern_length] == pattern:
            no_comp += pattern_length
            positions.append(m)

    return positions, no_comp, same_hash


def kmp_table(pattern: str) -> List[int]:
    pattern_length = len(pattern)
    t_out = [0 for _ in range(pattern_length + 1)]
    pos = 1
    cnd = 0

    t_out[0] = -1
    while pos < pattern_length:
        if pattern[pos] == pattern[cnd]:
            t_out[pos] = t_out[cnd]
        else:
            t_out[pos] = cnd
            while cnd >= 0 and pattern[pos] != pattern[cnd]:
                cnd = t_out[cnd]

        pos += 1
        cnd += 1

    t_out[pos] = cnd

    return t_out


def knuth_morris_pratt(txt_file: str, pattern: str):
    with open(txt_file, encoding='utf-8') as f:
        text = f.readlines()  # Lista linii tekstu

    s = ' '.join(text).lower()
    pattern = pattern.lower()
    positions = []
    no_comp = 0
    m = 0
    i = 0
    t = kmp_table(pattern)
    pattern_length = len(pattern)
    s_length = len(s)
    while m < s_length:
        no_comp += 1
        if pattern[i] == s[m]:
            m += 1
            i += 1
            if i == pattern_length:
                positions.append(m - i)
                i = t[i]
        else:
            i = t[i]
            if i < 0:
                m += 1
                i += 1

    return positions, no_comp, t


def main():
    t1_start = time.perf_counter()
    out1 = naive_method("lotr.txt", "time.")
    t1_stop = time.perf_counter()

    print("Czas dla metody naiwnej: {:.7f}".format(t1_stop - t1_start))
    print(f"{len(out1[0])}; {out1[1]}")

    t2_start = time.perf_counter()
    out2 = rabin_karp("lotr.txt", "time.")
    t2_stop = time.perf_counter()

    print("Czas dla metody rabina karpa: {:.7f}".format(t2_stop - t2_start))
    print(f"{out2[0]}; {len(out2[0])}; {out2[1]}; {out2[2]}")

    t3_start = time.perf_counter()
    out3 = knuth_morris_pratt("lotr.txt", "time.")
    t3_stop = time.perf_counter()

    print("Czas dla metody kmp: {:.7f}".format(t3_stop - t3_start))
    print(f"{len(out3[0])}; {out3[1]}; {out3[2]}")


if __name__ == "__main__":
    main()
