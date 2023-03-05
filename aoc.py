import argparse
import os
import sys
import datetime
import shutil
import json
from pathlib import Path
from configparser import ConfigParser
from importlib import util as importlib_util
from inspect import getsourcefile
from src.ascii_art import ascii_header
from src.data_parser import parse


INIT_CHECK = True
FPATH_FOLDER_PUZZLE = 'puzzles\\'
FPATH_FOLDER_TEMPLATE = 'src\\_template\\'
FPATH_FILE_STAT = 'stats.json'
FPATH_FILE_README = 'README.md'
FPATH_FILE_CONFIG = 'conf.ini'

def check_access_to_paths(*paths: str):
    for path in paths:
        if not os.access(path, os.R_OK ^ os.W_OK):
            if not args.silent: print(f'folder is inaccessible: {path}')
            sys.exit()

def puzzle_day_to_str(day: int):
    return 'Day-{:02}'.format(day)

def puzzle_day_from_str(puzzle_day_str: str):
    return int(puzzle_day_str.split('-')[-1])

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

def serialize_stat_fp(path_stat: Path, stat_obj: dict):
    with path_stat.open('w') as fp: 
        json.dump(stat_obj, fp)
    

def deserialize_stat_fp(path_stat: Path, stat_obj: dict = {}):
    if not path_stat.exists():
        with path_stat.open('w') as fp:
            if not stat_obj:
                stat_obj = {'status_enum': ['new', 'on-progress', 'test-assertion-failed', 'finished'], 'status': {}}
            json.dump(stat_obj, fp)
    else:
        with path_stat.open('r') as fp: 
            stat_obj = json.load(fp)
    return stat_obj

def update_stat(stat_obj, year:int, day:int, part:int, enum_id:int):
    if enum_id < 0 or enum_id > len(stat_obj['status_enum']):
        raise ValueError(f'enum_id is not valid index: {enum_id}')
    
    k_y = str(year)
    y = stat_obj['status'].get(k_y)
    if not y and not isinstance(y, dict):
        stat_obj['status'][k_y] = {}
    
    k_d = puzzle_day_to_str(day)
    d = stat_obj['status'][k_y].get(k_d)
    if not d and not isinstance(d, dict):
        d = stat_obj['status'][k_y] = {k_d: {}}

    stat_obj['status'][k_y][k_d][str(part)] = enum_id
    return stat_obj
        


