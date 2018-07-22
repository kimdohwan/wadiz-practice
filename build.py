#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

MODES = ['base', ]


def get_mode():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-m',
        '--mode',
        help=f'Docker build mode [{",".join(MODES)}]'
    )
    args = parser.parse_args()

    if args.mode:
        mode = args.mode.strip().lower()
    else:
        while True:
            print('Select mode')
            for index, mode in enumerate(MODES, start=1):
                print(f'{index}. {mode}')
            selected_mode = input('Choice: ')
            try:
                mode_index = int(selected_mode) - 1
                mode = MODES[mode_index]
                break
            except IndexError:
                print(f'숫자 1부터 {len(MODES)}까지 선택 가능')
    return mode


def mode_function(mode):
    print(f'{mode} 선택 후 mode_function 실행')
    if mode in MODES:
        cur_module = sys.modules[__name__]
        getattr(cur_module, f'build_{mode}')()
    else:
        raise ValueError(f'{MODES} 안에서 선택하세요 ')


def build_base():
    try:
        subprocess.call('pipenv lock -r > requirements.txt', shell=True)
        print('pipenv lock 실행')
        subprocess.call('docker build -t teamproject:base -f Dockerfile.base .', shell=True)
    finally:
        os.remove('requirements.txt')


if __name__ == '__main__':
    mode = get_mode()
    mode_function(mode)
