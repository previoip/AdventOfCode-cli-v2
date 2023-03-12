from math import isclose

class vec2:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __add__(self, o):
        x = self._x + o._x
        y = self._y + o._y
        return self.__class__(x, y)

    def __sub__(self, o):
        x = self._x - o._x
        y = self._y - o._y
        return self.__class__(x, y)

    def __eq__(self, o):
        return isclose(self._x, o._x) and isclose(self._y, o._y)

    def __repr__(self):
        return f'({self._x}, {self._y})'


TOK_ARROW = ['^',       'v',         '<',          '>'       ]
VEC_ARROW = [vec2(0, 1), vec2(0, -1), vec2(-1, 0), vec2(1, 0)]

def process_input(_input_str: str):
    result = _input_str
    
    return result

def part_1(_input):
    result = 1
    trace = [vec2(0, 0)]
    curr_p = vec2(0, 0)

    while _input:
        c = _input[0]
        _input = _input[1:]
        d = VEC_ARROW[TOK_ARROW.index(c)]
        curr_p += d
        if not curr_p in trace:
            trace.append(curr_p)
    result = len(trace)

    return result


def flip_the_flop(b: bool):
    if not b:
        b = True
    else:
        b = False
    return b

def part_2(_input):
    result = 1
    trace = [vec2(0, 0)]
    trace_c = [1]
    curr_p = vec2(0, 0)

    while _input:
        c = _input[0]
        _input = _input[1:]
        d = VEC_ARROW[TOK_ARROW.index(c)]
        curr_p += d
        if not curr_p in trace:
            trace.append(curr_p)
            trace_c.append(1)
    result = len(trace)
    
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

    run([path_executable, path_aoc, '-y 2015', '-d 3', '-p 1', '--test', '--silent'])
    run([path_executable, path_aoc, '-y 2015', '-d 3', '-p 2', '--test', '--silent'])
