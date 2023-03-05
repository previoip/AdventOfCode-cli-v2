

def process_input(input_str: str):
    result = sorted(map(int, input_str.splitlines()))
    result = list(result)
    
    return result

def part_1(input_str: str):
    while input_str:
        item = input_str.pop(0)
        for item_2nd in input_str:
            if item + item_2nd == 2020:
                return item * item_2nd
    
    return 0

def part_2(input_str: str):
    while input_str:
        item = input_str.pop(0)
        for item_2nd in input_str:
            for item_3rd in input_str:
                if item + item_2nd + item_3rd == 2020:
                    return item * item_2nd * item_3rd
    
    return 0




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

    run([path_executable, path_aoc, '-y 2020', '-d 1', '-p 1', '--test', '--silent'])
    run([path_executable, path_aoc, '-y 2020', '-d 1', '-p 2', '--test', '--silent'])
