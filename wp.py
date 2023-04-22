def highest_frequency(s):
    """
    This function takes a string 's' as input and returns the character with the highest frequency in 's'
    """
    s = ''.join(s)
    freq = {}
    for char in s:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    max_freq = max(freq.values())
    for char in freq:
        if freq[char] == max_freq:
            return char
