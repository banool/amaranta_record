#!/usr/bin/env python

import argparse

from buttons_input import run as buttons_input_run
from keyboard_input import run as keyboard_input_run


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        choices=("keyboard", "buttons"),
        required=True,
        help="Which input to use",
    )
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.input == "keyboard":
        keyboard_input_run()
    if args.input == "buttons":
        buttons_input_run()


if __name__ == "__main__":
    main()
