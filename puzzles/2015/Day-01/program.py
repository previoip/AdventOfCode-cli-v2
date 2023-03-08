

def process_input(_input_str: str):
    result = _input_str
    return result

def part_1(_input):
    result = 0

    while _input and '()' in _input:
        _input = _input.replace('()', '')

    while _input:
        s = _input[0]
        _input = _input[1:]

        if s == '(':
            result += 1

        if s == ')':
            result -= 1

    return result

def part_2(_input):
    c = 0
    result = 0

    while _input:
        result += 1
        s = _input[0]
        _input = _input[1:]

        if s == '(':
            c += 1

        if s == ')':
            c -= 1

        if c == -1:
            return result

    return result




if __name__ == '__main__':
    import sys
    from pathlib import Path
    from subprocess import run
    from inspect import getsourcefile

    path_this = Path(getsourcefile(lambda: 0))

    path_aoc = path_this
    while 'aoc.py' not in [i.name for i in path_aoc.glob('*')]:
        path_aoc /= '..'
    path_aoc = path_aoc.resolve()
    path_aoc /= 'aoc.py'

    path_executable = Path(sys.executable).resolve()

    # run([path_executable, path_aoc, '-y 2015', '-d 1', '-p 1', '--test', '--silent'])
    run([path_executable, path_aoc, '-y 2015', '-d 1', '-p 2', '--test', '--silent'])