def main():
    path_cwd      = Path(os.path.abspath(getsourcefile(lambda:0) + '/..'))
    path_puzzle   = path_cwd / FPATH_FOLDER_PUZZLE
    path_template = path_cwd / FPATH_FOLDER_TEMPLATE
    path_stat     = path_cwd / FPATH_FILE_STAT
    path_readme   = path_cwd / FPATH_FILE_README
    path_config   = path_cwd / FPATH_FILE_CONFIG
    year_curr     = datetime.date.today().year

    if not path_puzzle.exists():
        path_puzzle.mkdir()

    if not path_readme.exists():
        raise RuntimeError(f'{FPATH_FILE_README} file does not exist.')

    if not path_config.exists():
        raise RuntimeError(f'{FPATH_FILE_CONFIG} file does not exist.')

    config = ConfigParser()
    config.read(path_config)
    if config['DEFAULT'].getboolean('check_init'): check_access_to_paths(path_puzzle, path_stat, path_template, *path_puzzle.rglob('*'))

    stat_obj = deserialize_stat_fp(path_stat, stat_obj)

    parser = argparse.ArgumentParser(
        prog='aoc',
        description="CLI AOC Puzzle manager"
    )

    parser.add_argument(
        '--new',
        action='store_true',
        help='create new puzzle folder instance and exit'
    )

    parser.add_argument(
        '--gen-readme',
        action='store_true',
        help=f'puts {FPATH_FILE_STAT} into readme.md and exit'
    )

    parser.add_argument(
        '-y',
        metavar='[YEAR]',
        type=int,
        action='store',
        default=year_curr,
        help=f'puzzle [year] selector',
        dest='year'
    )

    parser.add_argument(
        '-d',
        metavar='[PUZZLE_DAY]',
        type=int,
        action='store',
        default=0,
        choices=range(1, 28),
        help='puzzle [day] selector',
        dest='day'
    )

    parser.add_argument(
        '-p',
        metavar='[PUZZLE_PART]',
        type=int,
        action='store',
        default=1,
        choices=[1, 2],
        help='puzzle [part] selector',
        dest='part'
    )

    parser.add_argument(
        '--test',
        action='store_true',
        help='run puzzle using test dataset',
        dest='test'
    )

    parser.add_argument(
        '--silent',
        action='store_true',
        help='disable logging to stdout (except for puzzle output)',
        dest='silent'
    )

    args = parser.parse_args()

    if args.gen_readme:
        return

    puzzle_day_format = puzzle_day_to_str(args.day)
    path_puzzle_to_year = path_puzzle / str(args.year)
    path_puzzle_to_day  = path_puzzle_to_year / puzzle_day_format

    if args.day == 0:
        dir_list = list(path_puzzle_to_year.glob('*'))
        day_latest = 0
        if dir_list:
            day_latest = puzzle_day_from_str(dir_list[-1].name)
            args.day = day_latest
        puzzle_day_format = puzzle_day_to_str(day_latest)
        path_puzzle_to_day  = path_puzzle_to_year / puzzle_day_format

    if args.new:
        day_increment = puzzle_day_from_str(puzzle_day_format) + 1
        puzzle_day_format = puzzle_day_to_str(day_increment)
        path_puzzle_to_day  = path_puzzle_to_year / puzzle_day_format
        if path_puzzle_to_day.exists() or day_increment > 27:
            print(f'could not create new puzzle folder {args.year}/{puzzle_day_format}')
            return

        if not args.silent: print(f'creating new puzzle folder: {args.year}/{puzzle_day_format}')
        shutil.copytree(path_template, path_puzzle_to_day)

        path_puzzle_program = path_puzzle_to_day / 'program.py'
        with open(path_puzzle_program, 'r') as fo:
            prog_content = fo.readlines()
            prog_content[-1] = ''
            prog_content[-1] += f"    run([path_executable, path_aoc, '-y {args.year}', '-d {day_increment}', '-p 1', '--test', '--silent'])\n"
            prog_content[-1] += f"    run([path_executable, path_aoc, '-y {args.year}', '-d {day_increment}', '-p 2', '--test', '--silent'])\n"

        with open(path_puzzle_program, 'w') as fo:
            fo.writelines(prog_content)
        update_stat(stat_obj, args.year, args.day, 1, 0)
        update_stat(stat_obj, args.year, args.day, 2, 0)
        serialize_stat_fp(path_stat, stat_obj)
        return

    # begin
    if not args.silent:
        _title_head = ascii_header(f'aoc {args.year}')
        _title_head_wide = len(_title_head.splitlines()[0])
        print()
        print('='*_title_head_wide)
        print(_title_head)
        print(pad_str(f' Day {args.day} Part {args.part} ', _title_head_wide, align='c', fill='-'))
        print('='*_title_head_wide)
        print()

    if not path_puzzle_to_day.exists():
        print('WARNING! target puzzle does not exist.')
        return

    path_puzzle_program = path_puzzle_to_day / 'program.py'
    path_puzzle_data = path_puzzle_to_day / 'data'
    path_puzzle_data_true_data = path_puzzle_data / 'data.txt'
    path_puzzle_data_test_data = path_puzzle_data / 'tests.txt'

    _spec = importlib_util.spec_from_file_location('program', path_puzzle_program)
    _prog_module = importlib_util.module_from_spec(_spec)
    _spec.loader.exec_module(_prog_module)

    if args.test:
        with path_puzzle_data_test_data.open('rb') as fo:
            data_object = parse(fo.read())
    else:
        with path_puzzle_data_true_data.open('rb') as fo:
            data_object = parse(fo.read())

    _temp = None
    for dtable in data_object.get_multiple_prfx('data'):
        name_dict = dtable.unpack_name([None, None, 'part'])
        if name_dict['part'] == '2' and not dtable.get('data'):
            if not args.silent: print(f'> puzzle part 2 data is empty, fetching from part 1')
            dtable.set_value('data', _temp)
        else:
            _temp = dtable.get('data')
    del _temp

    for dtable in data_object.get_multiple_prfx('data'):
        name_dict = dtable.unpack_name([None, None, 'part', None, 'test'])
        if name_dict.get('part') != str(args.part):
            data_object.pop(dtable)
            continue
        if not args.silent: print(f'> processing data {dtable.name}')
        dtable.set_value('data', _prog_module.process_input(dtable.get('data')))

    eval_func = getattr(_prog_module, f'part_{args.part}')

    for dtable in data_object.get_multiple_prfx('data'):
        if not args.silent: print(f'> evaluating: {dtable.name}')
        eval_result = eval_func(dtable.get('data'))
        print(f'>> evaluation result: {eval_result}')
        update_stat(stat_obj, args.year, args.day, args.part, 1)
        if args.test:
            res = dtable.get('res')
            if str(eval_result) == res:
                print(f'>> test passed')
                update_stat(stat_obj, args.year, args.day, args.part, 3)
            else:
                print(f'>> assertion failed {eval_result} != {res}')
                update_stat(stat_obj, args.year, args.day, args.part, 2)

    serialize_stat_fp(path_stat, stat_obj)

if __name__ == '__main__':
    main()