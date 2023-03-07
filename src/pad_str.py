def pad_str(string, pad, align='left', fill=' '):
    r_length = len(string)
    l_length = 0
    if r_length > pad:
        return string

    r_length = pad - r_length

    if align[0] == 'r':
        l_length = r_length
        r_length = 0
    elif align[0] == 'c':
        l_length = r_length
        r_length = r_length // 2
        l_length = l_length - r_length

    return (fill*l_length) + string + (fill*r_length)
