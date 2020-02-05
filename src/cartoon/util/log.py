#! -*- coding: utf-8 -*-

import os, sys

def sprint(text: str, *colors) -> str:
    return text

def println(text: str, *colors):
    sys.stdout.write(sprint(text, *colors) + "\n")

def print_err(text: str, *colors):
    sys.stderr.write(sprint(text, *colors) + "\n")

def print_log(text: str, *colors):
    sys.stderr.write(sprint(text, *colors) + "\n")

def i(message: str):
    print_log(message)

def yes_or_no(message: str) -> bool:
    ans = str(input("%s (y/N)" % message)).lower().strip()
    if ans == "y":
        return True
    return False