def gen_chars(char: str, whitespace=' '):
    whitespace = whitespace[0]
    char_cache = """
       ██████   ██ ██████  ██████  ██   ██ ███████  ██████ ███████  █████   █████   █████  ██████   ██████ ██████  ███████ ███████  ██████  ██   ██ ██      ██ ██   ██ ██      ███    ███ ███    ██  ██████  ██████   ██████  ██████  ███████ ████████ ██    ██ ██    ██ ██     ██ ██   ██ ██    ██ ███████ 
      ██  ████ ███      ██      ██ ██   ██ ██      ██           ██ ██   ██ ██   ██ ██   ██ ██   ██ ██      ██   ██ ██      ██      ██       ██   ██ ██      ██ ██  ██  ██      ████  ████ ████   ██ ██    ██ ██   ██ ██    ██ ██   ██ ██         ██    ██    ██ ██    ██ ██     ██  ██ ██   ██  ██     ███  
      ██ ██ ██  ██  █████   █████  ███████ ███████ ███████     ██   █████   ██████ ███████ ██████  ██      ██   ██ █████   █████   ██   ███ ███████ ██      ██ █████   ██      ██ ████ ██ ██ ██  ██ ██    ██ ██████  ██    ██ ██████  ███████    ██    ██    ██ ██    ██ ██  █  ██   ███     ████     ███   
      ████  ██  ██ ██           ██      ██      ██ ██    ██   ██   ██   ██      ██ ██   ██ ██   ██ ██      ██   ██ ██      ██      ██    ██ ██   ██ ██ ██   ██ ██  ██  ██      ██  ██  ██ ██  ██ ██ ██    ██ ██      ██ ▄▄ ██ ██   ██      ██    ██    ██    ██  ██  ██  ██ ███ ██  ██ ██     ██     ███    
       ██████   ██ ███████ ██████       ██ ███████  ██████    ██    █████   █████  ██   ██ ██████   ██████ ██████  ███████ ██       ██████  ██   ██ ██  █████  ██   ██ ███████ ██      ██ ██   ████  ██████  ██       ██████  ██   ██ ███████    ██     ██████    ████    ███ ███  ██   ██    ██    ███████ 
    """.replace(' ', whitespace).splitlines()[1:-1]
    #              0  1  2  3  4  5  6  7  8  9  A  B  C  D  E  F  G  H  I  J  K  L  M   N   O  P  Q  R  S  T  U  V  W   X  Y  Z
    char_map = [6, 9, 4, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 9, 8, 3, 8, 8, 8, 11, 10, 9, 8, 9, 8, 8, 9, 9, 9, 10, 8, 9, 8]

    char = char.upper()
    char_ord = ord(char)

    if char_ord > 47 and char_ord < 58:
        char_ord -= 47
    elif char_ord > 64 and char_ord < 91:
        char_ord -= 64
        char_ord += 10
    else:
        char_ord = 0

    length = char_map[char_ord]
    offset = sum(char_map[:char_ord+1]) - length

    res = ['' for _ in range(5)]
    for n in range(5):
        res[n] = char_cache[n][offset: offset+length]
    return res

def ascii_header(string):
    res = ['' for _ in range(5)]
    for c in string:
        r = gen_chars(c)
        for n in range(5):
            res[n] += r[n]

    for n in range(5):
        res[n] = res[n][:-1]

    return '\n'.join(res)

if __name__ == '__main__':
    print(ascii_header('abcdefgzxyvw133742069'))
