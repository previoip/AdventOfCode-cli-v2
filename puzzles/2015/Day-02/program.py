
def area_prism(l, w, h):
    sides = [l*w, w*h, h*l]
    return sum(sides)*2 + min(sides)

def length_ribbon(l, w, h):
    perims = [l, w, h]
    a = perims.pop(perims.index(min(perims)))
    b = perims.pop(perims.index(min(perims)))
    return a + a + b + b + (l * w * h)
    

def process_input(_input_str: str):
    items = _input_str.splitlines()
    items = [list(map(int, i.split('x'))) for i in items]
    return items

def part_1(_input):
    items = _input
    area = 0
    for item in items:
        area += area_prism(*item)
    
    return area

def part_2(_input):
    items = _input
    length = 0
    for item in items:
        length += length_ribbon(*item)
    
    
    return length




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

    run([path_executable, path_aoc, '-y 2015', '-d 2', '-p 1', '--test', '--silent'])
    run([path_executable, path_aoc, '-y 2015', '-d 2', '-p 2', '--test', '--silent'])
