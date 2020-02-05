#! -*- coding: utf-8 -*-

import os
import time
import re
from urllib import request, parse
import socket
from typing import List, Dict, Optional, Any, Union
from cartoon.util import log

FAKE_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",  # noqa
    "Accept-Charset": "UTF-8,*;q=0.5",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0",  # noqa
}

# global variables


def match1(text: str, *patterns: Any) -> Union[List[str], None]:

    ret: List[str] = []
    if len(patterns) == 1:
        pattern = patterns[0]
        match = re.search(pattern, text)
        if match:
            ret.append(match.group(1))
        else:
            return None
    else:
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                ret.append(match.group(1))
    return ret


def urlopen_with_retry(*args, **kwargs):
    retry_time = 3
    for i in range(retry_time):
        try:
            return request.urlopen(*args, **kwargs)
        except Exception as e:
            if i + 1 == retry_time:
                raise e


def get_content(url: str, headers: Dict[str, str]={}) -> bytes:
    req = request.Request(url, headers=headers)
    response = urlopen_with_retry(req)
    data = response.read()
    return data


def post_content(
    url: str, headers: Dict[str, str] = {}, post_data: Dict[str, Any] = {}, **kwargs
) -> bytes:
    req = request.Request(url, headers=headers)
    if kwargs.get("post_data_raw"):
        post_data_enc = bytes(kwargs["post_data_raw"], "utf-8")
    else:
        post_data_enc = bytes(parse.urlencode(post_data), "utf-8")
    response = urlopen_with_retry(req, data=post_data_enc)
    data = response.read()
    return data


def url_size(url: str, headers: Dict[str, str] = {}):
    if headers:
        response = urlopen_with_retry(request.Request(url, headers=headers))
    else:
        response = urlopen_with_retry(request.Request(url))
    size = response.headers.get("content-length")
    return int(size) if size is not None else float("inf")


def urls_size(urls: List[str], headers: Dict[str, str]={}):
    return sum(url_size(url, headers) for url in urls)


def url_save(
    url: Union[List[str], str],
    filepath: str,
    headers: Optional[Dict[str, str]] = None,
    refer:Optional[str] = None,
    timeout: Optional[float] = None,
    **kwargs
):
    temp_headers = headers.copy() if headers is not None else {}
    if refer is not None:
        temp_headers.setdefault("refer", refer)

    if isinstance(url, list):
        file_size = urls_size(url, temp_headers)
        is_chunked, urls = True, url
    else:
        file_size = url_size(url, temp_headers)
        is_chunked, urls = False, [url]

    open_mode = "wb"
    temp_filename = filepath + ".download" if file_size != float("inf") else filepath
    # received: int = 0

    for url in urls:
        if timeout:
            response = urlopen_with_retry(request.Request(url, headers=temp_headers), timeout=timeout)
        else:
            response = urlopen_with_retry(request.Request(url, headers=temp_headers))
        log.i("saving {}".format(url))
        with open(temp_filename, open_mode) as output:
            while True:
                buffer = None
                try:
                    buffer = response.read(1024 * 256)
                except Exception as e:
                    print(e)
                    break
                else:
                    if not buffer:
                        break
                    output.write(buffer)
        
        if os.access(filepath, os.W_OK):
            os.remove(filepath)
        os.rename(temp_filename, filepath)