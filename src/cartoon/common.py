#! -*- coding: utf-8 -*-

import time
from urllib import request, parse
import socket

FAKE_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
    "Accept-Charset": "UTF-8,*;q=0.5",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",  # noqa
}

# global variables


def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            return request.urlopen(*args, **kwargs)
        except Exception as e:
            if i + 1 == retry_time:
                raise e


def get_content(url, headers={}) -> bytes:
    req = request.Request(url, headers=headers)
    response = urlopen_with_retry(req)
    data = response.read()
    return data


def post_content(url, headers={}, post_data={}, **kwargs) -> bytes:
    req = request.Request(url, headers=headers)
    if kwargs.get("post_data_raw"):
        post_data_enc = bytes(kwargs["post_data_raw"], "utf-8")
    else:
        post_data_enc = bytes(parse.urlencode(post_data), "utf-8")
    response = urlopen_with_retry(req, data=post_data_enc)
    data = response.read()
    return data


def url_size(url, headers={}):
    if headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(request.Request(url))
    size = response.headers.get("content-length")
    return int(size) if size is not None else float("inf")


def urls_size(urls, headers={}):
    return sum(url_size(url, headers) for url in urls)
