import timeit

def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    
    # Таблиця останніх входжень символів
    last = {}
    for i in range(m):
        last[pattern[i]] = i
    
    i = m - 1
    while i < n:
        j = m - 1
        k = i
        while j >= 0 and text[k] == pattern[j]:
            k -= 1
            j -= 1
        if j == -1:
            return k + 1
        skip = last.get(text[i], -1)
        i += m - min(j, 1 + skip)
    return -1

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0

    # LPS-масив
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    i = 0
    j = 0
    while i < n:
        if text[i] == pattern[j]:
            i += 1
            j += 1
        if j == m:
            return i - j
        elif i < n and text[i] != pattern[j]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

def rabin_karp(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    d = 256
    q = 101
    h = pow(d, m-1) % q
    p = 0
    t = 0

    # Початкові хеші
    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                return i
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return -1

with open("article1.txt", "r", encoding="utf-8") as f:
    text1 = f.read()

with open("article2.txt", "r", encoding="utf-8") as f:
    text2 = f.read()

real_pattern1 = "аналізувати і вирішувати проблеми"
fake_pattern1 = "Sapienti sat"
real_pattern2 = "а при зміні розміру немає необхідності розширювати область пам’яті."
fake_pattern2 = "Exorcizamus te omnis immundus spiritus"

def measure_time(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=100)

# Для статті 1
bm_real1 = measure_time(boyer_moore, text1, real_pattern1)
bm_fake1 = measure_time(boyer_moore, text1, fake_pattern1)
kmp_real1 = measure_time(kmp_search, text1, real_pattern1)
kmp_fake1 = measure_time(kmp_search, text1, fake_pattern1)
rk_real1 = measure_time(rabin_karp, text1, real_pattern1)
rk_fake1 = measure_time(rabin_karp, text1, fake_pattern1)

# Для статті 2
bm_real2 = measure_time(boyer_moore, text2, real_pattern2)
bm_fake2 = measure_time(boyer_moore, text2, fake_pattern2)
kmp_real2 = measure_time(kmp_search, text2, real_pattern2)
kmp_fake2 = measure_time(kmp_search, text2, fake_pattern2)
rk_real2 = measure_time(rabin_karp, text2, real_pattern2)
rk_fake2 = measure_time(rabin_karp, text2, fake_pattern2)

print("=== Стаття 1 ===")
print(f"Boyer-Moore: реальний = {bm_real1:.5f}, вигаданий = {bm_fake1:.5f}")
print(f"KMP:        реальний = {kmp_real1:.5f}, вигаданий = {kmp_fake1:.5f}")
print(f"Rabin-Karp: реальний = {rk_real1:.5f}, вигаданий = {rk_fake1:.5f}")

print("=== Стаття 2 ===")
print(f"Boyer-Moore: реальний = {bm_real2:.5f}, вигаданий = {bm_fake2:.5f}")
print(f"KMP:        реальний = {kmp_real2:.5f}, вигаданий = {kmp_fake2:.5f}")
print(f"Rabin-Karp: реальний = {rk_real2:.5f}, вигаданий = {rk_fake2:.5f}")
