#! -*- coding: utf-8 -*-

import sys
import importlib
import codecs
from argparse import ArgumentParser, Namespace
from typing import Optional, Text, Any, List
import cartoon

def import_class(import_string: str):
    try:
        module, classname = import_string.rsplit(".", 1)
        print(module, classname)
        cls = getattr(importlib.import_module(module), classname)
    except ValueError:
        sys.exit("Please supply module.classname.")
    except ImportError:
        sys.exit("Cannot import module %s" % module)
    except AttributeError:
        sys.exit("Cannot find class {} in module {}".format(classname, module))
    else:
        return cls

def parse(args: Optional[List[Any]]) -> Namespace:
    parser = ArgumentParser(prog="cartoon")
    
    parser.add_argument("-v", "--version", action="version", version=cartoon.__version__)

    parser.add_argument("-u", "--url", help="cartoon url")

    parser.add_argument("-l", "--list", help="list of cartoon link")

    return parser.parse_args(args=args)


def main():
    namespace = parse(sys.argv[1:])
    origin_url: Optional[str] = None
    list_mode: bool = False
    if namespace.url:
        origin_url = namespace.url
    if namespace.list:
        list_mode = True
        origin_url = namespace.list
    print("需要开始下载{origin_url} - {list_mode}".format(origin_url=origin_url, list_mode=list_mode))
    