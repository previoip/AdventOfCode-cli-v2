

def process_input(_input_str: str):
    result = _input_str
    
    ...
    
    return result

def part_1(_input):
    result = _input
    
    ...
    
    return result

def part_2(_input):
    result = _input
    
    ...
    
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

    run([path_executable, path_aoc, '--help'])