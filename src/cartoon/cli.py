#! -*- coding: utf-8 -*-

import os
import io
import re
import sys
import time
import json
import argparse
import logging
from importlib import import_module
from argparse import ArgumentParser
from typing import Tuple, Any, Dict, List, Callable, Optional, Union
from urllib import parse, request, error

import cartoon
from cartoon.common import *

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SITES: Dict[str, str] = {
    "fzdm": "fzdm",
    "jav468": "jav",
    "kuaikanmanhua": "kkmh",
}

# global var
prefer_list: bool = False

def url_to_module(url: str) -> Tuple[Any, str]:
    """
    find module by url, we match with dic SITES 

    Return: module name if matched
    """

    hosts = match1(url, (r"https?://([^/]+)/"))
    if not hosts:
        return (None, url)
    host: str = hosts[0]
    if host.endswith(".com.cn") or host.endswith(".ac.cn"):
        host = host[:-3]
    domains = match1(host, r"(\.[^.]+\.[^.]+)$") or []
    domain = domains[0] or host

    url = "".join([ch if ord(ch) in range(128) else parse.quote(ch) for ch in url])
    ks = match1(domain, r"([^.]+)") or []
    k = ks[0] or ""
    if k in SITES:
        return (import_module(".".join(["cartoon", "extractors", SITES[k]])), url)
    else:
        return (import_module(".".join(["cartoon", "extractors", "universal"])), url)


def any_download(url: str, **kwargs):
    """
    dowload a single html url
    use module if matched, otherwise we use universal downloader
    """
    m, url = url_to_module(url)
    m.prefer_download(url)


def any_download_playlist(url: str, **kwargs):
    """
    dowload a list html url
    use module if matched, otherwise we use universal downloader
    """
    m, url = url_to_module(url)
    m.prefer_download_list(url)


def download_main(
    download: Callable[..., None],
    download_playlist: Callable[..., None],
    urls: List[str],
):
    for url in urls:
        if re.match(r"https?://", url) is None:
            url = "http://" + url

        if prefer_list:
            download_playlist(url)
        else:
            download(url)


def parse_main(**kwargs):

    logging.basicConfig(format="[%(levelname)s] %(message)s")

    parser = ArgumentParser(
        prog="ct-get",
        usage="ct-get [OPTION] ... URL...",
        description="tool for cartoon downloader",
    )

    # version info
    parser.add_argument(
        "-v", "--version", action="version", version=cartoon.__version__
    )
    # 命令分组， 便于分割
    run_grp = parser.add_argument_group("Dry run options", "(no actual download)")
    run_grp.add_mutually_exclusive_group()

    run_grp.add_argument(
        "-i",
        "--info",
        action="store_true",
        help="Print extracted information with URLs",
    )
     
    # 下载选项
    download_grp = parser.add_argument_group("Download options")
    # debug 会输出一些信息
    download_grp.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Show traceback and other debug infomation",
    )
    # 下载的是列表
    download_grp.add_argument(
        "-l", "--playlist", action="store_true", help="prefer to download list"
    )
    # 将args参数赋予URL
    parser.add_argument("URL", nargs="*", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    global prefer_list
    if args.playlist:
        prefer_list = True

    URLs: List[str] = []
    URLs.extend(args.URL)
    download_main(any_download, any_download_playlist, URLs)


def main(**kwargs):
    """
    inner function
    """
    parse_main(**kwargs)
