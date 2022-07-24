def substrings_in_strings(substrings, strings):
    if type(strings) != list:
        strings = [strings]
    if type(substrings) != list:
        substrings = [substrings]
    for string in strings:
        for substring in substrings:
            if substring == "":
                continue
            if substring in string:
                return string
    return ""
